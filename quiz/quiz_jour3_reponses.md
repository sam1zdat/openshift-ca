# Quiz d'évaluation - Jour 3
## Formation RedHat OpenShift - Déploiement avancé et migration d'applications

**Nom :** ________________________

**Date :** ________________________

### Instructions
- Ce quiz comporte 20 questions
- Durée : 30 minutes
- Entourez la ou les bonnes réponses pour les questions à choix multiples
- Répondez brièvement aux questions ouvertes

---

### Questions à choix multiples

**1. Quelle sonde vérifie si un conteneur est prêt à servir du trafic ?**
   - A) Liveness probe
   - **B) Readiness probe**
   - C) Startup probe
   - D) Health probe

**2. Quelle sonde vérifie si un conteneur est en vie et doit être redémarré s'il ne répond pas ?**
   - **A) Liveness probe**
   - B) Readiness probe
   - C) Startup probe
   - D) Health probe

**3. Quelle sonde, introduite dans Kubernetes 1.16, permet de gérer le démarrage initial des applications à démarrage lent ?**
   - A) Liveness probe
   - B) Readiness probe
   - **C) Startup probe**
   - D) Health probe

**4. Quelle stratégie de déploiement met à jour les pods progressivement, par lots ?**
   - A) Recreate
   - **B) Rolling**
   - C) Blue-Green
   - D) Canary

**5. Quelle stratégie de déploiement arrête tous les pods existants avant d'en créer de nouveaux ?**
   - **A) Recreate**
   - B) Rolling
   - C) Blue-Green
   - D) Canary

**6. Quelle stratégie de déploiement maintient deux environnements identiques en parallèle ?**
   - A) Recreate
   - B) Rolling
   - **C) Blue-Green**
   - D) Canary

**7. Quel type de service OpenShift crée un alias DNS pour un service externe ?**
   - A) ClusterIP
   - B) NodePort
   - C) LoadBalancer
   - **D) ExternalName**

**8. Comment peut-on intégrer un service externe avec une IP fixe dans OpenShift ?**
   - A) En utilisant un Service ExternalName
   - **B) En utilisant un Service avec Endpoints manuels**
   - C) En utilisant un Ingress
   - D) En utilisant un NetworkPolicy

**9. Quelle ressource OpenShift permet de configurer l'autoscaling horizontal basé sur l'utilisation CPU ?**
   - A) AutoScaler
   - **B) HorizontalPodAutoscaler**
   - C) VerticalPodAutoscaler
   - D) ScalingPolicy

**10. Quel outil est intégré à OpenShift pour la collecte de métriques ?**
    - A) Grafana
    - **B) Prometheus**
    - C) Elasticsearch
    - D) Jaeger

**11. Quelle variable d'environnement est typiquement utilisée pour configurer une datasource JNDI dans JBoss EAP sur OpenShift ?**
    - **A) DB_JNDI**
    - B) DATASOURCE_JNDI
    - C) JNDI_NAME
    - D) EAP_JNDI

**12. Quelle ressource Kubernetes est utilisée pour stocker des données de configuration non sensibles ?**
    - A) Secret
    - **B) ConfigMap**
    - C) PersistentVolume
    - D) ServiceAccount

**13. Quelle ressource Kubernetes est utilisée pour stocker des données sensibles comme des mots de passe ?**
    - **A) Secret**
    - B) ConfigMap
    - C) PersistentVolume
    - D) ServiceAccount

**14. Quelle commande permet de configurer l'autoscaling pour un déploiement ?**
    - A) `oc scale`
    - **B) `oc autoscale`**
    - C) `oc set autoscaler`
    - D) `oc create hpa`

**15. Quelle fonctionnalité permet de spécifier sur quels nœuds un pod doit être planifié ?**
    - A) Taints et Tolerations
    - B) Node Selector
    - C) Pod Affinity
    - **D) Toutes les réponses ci-dessus**

---

### Questions ouvertes

**16. Expliquez les différences entre les stratégies de déploiement Rolling et Blue-Green, et dans quels cas utiliser chacune.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**17. Décrivez les différentes méthodes pour intégrer des services externes dans OpenShift et leurs cas d'usage.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**18. Expliquez comment configurer et utiliser les sondes de disponibilité (probes) dans OpenShift et pourquoi elles sont importantes.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**19. Quels sont les défis spécifiques à la migration d'applications traditionnelles vers OpenShift et comment les surmonter ?**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**20. Décrivez une checklist des éléments à vérifier avant de mettre une application OpenShift en production.**

Réponse : ___________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________
