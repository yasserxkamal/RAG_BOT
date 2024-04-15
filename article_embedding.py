

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from function import contenu_tables
import pickle
import sqlite3


# Exemple d'utilisation
nom_fichier_base_de_donnees = "assistance.sqlite3"
articles=contenu_tables(nom_fichier_base_de_donnees)

# Créer la fonction d'embedding
embedding_function = HuggingFaceEmbeddings()


# Générer les embeddings et les stocker dans un fichier
embeddings = [embedding_function.embed_query(article) for article in articles]
with open("embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f