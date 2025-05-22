# my-python-app/app.py
import os
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    greeting = os.environ.get("CUSTOM_GREETING", "Hello")  # Bonjour en français : "Salut"
    figlet_output = "Figlet non disponible"
    try:
        # Essayer d'exécuter figlet s'il a été installé
        process = subprocess.run(['figlet', greeting], capture_output=True, text=True, check=True)
        figlet_output = f"<pre>{process.stdout}</pre>"
    except FileNotFoundError:
        figlet_output = "<p>(Commande figlet non trouvée. A-t-elle été installée pendant le build ?)</p>"
    except subprocess.CalledProcessError as e:
        figlet_output = f"<p>Erreur Figlet : {e}</p>"

    return f"<h1>{greeting} depuis OpenShift !</h1>{figlet_output}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"----> App Flask personnalisée : Démarrage sur le port {port} avec le message d'accueil : {os.environ.get('CUSTOM_GREETING', 'Défaut')}")
    app.run(host='0.0.0.0', port=port)