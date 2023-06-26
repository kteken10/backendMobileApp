import requests
import json

# Désactiver le support du proxy
requests.adapters.DEFAULT_RETRIES = 5
requests.packages.urllib3.disable_warnings()

# Charger les données depuis le fichier fournisseur.json
with open('fournisseur.json', 'r') as file:
    fournisseurs = json.load(file)

# Endpoint de l'API pour créer un fournisseur
url = 'http://localhost:5000/fournisseurs'

# Parcourir chaque fournisseur et envoyer les données à l'API
for fournisseur in fournisseurs:
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=fournisseur, headers=headers, proxies={'http': None, 'https': None})
    
    if response.status_code == 200:
        print('Fournisseur créé avec succès:', fournisseur['nom_fournisseur'])
    else:
        print('Erreur lors de la création du fournisseur:', fournisseur['nom_fournisseur'])
        print('Code d\'erreur:', response.status_code)
# Charger les données depuis le fichier visiteur.json
with open('visiteur.json', 'r') as file:
    visiteurs = json.load(file)

# Endpoint de l'API pour créer un visiteur
url = 'http://localhost:5000/visiteurs'

# Parcourir chaque visiteur et envoyer les données à l'API
for visiteur in visiteurs:
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=visiteur, headers=headers, proxies={'http': None, 'https': None})
    
    if response.status_code == 200:
        print('Visiteur créé avec succès:', visiteur['nom'])
    else:
        print('Erreur lors de la création du visiteur:', visiteur['nom'])
        print('Code d\'erreur:', response.status_code)
# Charger les données depuis le fichier automobiles.json
with open('automobile.json', 'r') as file:
    automobiles = json.load(file)

# Endpoint de l'API pour créer une automobile
url = 'http://localhost:5000/automobiles'

# Parcourir chaque automobile et envoyer les données à l'API
for automobile in automobiles:
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=automobile, headers=headers, proxies={'http': None, 'https': None})
    
    if response.status_code == 200:
        print('Automobile créée avec succès:', automobile['marque'])
    else:
        print('Erreur lors de la création de l\'automobile:', automobile['marque'])
        print('Code d\'erreur:', response.status_code)        
        