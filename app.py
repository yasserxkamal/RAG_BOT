from flask import Flask, render_template, request
from function import contenu_tables, cos_sim, n_plus_proches
import numpy as np
from openai import OpenAI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import pickle
import sqlite3
import os

# Charger les variables d'environnement depuis le fichier .env
from dotenv import load_dotenv
load_dotenv()

# Récupérer les valeurs des variables d'environnement
API_KEY = os.getenv('API_KEY')

client = OpenAI(
  api_key=API_KEY,  # this is also the default, it can be omitted
)



# Exemple d'utilisation
nom_fichier_base_de_donnees = "assistance.sqlite3"
articles=contenu_tables(nom_fichier_base_de_donnees)

# Créer la fonction d'embedding
embedding_function = HuggingFaceEmbeddings()
messages_in=[]
conversation_in=[]

# Charger les embeddings depuis le fichier
with open("embeddings.pkl", "rb") as f:
    embeddings = pickle.load(f)




test=embedding_function.embed_query('test')


app = Flask(__name__)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    conversation=conversation_in
    conversation.append(query)
    if len(conversation)>1:
      conver_text=''
      for i in range(len(conversation)):
        if i%2==0:
          conver_text+=f'A: {conversation[i]}\n'
        else:
          conver_text+=f'B: {conversation[i]}\n'
      input_query=f'''Q:
      Reformulez la dernière message de la conversation suivante de manière claire et autonome, sans avoir besoin du contexte précédent.

      Conversation :
      A : J'aimerais trouver un nouveau livre à lire, avez-vous des suggestions ?
      B : Bien sûr, dans quel genre de livre êtes-vous intéressé ? Roman, biographie, essai ?
      A : Je préfère les romans historiques ou d'aventures.

      R:
      Pourriez-vous me recommander des romans dans les genres historique ou aventure ?

      Q:
      Reformulez la dernière message de la conversation suivante de manière claire et autonome, sans avoir besoin du contexte précédent.

      Conversation :
      A : Salut, j'aurais besoin de conseils pour choisir un nouveau téléphone portable.
      B : Bien sûr, quels sont vos critères principaux ? Budget, taille d'écran, performances...?
      A : Mon budget est d'environ 400 euros. La taille d'écran n'est pas un critère important pour moi.
      B : D'accord, et qu'en est-il de l'appareil photo ? Est-ce un élément décisif pour vous ?
      A : Oui, j'aimerais un bon appareil photo, c'est plutôt important.  

      R:
      Quelles seraient vos recommandations pour un smartphone autour de 400 euros avec un bon appareil photo ?

      Q:
      Reformulez la dernière message de la conversation suivante de manière claire et autonome, sans avoir besoin du contexte précédent.

      Conversation :
      {conver_text}
      R:'''
      completion =client.chat.completions.create(model="gpt-3.5-turbo-0125",temperature=0.3, messages=[{"role": "user", "content": input_query}])
      question = completion.choices[0].message.content
      conversation[-1]=question
    embedding_question=embedding_function.embed_query(conversation[-1])
    indices_proches = n_plus_proches(embedding_question, embeddings,3)
    input=f'''Article 1 : [{articles[indices_proches[0]]}]

    Article 2 : [{articles[indices_proches[1]]}]

    Article 3 : [{articles[indices_proches[2]]}]

    Question de l'utilisateur liée à l'article : [{conversation[-1]}]

    Consigne : Vos réponses aux questions doivent strictement se baser sur les informations présentes dans les articles fournis, sans jamais faire allusion aux articles eux-mêmes ou indiquer que vous les avez utilisés. En aucun cas vous ne devez mentionner, citer ou faire référence aux articles. Si la question n'est pas liée au contenu des articles, vous répondrez simplement que vous n'avez pas assez d'informations pour y répondre, sans donner d'autres explications.'''
    messages=messages_in
    messages.append({"role": "user", "content": input})
    completion =client.chat.completions.create(model="gpt-3.5-turbo-0125",temperature=0.3, messages=[{"role": "system", "content": " Vous êtes un système conçu pour répondre à toutes vos questions concernant les produits et services offerts par Iliad."}]+messages)
    response = completion.choices[0].message.content
    messages[-1]={"role": "user", "content": conversation[-1]}
    conversation.append(response)
    messages.append({"role": "assistant", "content": response})
    conversation_in[:]=conversation[-8:]
    messages_in[:]=messages[-8:]
    
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=54321)