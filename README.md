# Iliad Bot 

## Description

Ce projet concerne un bot d'assistance qui base ses réponses uniquement sur les articles offerts sur le site web https://assistance.free.fr/univers/. Le bot ne fournit jamais de réponses en dehors du contenu de ces articles.

## Démonstration

Une démonstration vidéo d'une conversation avec le bot est disponible à l'adresse suivante : https://1drv.ms/v/c/6736b90013a2951f/Ecb7ksXOfUNGgvkZUg2GXrIBzmDB3doTS6m74h8DquYgSQ?e=D73tNh

## Installation

Avant de commencer, il est nécessaire d'installer les prérequis.
```
pip install -r requirements.txt
```

## Génération de l'embedding des données

Le code source comprend un fichier `article_embedding.py` pour générer l'embedding des données. Pour l'exécuter, entrez la commande suivante dans le terminal :

```
python article_embedding.py
```

Cependant, l'embedding est déjà enregistré localement dans un fichier `embedding.pkl`, donc cette étape n'est pas nécessaire.

## Test du code

Pour tester le code, il suffit d'importer un fichier CSV contenant les questions. Ce fichier doit être nommé exactement `questions.csv` pour éviter les erreurs. Ensuite, exécutez la commande suivante dans le terminal :

```
python test.py
```

Le code fournira un nouveau fichier `reponses.csv` dans le même dossier, contenant les réponses à chaque question.

## Utilisation manuelle du bot

Pour utiliser manuellement le bot, exécutez la commande suivante dans le terminal :

```
python app.py
```

Attendez jusqu'à ce que le message suivant s'affiche :

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:54321
 * Running on http://192.168.1.171:54321
```

Copiez et collez l'URL dans votre navigateur web, et vous pourrez interagir avec le bot.
