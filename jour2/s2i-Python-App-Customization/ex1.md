## Exercice : Personnalisation du processus S2I (Source-to-Image) dans OpenShift

**Objectif :**
Vous allez prendre une application Python Flask simple et personnaliser son processus de build S2I pour :
1.  Installer un paquetage supplémentaire au niveau du système d'exploitation (`figlet`) pendant le build.
2.  Afficher un message personnalisé pendant la phase `assemble`.
3.  Personnaliser le script `run` pour définir une variable d'environnement spécifique et afficher un message de démarrage personnalisé.

**Prérequis :**
*   Un cluster OpenShift où vous avez les permissions de créer des projets et de builder des applications (par ex., CodeReady Containers, Minishift, ou un cluster partagé).
*   L'outil CLI `oc` installé et configuré pour se connecter à votre cluster.
*   `git` installé.

**Application Scénario :**
Nous utiliserons une application Python Flask très simple.

---

**Étape 1 : Mettre en place votre projet et le code de l'application**

1.  **Créez un nouveau projet OpenShift :**
    ```bash
    oc new-project s2i-custom-exercice
    ```

2.  **Créez les fichiers de l'application localement :**
    Créez un répertoire nommé `my-python-app` :
    ```bash
    mkdir my-python-app
    cd my-python-app
    ```

3.  **`app.py` :**
    ```python
    # my-python-app/app.py
    from flask import Flask, os
    import subprocess

    app = Flask(__name__)

    @app.route('/')
    def hello():
        greeting = os.environ.get("CUSTOM_GREETING", "Hello") 
        figlet_output = "Figlet non disponible"
        try:
            # Essayer d'exécuter figlet s'il a été installé
            process = subprocess.run(['figlet', greeting], capture_output=True, text=True, check=True)
            figlet_output = f"<pre>{process.stdout}</pre>"
        except FileNotFoundError:
            figlet_output = f"<p>(Commande figlet non trouvée. A-t-elle été installée pendant le build ?)</p>"
        except subprocess.CalledProcessError as e:
            figlet_output = f"<p>Erreur Figlet : {e}</p>"

        return f"<h1>{greeting} depuis OpenShift !</h1>{figlet_output}"

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8080))
        print(f"----> App Flask personnalisée : Démarrage sur le port {port} avec le message d'accueil : {os.environ.get('CUSTOM_GREETING', 'Défaut')}")
        app.run(host='0.0.0.0', port=port)
    ```

4.  **`requirements.txt` :**
    ```
    # my-python-app/requirements.txt
    Flask
    ```

5.  **Initialisez un dépôt Git (S2I utilise souvent Git) :**
    ```bash
    git init
    git add .
    git commit -m "Première application flask simple"
    ```

---

**Étape 2 : Build initial (Comportement S2I par défaut)**

1.  **Créez l'application dans OpenShift en utilisant un builder S2I Python :**
    Nous utiliserons le répertoire courant (`.`) comme source.
    ```bash
    oc new-app python:3.9-ubi8~. --name=default-py-app
    ```
    (Ajustez `python:3.9-ubi8` si votre cluster a un tag d'image stream Python préféré différent, par ex., `python:latest` ou `python:3.8`)

2.  **Surveillez le build :**
    ```bash
    oc logs -f bc/default-py-app
    (soyez patient ...)
    ```
    Attendez qu'il se termine. Remarquez les logs de build standards.

3.  **Exposez le service et accédez-y :**
    ```bash
    oc expose svc/default-py-app
    oc get route default-py-app
    ```
    Accédez à l'application via l'URL de la route. Vous devriez voir "Hello depuis OpenShift !" et un message indiquant que figlet n'a pas été trouvé.

4.  **Vérifiez les logs d'exécution :**
    ```bash
    oc logs dc/default-py-app
    ```
    Vous verrez les messages de démarrage par défaut de l'image S2I Python.

---

**Étape 3 : Personnalisation du script `assemble`**

Le script `assemble` est responsable du build de votre application. Nous allons le surcharger pour installer `figlet` et ajouter un message personnalisé.

1.  **Créez le répertoire des scripts S2I personnalisés :**
    ```bash
    mkdir -p .s2i/bin
    ```

2.  **Créez un script `assemble` personnalisé (`.s2i/bin/assemble`) :**
    ```bash
    # my-python-app/.s2i/bin/assemble
    #!/bin/bash

    echo "----> Démarrage du script ASSEMBLE PERSONNALISÉ !"

    # Tentative d'installation de figlet (nécessite root, que les images UBI fournissent souvent pendant le build)
    echo "----> Tentative d'installation de figlet..."
    if command -v yum &> /dev/null; then
        yum install -y figlet
    elif command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y figlet
    else
        echo "----> ATTENTION : Impossible de déterminer le gestionnaire de paquets pour installer figlet."
    fi
    echo "----> Tentative d'installation de Figlet terminée."

    echo "----> Appel du script assemble du builder S2I par défaut..."
    # Ceci est important ! Nous voulons étendre, et non remplacer complètement, le build par défaut.
    # Le chemin /usr/libexec/s2i/assemble est courant pour les builders S2I officiels.
    exec /usr/libexec/s2i/assemble
    ```
    *   **Important :** La ligne `exec /usr/libexec/s2i/assemble` appelle le script `assemble` original du builder. Sans cela, vous seriez responsable de *toutes* les étapes de build (comme l'installation de `requirements.txt`).

3.  **Rendez le script exécutable :**
    ```bash
    chmod +x .s2i/bin/assemble
    ```

4.  **Commitez les changements :**
    ```bash
    git add .s2i/bin/assemble
    git commit -m "Ajout du script assemble personnalisé pour installer figlet"
    ```

---

**Étape 4 : Personnalisation du script `run`**

Le script `run` est responsable du démarrage de votre application.

1.  **Créez un script `run` personnalisé (`.s2i/bin/run`) :**
    ```bash
    # my-python-app/.s2i/bin/run
    #!/bin/bash

    echo "----> Démarrage du script RUN PERSONNALISÉ !"

    # Définir une variable d'environnement personnalisée
    export CUSTOM_GREETING="Salut Personnalisation S2I"
    echo "----> CUSTOM_GREETING défini à : ${CUSTOM_GREETING}"

    echo "----> Appel du script run du builder S2I par défaut..."
    # Ceci appelle le script run S2I original.
    # Alternativement, vous pourriez directement exécuter votre application :
    # exec python app.py
    # Mais utiliser celui par défaut permet toute autre configuration que l'image S2I effectue.
    exec /usr/libexec/s2i/run
    ```

2.  **Rendez le script exécutable :**
    ```bash
    chmod +x .s2i/bin/run
    ```

3.  **Commitez les changements :**
    ```bash
    git add .s2i/bin/run
    git commit -m "Ajout du script run personnalisé avec variable d'env"
    ```

---

**Étape 5 : Builder et déployer l'application personnalisée**

1.  **Créez une nouvelle application pour la version personnalisée (ou déclenchez un nouveau build pour l'existante) :**
    Créons-en une nouvelle pour comparer.
    ```bash
    oc new-app python:3.9-ubi8~. --name=custom-py-app
    ```

2.  **Surveillez les logs de build :**
    ```bash
    oc logs -f bc/custom-py-app
    ```
    Vous devriez voir :
    *   "----> Démarrage du script ASSEMBLE PERSONNALISÉ !"
    *   Logs relatifs à l'installation de `figlet`.
    *   Puis les logs de build S2I Python standards (parce que nous avons appelé le script `assemble` original).

3.  **Une fois le build terminé, exposez le service :**
    ```bash
    oc expose svc/custom-py-app
    oc get route custom-py-app
    ```

4.  **Vérifiez les logs d'exécution :**
    ```bash
    oc logs dc/custom-py-app
    ```
    Vous devriez voir :
    *   "----> Démarrage du script RUN PERSONNALISÉ !"
    *   "----> CUSTOM_GREETING défini à : Salut Personnalisation S2I"
    *   Le message de démarrage personnalisé de `app.py` reflétant maintenant "Salut Personnalisation S2I".

5.  **Accédez à l'application :**
    Ouvrez l'URL de la route pour `custom-py-app` dans votre navigateur.
    Vous devriez voir :
    *   "Salut Personnalisation S2I depuis OpenShift !"
    *   Le mot "Salut" rendu en grand art ASCII par `figlet`.

---

**Étape 6 : (Optionnel) Utilisation du fichier `.s2i/environment`**

Pour des configurations simples de variables d'environnement pendant le temps de build, vous pouvez utiliser un fichier `.s2i/environment`. Ceci est traité par les scripts S2I par défaut.

1.  **Créez `.s2i/environment` :**
    ```
    # my-python-app/.s2i/environment
    BUILD_LOG_LEVEL=5
    MY_BUILD_TIME_INFO="Ceci est défini pendant le build par .s2i/environment"
    ```
    `BUILD_LOG_LEVEL` est un exemple de variable que le builder S2I Python pourrait reconnaître. `MY_BUILD_TIME_INFO` est une variable personnalisée.

2.  **Modifiez `.s2i/bin/assemble` pour afficher cette variable :**
    Ajoutez cette ligne au début de votre script `assemble` personnalisé :
    ```bash
    echo "----> MY_BUILD_TIME_INFO de .s2i/environment : ${MY_BUILD_TIME_INFO}"
    ```

3.  **Commitez et rebuildez :**
    ```bash
    git add .s2i/environment .s2i/bin/assemble
    git commit -m "Test du fichier .s2i/environment"
    oc start-build custom-py-app --from-dir=. --wait
    ```
    Vérifiez les logs de build (`oc logs -f bc/custom-py-app`) pour voir la valeur de `MY_BUILD_TIME_INFO` affichée.

---

**Nettoyage :**
```bash
oc delete project s2i-custom-exercice
```

**Concepts Clés Démontrés :**

*   **Scripts S2I :** `assemble` (pour le build) et `run` (pour l'exécution).
*   **Répertoire `.s2i/bin` :** L'emplacement où S2I recherche les scripts personnalisés.
*   **Permissions d'exécution :** Les scripts S2I *doivent* être exécutables.
*   **Étendre vs. Remplacer :** En appelant les scripts S2I originaux (par ex., `exec /usr/libexec/s2i/assemble`), vous étendez leurs fonctionnalités. Si vous omettez cela, vous les remplacez complètement et êtes responsable de toute la logique.
*   **Personnalisation au moment du build vs. à l'exécution :** `assemble` personnalise la création de l'image ; `run` personnalise le démarrage du conteneur.
*   **`.s2i/environment` :** Un moyen simple de passer des variables d'environnement au processus de build.

Cet exercice fournit une base solide pour des personnalisations S2I plus avancées !