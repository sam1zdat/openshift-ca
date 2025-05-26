# Quiz d'évaluation - Jour 2
## Formation RedHat OpenShift - Construction et personnalisation d'applications

**Nom :** ________________________

**Date :** ________________________

### Instructions
- Ce quiz comporte 20 questions
- Durée : 30 minutes
- Entourez la ou les bonnes réponses pour les questions à choix multiples
- Répondez brièvement aux questions ouvertes

---

### Questions à choix multiples

**1. Quel principe de conception recommande d'éviter la duplication de code ?**
   - A) KISS (Keep It Simple, Stupid)
   - **B) DRY (Don't Repeat Yourself)**
   - C) YAGNI (You Aren't Gonna Need It)
   - D) SoC (Separation of Concerns)

**2. Quel principe suggère de ne pas implémenter des fonctionnalités qui ne sont pas immédiatement nécessaires ?**
   - A) KISS (Keep It Simple, Stupid)
   - B) DRY (Don't Repeat Yourself)
   - **C) YAGNI (You Aren't Gonna Need It)**
   - D) SoC (Separation of Concerns)

**3. Quelle architecture est caractérisée par la décomposition d'une application en services autonomes et spécialisés ?**
   - A) Architecture monolithique
   - B) Architecture en couches
   - **C) Architecture microservices**
   - D) Architecture orientée événements

**4. Parmi les suivants, lequel n'est PAS un des 12 facteurs d'une application cloud-native ?**
   - A) Base de code unique
   - B) Dépendances explicites
   - **C) Interface graphique riche**
   - D) Processus sans état

**5. Quel type de build OpenShift utilise un Dockerfile pour construire une image ?**
   - A) Source-to-Image (S2I)
   - **B) Docker build**
   - C) Custom build
   - D) Pipeline build

**6. Quel type de build OpenShift construit une image directement à partir du code source ?**
   - **A) Source-to-Image (S2I)**
   - B) Docker build
   - C) Custom build
   - D) Pipeline build

**7. Quel déclencheur de build est activé lorsqu'une image de base est mise à jour ?**
   - A) Webhook
   - B) ConfigChange
   - **C) ImageChange**
   - D) Manual

**8. Quel script S2I est responsable de la construction de l'application ?**
   - A) run
   - **B) assemble**
   - C) build
   - D) compile

**9. Quel script S2I est exécuté pour démarrer l'application ?**
   - **A) run**
   - B) assemble
   - C) start
   - D) execute

**10. Quel script S2I optionnel permet de sauvegarder des artefacts entre les builds ?**
    - A) backup
    - B) save
    - **C) save-artifacts**
    - D) preserve

**11. Quelle ressource OpenShift permet de définir un ensemble de ressources paramétrables à déployer ensemble ?**
    - A) BuildConfig
    - B) DeploymentConfig
    - **C) Template**
    - D) ConfigMap

**12. Comment sont générées les valeurs aléatoires dans un modèle OpenShift ?**
    - A) Avec la fonction `random()`
    - **B) Avec l'expression `generate: expression`**
    - C) Avec la fonction `uuid()`
    - D) Avec l'annotation `openshift.io/generate-value`

**13. Quel pattern de déploiement multi-conteneurs utilise un conteneur auxiliaire pour des fonctions comme le logging ou le monitoring ?**
    - A) Ambassador
    - B) Adapter
    - **C) Sidecar**
    - D) Proxy

**14. Quelle commande permet de créer une nouvelle application à partir d'un modèle ?**
    - A) `oc process`
    - **B) `oc new-app`**
    - C) `oc create template`
    - D) `oc apply template`

**15. Quelle commande permet d'exporter un modèle existant ?**
    - A) `oc export template`
    - **B) `oc get template -o yaml`**
    - C) `oc describe template`
    - D) `oc template export`

---

### Questions ouvertes

**16. Expliquez la différence entre une architecture monolithique et une architecture microservices.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**17. Décrivez le processus de construction Source-to-Image (S2I) dans OpenShift.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**18. Quels sont les avantages de personnaliser une image S2I par rapport à l'utilisation d'une image standard ?**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**19. Expliquez comment les paramètres fonctionnent dans un modèle OpenShift et donnez des exemples de types de paramètres.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**20. Décrivez trois patterns de déploiement multi-conteneurs et leurs cas d'usage.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________
