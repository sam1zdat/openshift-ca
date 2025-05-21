## Exercice 2 : Création et gestion de projets

**Objectif** : Apprendre à créer et gérer des projets OpenShift.

**Durée** : 20 minutes

**Instructions** :

1. Création d'un projet via l'interface web
   - Dans la console web, cliquez sur "Create Project"
   - Nommez votre projet "exercice-web-<votre-nom>"
   - Ajoutez une description et des labels

2. Création d'un projet via la ligne de commande
   - Ouvrez un terminal
   - Créez un nouveau projet :
     ```bash
     oc new-project exercice-cli-<votre-nom> --display-name="Exercice CLI <Votre Nom>" --description="Projet créé via CLI"
     ```

3. Gestion des projets
   - Listez tous vos projets :
     ```bash
     oc projects
     ```
   - Basculez entre les projets :
     ```bash
     oc project <project-number-1>
     oc project <project-number-2>
     ```
   - Examinez les détails d'un projet :
     ```bash
     oc describe project <project-name>
     ```

4. Ajout d'utilisateurs à un projet
   - Ajoutez un autre participant en tant qu'éditeur :
     ```bash
     oc policy add-role-to-user edit <autre-participant> -n exercice-cli-<votre-nom>
     ```
   - Vérifiez les rôles attribués :
     ```bash
     oc get rolebindings -n exercice-cli-<votre-nom>
     ```

**Questions de réflexion** :
- Pourquoi est-il important de bien organiser ses projets dans OpenShift ?
- Comment les rôles et les autorisations contribuent-ils à la sécurité dans un environnement multi-utilisateurs ?