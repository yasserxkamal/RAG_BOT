import csv
from openai import OpenAI
from function import contenu_tables, cos_sim, n_plus_proches
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import pickle
import sqlite3
import numpy as np
import os

# Charger les variables d'environnement depuis le fichier .env
from dotenv import load_dotenv
load_dotenv()

# Récupérer les valeurs des variables d'environnement
API_KEY = os.getenv('API_KEY')

client = OpenAI(
  api_key=API_KEY,  # this is also the default, it can be omitted
)

# Créer la fonction d'embedding
embedding_function = HuggingFaceEmbeddings()

# Charger les articles et leurs embeddings depuis les fichiers
# Exemple d'utilisation
nom_fichier_base_de_donnees = "assistance.sqlite3"
articles=contenu_tables(nom_fichier_base_de_donnees)

with open("embeddings.pkl", "rb") as f:
    embeddings = pickle.load(f)


def get_bot_response(query):
    embedding_query = embedding_function.embed_query(query)
    indices_proches = n_plus_proches(embedding_query, embeddings, 3)

    input_text = f'''Article 1 : [{articles[indices_proches[0]]}]

    Article 2 : [{articles[indices_proches[1]]}]

    Article 3 : [{articles[indices_proches[2]]}]

    Question de l'utilisateur liée à l'article : [{query}]

    Consigne : Vos réponses aux questions doivent strictement se baser sur les informations présentes dans les articles fournis, sans jamais faire allusion aux articles eux-mêmes ou indiquer que vous les avez utilisés. En aucun cas vous ne devez mentionner, citer ou faire référence aux articles. Si la question n'est pas liée au contenu des articles, vous répondrez simplement que vous n'avez pas assez d'informations pour y répondre, sans donner d'autres explications.'''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "Vous êtes un système conçu pour répondre à toutes vos questions concernant les produits et services offerts par Iliad."},
            {"role": "user", "content": input_text}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

# Lire les questions du fichier CSV
questions = []
with open("questions.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        questions.append(row[0])

# Obtenir les réponses du chatbot
responses = []
for question in questions:
    response = get_bot_response(question)
    responses.append(response)

# Écrire les réponses dans un nouveau fichier CSV
with open("reponses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for question, response in zip(questions, responses):
        writer.writerow([question, response])

print("Les réponses ont été enregistrées dans reponses.csv")