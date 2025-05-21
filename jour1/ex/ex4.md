## Exercice 4 : Configuration des déploiements

**Objectif** : Apprendre à configurer les déploiements avec des variables d'environnement et des limites de ressources.

**Durée** : 30 minutes

**Instructions** :

1. Déployez une application à partir d'une image :
     ```bash
     oc new-app --name=nginx-cli registry.access.redhat.com/rhscl/nginx-114-rhel7
     ```
2. Ajout de variables d'environnement
   - Modifiez le déploiement nginx-cli :
     ```bash
     oc set env deployment/nginx-cli NGINX_HOST=www.exemple.com NGINX_PORT=80
     ```
   - Vérifiez que les variables ont été ajoutées :
     ```bash
     oc describe deployment nginx-cli
     ```

2. Configuration des limites de ressources
   - Définissez des limites de ressources pour le déploiement :
     ```bash
     oc set resources deployment/nginx-cli --limits=cpu=200m,memory=256Mi --requests=cpu=100m,memory=128Mi
     ```
   - Vérifiez les limites configurées :
     ```bash
     oc describe deployment nginx-cli
     ```

3. Scaling manuel de l'application
   - Augmentez le nombre de réplicas :
     ```bash
     oc scale deployment/nginx-cli --replicas=3
     ```
   - Vérifiez que les pods supplémentaires sont créés :
     ```bash
     oc get pods
     ```

4. Configuration d'un autoscaler
   - Créez un autoscaler pour le déploiement :
     ```bash
     oc autoscale deployment/nginx-cli --min=2 --max=5 --cpu-percent=80
     ```
   - Vérifiez la configuration de l'autoscaler :
     ```bash
     oc get hpa
     ```

**Questions de réflexion** :
- Pourquoi est-il important de définir des limites de ressources pour les applications ?
- Dans quels cas l'autoscaling est-il particulièrement utile ?