# Quiz d'évaluation - Jour 1
## Formation RedHat OpenShift - Fondamentaux et déploiement d'applications

**Nom :** ________________________

**Date :** ________________________

### Instructions
- Ce quiz comporte 20 questions
- Durée : 30 minutes
- Entourez la ou les bonnes réponses pour les questions à choix multiples
- Répondez brièvement aux questions ouvertes

---

### Questions à choix multiples

**1. Qu'est-ce qu'OpenShift Container Platform ?**
   - A) Un système d'exploitation Linux
   - **B) Une plateforme d'applications conteneurisées basée sur Kubernetes**
   - C) Un logiciel de virtualisation
   - D) Un service de stockage cloud

**2. Quelle est la relation entre Kubernetes et OpenShift ?**
   - **A) OpenShift est une distribution de Kubernetes avec des fonctionnalités supplémentaires**
   - B) Kubernetes est une version commerciale d'OpenShift
   - C) OpenShift et Kubernetes sont des produits concurrents sans relation
   - D) OpenShift remplace complètement Kubernetes

**3. Quel composant est responsable du stockage des données de configuration dans OpenShift ?**
   - A) CRI-O
   - **B) Etcd**
   - C) SDN
   - D) Router

**4. Quelle commande permet de créer un nouveau projet dans OpenShift via la ligne de commande ?**
   - A) `oc create project`
   - **B) `oc new-project`**
   - C) `oc add project`
   - D) `oc make project`

**5. Quelle ressource OpenShift permet d'exposer un service à l'extérieur du cluster ?**
   - A) Deployment
   - B) Pod
   - **C) Route**
   - D) ConfigMap

**6. Quelle commande permet de déployer une application à partir d'une image existante ?**
   - A) `oc deploy`
   - B) `oc create app`
   - **C) `oc new-app`**
   - D) `oc start-app`

**7. Comment peut-on visualiser les logs d'un pod dans OpenShift ?**
   - A) `oc get logs`
   - **B) `oc logs`**
   - C) `oc show logs`
   - D) `oc view logs`

**8. Quelle instruction dans un Dockerfile définit l'image de base à utiliser ?**
   - A) `BASE`
   - **B) `FROM`**
   - C) `IMAGE`
   - D) `USING`

**9. Quelle est la meilleure pratique pour réduire la taille d'une image de conteneur ?**
   - A) `Utiliser une image de base complète avec tous les outils possibles`
   - B) Installer tous les packages de développement
   - **C) Nettoyer les caches après installation des packages**
   - D) Conserver tous les fichiers temporaires

**10. Quel est l'avantage principal d'un multi-stage build dans un Dockerfile ?**
    - A) Il permet d'utiliser plusieurs langages de programmation
    - **B) Il réduit la taille de l'image finale en séparant les étapes de build et d'exécution**
    - C) Il accélère le processus de build
    - D) Il permet de déployer sur plusieurs clusters simultanément

**11. Quelle commande permet de créer un build dans OpenShift à partir de fichiers locaux ?**
    - A) `oc build`
    - **B) `oc new-build`**
    - **C) `oc start-build`**
    - D) `oc create build`

**12. Quelle est l'URL typique du registre intégré d'OpenShift ?**
    - A) `docker.io`
    - B) `quay.io`
    - **C) `image-registry.openshift-image-registry.svc:5000`**
    - D) `registry.access.redhat.com`

**13. Quel rôle permet à un utilisateur de pousser des images vers le registre OpenShift ?**
    - A) `registry-viewer`
    - **B) `registry-editor`**
    - C) `registry-admin`
    - D) `registry-pusher`

**14. Comment définit-on des limites de ressources pour un déploiement dans OpenShift ?**
    - A) `oc limit resources`
    - B) `oc set quota`
    - **C) `oc set resources`**
    - D) `oc apply limits`

**15. Quelle commande permet d'augmenter le nombre de réplicas d'un déploiement ?**
    - A) `oc replicate`
    - **B) `oc scale`**
    - C) `oc increase`
    - D) `oc expand`

---

### Questions ouvertes

**16. Expliquez la différence entre une image de conteneur et un conteneur.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**17. Décrivez au moins trois bonnes pratiques pour la création d'images de conteneurs sécurisées.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**18. Expliquez comment fonctionne l'autoscaling dans OpenShift et quels métriques peuvent être utilisées pour le déclencher.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**19. Décrivez le processus de déploiement d'une application dans OpenShift, de la création de l'image à l'exposition du service.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**20. Quels sont les avantages d'utiliser un registre privé par rapport à un registre public pour stocker vos images de conteneurs ?**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________
