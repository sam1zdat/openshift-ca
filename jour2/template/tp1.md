# TP Jour 2 : Déploiement avancé et migration d'applications OpenShift

## Objectifs du TP
- Maîtriser la création et le déploiement de modèles multi-conteneurs complexes
- Configurer et gérer différentes stratégies de déploiement
- Mettre en place le monitoring des applications
- Intégrer des services externes et migrer des applications existantes vers OpenShift

## Prérequis
- Accès à un cluster OpenShift
- Outil CLI `oc` installé

## Durée estimée
3 heures

## Partie 1 : Création avancée d'applications à partir de modèles OpenShift

### 1.1 Création d'un modèle multi-conteneurs complet

1. Créez un nouveau projet :
   ```bash
   oc new-project tp3-templates-<votre-nom>
   ```

2. Créez un modèle pour une application à trois tiers (frontend, backend, base de données) :
   ```bash
   cat > three-tier-template.yaml << EOF
   apiVersion: template.openshift.io/v1
   kind: Template
   metadata:
     name: three-tier-app
     annotations:
       description: "Template for a three-tier application (frontend, backend, database)"
       tags: "quickstart,nodejs,java,postgresql"
   objects:
   # Secret pour la base de données
   - apiVersion: v1
     kind: Secret
     metadata:
       name: \${DATABASE_SERVICE_NAME}
     stringData:
       database-user: \${DATABASE_USER}
       database-password: \${DATABASE_PASSWORD}
       database-admin-password: \${DATABASE_ADMIN_PASSWORD}
   
   # Service et déploiement pour la base de données
   - apiVersion: v1
     kind: Service
     metadata:
       name: \${DATABASE_SERVICE_NAME}
     spec:
       ports:
       - name: postgresql
         port: 5432
       selector:
         name: \${DATABASE_SERVICE_NAME}
   - apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: \${DATABASE_SERVICE_NAME}
     spec:
       replicas: 1
       selector:
         matchLabels:
           name: \${DATABASE_SERVICE_NAME}
       template:
         metadata:
           labels:
             name: \${DATABASE_SERVICE_NAME}
         spec:
           containers:
           - name: postgresql
             image: postgres:13
             ports:
             - containerPort: 5432
             env:
             - name: POSTGRES_USER
               valueFrom:
                 secretKeyRef:
                   name: \${DATABASE_SERVICE_NAME}
                   key: database-user
             - name: POSTGRES_PASSWORD
               valueFrom:
                 secretKeyRef:
                   name: \${DATABASE_SERVICE_NAME}
                   key: database-password
             - name: POSTGRES_DB
               value: \${DATABASE_NAME}
             volumeMounts:
             - name: postgresql-data
               mountPath: /var/lib/postgresql/data
           volumes:
           - name: postgresql-data
             emptyDir: {}
   
   # Service et déploiement pour le backend
   - apiVersion: v1
     kind: Service
     metadata:
       name: \${BACKEND_SERVICE_NAME}
     spec:
       ports:
       - name: http
         port: 8080
       selector:
         name: \${BACKEND_SERVICE_NAME}
   - apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: \${BACKEND_SERVICE_NAME}
     spec:
       replicas: \${{BACKEND_REPLICAS}}
       selector:
         matchLabels:
           name: \${BACKEND_SERVICE_NAME}
       template:
         metadata:
           labels:
             name: \${BACKEND_SERVICE_NAME}
         spec:
           containers:
           - name: backend
             image: \${BACKEND_IMAGE}
             ports:
             - containerPort: 8080
             env:
             - name: DATABASE_SERVICE_NAME
               value: \${DATABASE_SERVICE_NAME}
             - name: DATABASE_USER
               valueFrom:
                 secretKeyRef:
                   name: \${DATABASE_SERVICE_NAME}
                   key: database-user
             - name: DATABASE_PASSWORD
               valueFrom:
                 secretKeyRef:
                   name: \${DATABASE_SERVICE_NAME}
                   key: database-password
             - name: DATABASE_NAME
               value: \${DATABASE_NAME}
             - name: DATABASE_PORT
               value: "5432"
             resources:
               limits:
                 memory: \${BACKEND_MEMORY_LIMIT}
                 cpu: \${BACKEND_CPU_LIMIT}
               requests:
                 memory: \${BACKEND_MEMORY_REQUEST}
                 cpu: \${BACKEND_CPU_REQUEST}
             readinessProbe:
               httpGet:
                 path: /health
                 port: 8080
               initialDelaySeconds: 15
               timeoutSeconds: 1
             livenessProbe:
               httpGet:
                 path: /health
                 port: 8080
               initialDelaySeconds: 30
               timeoutSeconds: 1
               periodSeconds: 10
               successThreshold: 1
               failureThreshold: 3
   
   # Service, route et déploiement pour le frontend
   - apiVersion: v1
     kind: Service
     metadata:
       name: \${FRONTEND_SERVICE_NAME}
     spec:
       ports:
       - name: http
         port: 8080
       selector:
         name: \${FRONTEND_SERVICE_NAME}
   - apiVersion: route.openshift.io/v1
     kind: Route
     metadata:
       name: \${FRONTEND_SERVICE_NAME}
     spec:
       host: \${APPLICATION_DOMAIN}
       to:
         kind: Service
         name: \${FRONTEND_SERVICE_NAME}
   - apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: \${FRONTEND_SERVICE_NAME}
     spec:
       replicas: \${FRONTEND_REPLICAS}
       selector:
         matchLabels:
           name: \${FRONTEND_SERVICE_NAME}
       template:
         metadata:
           labels:
             name: \${FRONTEND_SERVICE_NAME}
         spec:
           containers:
           - name: frontend
             image: \${FRONTEND_IMAGE}
             ports:
             - containerPort: 8080
             env:
             - name: BACKEND_URL
               value: http://\${BACKEND_SERVICE_NAME}:8080
             resources:
               limits:
                 memory: \${FRONTEND_MEMORY_LIMIT}
                 cpu: \${FRONTEND_CPU_LIMIT}
               requests:
                 memory: \${FRONTEND_MEMORY_REQUEST}
                 cpu: \${FRONTEND_CPU_REQUEST}
             readinessProbe:
               httpGet:
                 path: /
                 port: 8080
               initialDelaySeconds: 10
               timeoutSeconds: 1
             livenessProbe:
               httpGet:
                 path: /
                 port: 8080
               initialDelaySeconds: 30
               timeoutSeconds: 1
               periodSeconds: 10
               successThreshold: 1
               failureThreshold: 3
   
   # ConfigMap pour la configuration de l'application
   - apiVersion: v1
     kind: ConfigMap
     metadata:
       name: \${APP_CONFIG_MAP}
     data:
       app.properties: |
         environment=\${ENVIRONMENT}
         logging.level=\${LOGGING_LEVEL}
         feature.experimental=\${ENABLE_EXPERIMENTAL_FEATURES}
   
   parameters:
   # Paramètres généraux
   - name: ENVIRONMENT
     displayName: Environment
     description: Environment (dev, test, prod)
     required: true
     value: dev
   - name: APPLICATION_DOMAIN
     displayName: Application Domain
     description: The exposed hostname for the application
     value: ""
   - name: APP_CONFIG_MAP
     displayName: Application ConfigMap
     description: Name of the ConfigMap for application configuration
     required: true
     value: app-config
   
   # Paramètres de base de données
   - name: DATABASE_SERVICE_NAME
     displayName: Database Service Name
     description: The name of the PostgreSQL service
     required: true
     value: postgresql
   - name: DATABASE_USER
     displayName: PostgreSQL Username
     description: Username for PostgreSQL user
     required: true
     value: dbuser
   - name: DATABASE_PASSWORD
     displayName: PostgreSQL Password
     description: Password for the PostgreSQL user
     generate: expression
     from: "[a-zA-Z0-9]{16}"
   - name: DATABASE_ADMIN_PASSWORD
     displayName: PostgreSQL Admin Password
     description: Password for the PostgreSQL admin user
     generate: expression
     from: "[a-zA-Z0-9]{16}"
   - name: DATABASE_NAME
     displayName: Database Name
     description: Name of the PostgreSQL database
     required: true
     value: appdb
   
   # Paramètres du backend
   - name: BACKEND_SERVICE_NAME
     displayName: Backend Service Name
     description: Name of the backend service
     required: true
     value: backend
   - name: BACKEND_IMAGE
     displayName: Backend Image
     description: Backend Docker image to use
     required: true
     value: quay.io/redhattraining/do240-backend:latest
   - name: BACKEND_REPLICAS
     displayName: Backend Replicas
     description: Number of backend replicas
     required: true
     value: "2"
   - name: BACKEND_MEMORY_LIMIT
     displayName: Backend Memory Limit
     description: Maximum amount of memory the backend container can use
     required: true
     value: 512Mi
   - name: BACKEND_CPU_LIMIT
     displayName: Backend CPU Limit
     description: Maximum amount of CPU the backend container can use
     required: true
     value: 500m
   - name: BACKEND_MEMORY_REQUEST
     displayName: Backend Memory Request
     description: Requested amount of memory for the backend container
     required: true
     value: 256Mi
   - name: BACKEND_CPU_REQUEST
     displayName: Backend CPU Request
     description: Requested amount of CPU for the backend container
     required: true
     value: 200m
   
   # Paramètres du frontend
   - name: FRONTEND_SERVICE_NAME
     displayName: Frontend Service Name
     description: Name of the frontend service
     required: true
     value: frontend
   - name: FRONTEND_IMAGE
     displayName: Frontend Image
     description: Frontend Docker image to use
     required: true
     value: quay.io/redhattraining/do240-frontend:latest
   - name: FRONTEND_REPLICAS
     displayName: Frontend Replicas
     description: Number of frontend replicas
     required: true
     value: "2"
   - name: FRONTEND_MEMORY_LIMIT
     displayName: Frontend Memory Limit
     description: Maximum amount of memory the frontend container can use
     required: true
     value: 256Mi
   - name: FRONTEND_CPU_LIMIT
     displayName: Frontend CPU Limit
     description: Maximum amount of CPU the frontend container can use
     required: true
     value: 300m
   - name: FRONTEND_MEMORY_REQUEST
     displayName: Frontend Memory Request
     description: Requested amount of memory for the frontend container
     required: true
     value: 128Mi
   - name: FRONTEND_CPU_REQUEST
     displayName: Frontend CPU Request
     description: Requested amount of CPU for the frontend container
     required: true
     value: 100m
   
   # Paramètres de configuration
   - name: LOGGING_LEVEL
     displayName: Logging Level
     description: Logging level (INFO, DEBUG, WARN, ERROR)
     required: true
     value: INFO
   - name: ENABLE_EXPERIMENTAL_FEATURES
     displayName: Enable Experimental Features
     description: Enable experimental features (true/false)
     required: true
     value: "false"
   EOF
   
   oc create -f three-tier-template.yaml
   ```

### 1.2 Déploiement à partir du modèle complexe

1. Déployez une application à partir du modèle :
   ```bash
   oc new-app --template=three-tier-app \
     -p ENVIRONMENT=dev \
     -p BACKEND_REPLICAS=1 \
     -p FRONTEND_REPLICAS=1 \
     -p LOGGING_LEVEL=DEBUG
   ```

2. Vérifiez les ressources créées :
   ```bash
   oc get all
   oc get configmap
   oc get secret
   ```

### 1.3 Paramétrage pour différents environnements

1. Créez un fichier de paramètres pour l'environnement de production :
   ```bash
   cat > production-params.env << EOF
   ENVIRONMENT=production
   BACKEND_REPLICAS=3
   FRONTEND_REPLICAS=3
   BACKEND_MEMORY_LIMIT=1Gi
   BACKEND_CPU_LIMIT=1000m
   FRONTEND_MEMORY_LIMIT=512Mi
   FRONTEND_CPU_LIMIT=500m
   LOGGING_LEVEL=WARN
   ENABLE_EXPERIMENTAL_FEATURES=false
   EOF
   ```

2. Déployez une version de production dans un nouveau projet :
   ```bash
   oc new-project tp3-templates-prod-<votre-nom>
   ou
   oc delete all -l app=three-tier-app
   oc new-app --template=three-tier-app --param-file=production-params.env
   ou
   oc new-app --template=three-tier-app --param-file=production-params.env [--labels=app=env-prod]
   
   ```

## Partie 2 : Gestion de déploiement d'applications

### 2.1 Configuration des sondes de disponibilité

1. Créez un nouveau projet :
   ```bash
   oc new-project tp3-deployment-<votre-nom>
   ```

2. Déployez une application avec des sondes de disponibilité :
   ```bash
   cat > deployment-probes.yaml << EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-with-probes
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: app-with-probes
     template:
       metadata:
         labels:
           app: app-with-probes
       spec:
         containers:
         - name: app
           image: quay.io/redhattraining/hello-world-nginx:v1.0
           ports:
           - containerPort: 8080
           readinessProbe:
             httpGet:
               path: /
               port: 8080
             initialDelaySeconds: 5
             periodSeconds: 5
             timeoutSeconds: 1
             successThreshold: 1
             failureThreshold: 3
           livenessProbe:
             httpGet:
               path: /
               port: 8080
             initialDelaySeconds: 15
             periodSeconds: 20
             timeoutSeconds: 1
             successThreshold: 1
             failureThreshold: 3
           startupProbe:
             httpGet:
               path: /
               port: 8080
             initialDelaySeconds: 5
             periodSeconds: 5
             timeoutSeconds: 1
             successThreshold: 1
             failureThreshold: 30
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: app-with-probes
   spec:
     selector:
       app: app-with-probes
     ports:
     - port: 80
       targetPort: 8080
   ---
   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
     name: app-with-probes
   spec:
     to:
       kind: Service
       name: app-with-probes
   EOF
   
   oc create -f deployment-probes.yaml
   ```

3. Vérifiez l'état des pods et des sondes :
   ```bash
   oc get pods
   oc describe pod $(oc get pods -l app=app-with-probes -o name | head -1)
   ```

### 2.2 Mise en place d'une stratégie de déploiement Rolling

1. Créez un déploiement avec stratégie Rolling :
   ```bash
   cat > rolling-deployment.yaml << EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: rolling-app
   spec:
     replicas: 5
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1
         maxUnavailable: 1
     selector:
       matchLabels:
         app: rolling-app
     template:
       metadata:
         labels:
           app: rolling-app
       spec:
         containers:
         - name: app
           image: quay.io/redhattraining/hello-world-nginx:v1.0
           ports:
           - containerPort: 8080
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: rolling-app
   spec:
     selector:
       app: rolling-app
     ports:
     - port: 80
       targetPort: 8080
   ---
   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
     name: rolling-app
   spec:
     to:
       kind: Service
       name: rolling-app
   EOF
   
   oc create -f rolling-deployment.yaml
   ```

2. Effectuez une mise à jour de l'application :
   ```bash
   oc set image deployment/rolling-app app=quay.io/redhattraining/hello-world-nginx:v2.0
   ```

3. Observez le processus de déploiement :
   ```bash
   oc rollout status deployment/rolling-app
   ```

### 2.3 Mise en œuvre d'un déploiement Blue-Green

1. Déployez la version "blue" :
   ```bash
   cat > blue-deployment.yaml << EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-blue
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: app-blue
     template:
       metadata:
         labels:
           app: app-blue
           version: blue
       spec:
         containers:
         - name: app
           image: quay.io/redhattraining/hello-world-nginx:v1.0
           ports:
           - containerPort: 8080
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: app-blue
   spec:
     selector:
       app: app-blue
     ports:
     - port: 80
       targetPort: 8080
   EOF
   
   oc create -f blue-deployment.yaml
   ```

2. Créez une route pointant vers la version "blue" :
   ```bash
   cat > app-route.yaml << EOF
   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
     name: app
   spec:
     to:
       kind: Service
       name: app-blue
   EOF
   
   oc create -f app-route.yaml
   ```

3. Déployez la version "green" :
   ```bash
   cat > green-deployment.yaml << EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-green
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: app-green
     template:
       metadata:
         labels:
           app: app-green
           version: green
       spec:
         containers:
         - name: app
           image: quay.io/redhattraining/hello-world-nginx:v2.0
           ports:
           - containerPort: 8080
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: app-green
   spec:
     selector:
       app: app-green
     ports:
     - port: 80
       targetPort: 8080
   EOF
   
   oc create -f green-deployment.yaml
   ```

4. Basculez le trafic vers la version "green" :
   ```bash
   oc patch route/app -p '{"spec":{"to":{"name":"app-green"}}}'
   ```

5. Vérifiez que la route pointe maintenant vers la version "green" :
   ```bash
   oc describe route app
   ```
