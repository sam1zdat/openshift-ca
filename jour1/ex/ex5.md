## Exercice 5 : Construction d'une image pour une application

**Objectif** : Créer une image de conteneur personnalisée à partir d'un Dockerfile.

**Durée** : 45 minutes

**Instructions** :

1. Création d'une application simple
   - Créez un répertoire pour votre application :
     ```bash
     mkdir -p ~/app-custom
     cd ~/app-custom
     ```
   - Créez un fichier index.html :
     ```bash
     cat > index.html << EOF
        <!DOCTYPE html>
        <html>
        <head>
            <title>Application personnalisée</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #336699; }
            </style>
        </head>
        <body>
            <h1>Mon application personnalisée sur OpenShift</h1>
            <p>Cette application a été déployée à partir d'une image personnalisée.</p>
            <p>Date de déploiement : $(date)</p>
        </body>
        </html>
        EOF
     ```

2. Création d'un Dockerfile
   - Créez un fichier Dockerfile :
     ```bash
     cat > Dockerfile << EOF
        FROM nginx:alpine

        # Copie ta page HTML dans le répertoire par défaut de NGINX
        COPY index.html /usr/share/nginx/html/index.html

        # Expose le port HTTP
        EXPOSE 80

        # Commande pour lancer NGINX au premier plan
        CMD ["nginx", "-g", "daemon off;"]
        EOF
     ```

1. Construction de l'image avec OpenShift
   - Créez une nouvelle application à partir du Dockerfile :
     ```bash
     oc project exercice-cli-<votre-nom>
     oc new-build --name=app-custom --binary=true
     ```
### ✅ Explication de ta commande :
* Crée un **BuildConfig** nommé `app-custom`
* Attend que tu lui **envoies les sources manuellement** (fichiers locaux)
* Utilisera un `Dockerfile` dans ton répertoire local

---
## 🚀 Étapes suivantes

### ✅ Démarrer le build avec les fichiers locaux :

Dans le dossier contenant `Dockerfile` et `index.html`, exécute :

```bash
oc start-build app-custom --from-dir=. --follow
```

> Cela envoie tous les fichiers dans le répertoire courant à OpenShift, et suit le build en direct.

---

### 🧪 Vérifie l'image créée :

```bash
oc get builds
oc logs build/app-custom-1
```
---

### ✅ Déployer ton image 

### 🌍 Exposer l’application via une route :

2. Déploiement de l'application
   - Créez un déploiement à partir de l'image construite :
     ```bash
     oc new-app --name=app-custom-deploy app-custom
     oc expose service/app-custom-deploy
     ```
   - Vérifiez l'URL de l'application :
     ```bash
     oc get route app-custom-deploy
     ```
   - Accédez à l'application dans votre navigateur

**Questions de réflexion** :
- Quels sont les avantages de construire des images directement dans OpenShift plutôt que de les construire localement ?
- Comment pourriez-vous améliorer ce Dockerfile pour le rendre plus sécurisé et optimisé ?