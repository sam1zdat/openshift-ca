## Exercice 6 : Publication d'images dans le registre OpenShift

**Objectif** : Apprendre à utiliser le registre intégré d'OpenShift.

**Durée** : 30 minutes

**Instructions** :

1. Exploration du registre intégré
   - Affichez les informations sur le registre intégré :
     ```bash
     oc get route -n openshift-image-registry
     ```
   - Si le registre n'est pas exposé, exposez-le (nécessite des droits d'administrateur) :
     ```bash
     oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"defaultRoute":true}}' --type=merge
     ```

2. Connexion au registre
   - Obtenez un jeton d'authentification :
     ```bash
     TOKEN=$(oc whoami -t)
     ```
   - Connectez-vous au registre avec podman ou docker :
     ```bash
     podman login -u $(oc whoami) -p $TOKEN <registry-route>
     ```

3. Push d'une image vers le registre
   - Taguez l'image construite précédemment :
     ```bash
     podman tag app-custom:latest <registry-route>/exercice-cli-<votre-nom>/app-custom:latest
     ```
   - Poussez l'image vers le registre :
     ```bash
     podman push <registry-route>/exercice-cli-<votre-nom>/app-custom:latest
     ```

4. Déploiement à partir du registre
   - Créez une nouvelle application à partir de l'image dans le registre :
     ```bash
     oc new-app --name=app-from-registry <registry-route>/exercice-cli-<votre-nom>/app-custom:latest
     oc expose service/app-from-registry
     ```

**Questions de réflexion** :
- Quels sont les avantages d'utiliser un registre privé par rapport à un registre public ?
- Comment le registre intégré d'OpenShift s'intègre-t-il avec les mécanismes de sécurité de la plateforme ?