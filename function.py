import sqlite3
import numpy as np

def contenu_tables(nom_fichier):
    articles=[]
    titles=[]
    # Connexion à la base de données
    connexion = sqlite3.connect(nom_fichier)
    curseur = connexion.cursor()

    # Récupération des tables de la base de données
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = curseur.fetchall()

    # Parcourir les tables et afficher leur contenu
    for table in tables:
        nom_table = table[0]
        curseur.execute(f"SELECT * FROM {nom_table};")
        contenu = curseur.fetchall()
        for ligne in contenu:
          if ligne[1] not in titles:
            titles.append(ligne[1])
            articles.append(ligne[1]+' '+ligne[2])

    # Fermer la connexion
    connexion.close()
    return articles

def cos_sim(v1, v2):
    """Calcul de la similarité cosinus entre deux vecteurs."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def n_plus_proches(vecteur, liste_vecteurs,n):
    """Trouve les trois vecteurs les plus proches du vecteur donné."""
    sim_scores = []

    # Calculer les similarités cosinus entre le vecteur donné et chaque vecteur dans la liste
    for vec in liste_vecteurs:
        sim_scores.append(cos_sim(vecteur, vec))

    # Trouver les indices des trois vecteurs les plus proches
    indices_plus_proches = np.argsort(sim_scores)[-n:][::-1]
    return indices_plus_proches