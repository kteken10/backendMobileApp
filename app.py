from flask import Flask

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir une route pour la page d'accueil
@app.route('/')
def home():
    return "Hello, Flask!"

# Exécuter l'application Flask lorsque ce fichier est exécuté
if __name__ == '__main__':
    app.run()
