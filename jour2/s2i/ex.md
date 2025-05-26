 **Créer une image S2I Node.js personnalisée et l’utiliser pour builder une application depuis un dépôt GitHub.**

---

### ✅ 1. Préparer la structure de l’image S2I Node.js custom

```bash
mkdir -p custom-nodejs-s2i/.s2i/bin
cd custom-nodejs-s2i
```

Créer un fichier `Dockerfile` :

```Dockerfile
FROM registry.access.redhat.com/ubi8/nodejs-14

LABEL io.k8s.description="Custom Node.js S2I builder with additional tools" \
      io.k8s.display-name="Node.js 14 Custom S2I builder" \
      io.openshift.s2i.scripts-url="image:///usr/libexec/s2i"

USER root
RUN dnf install -y git wget curl && \
    mv /usr/libexec/s2i/assemble /usr/libexec/s2i/assemble.original && \
    mv /usr/libexec/s2i/run /usr/libexec/s2i/run.original && \
    dnf clean all

COPY .s2i/bin/ /usr/libexec/s2i/
RUN chmod +x /usr/libexec/s2i/*
RUN echo 'hello'
USER 1001
CMD ["/usr/libexec/s2i/usage"]
```

---

Créer les scripts `.s2i/bin/assemble` et `.s2i/bin/run` :

**assemble** :

```bash
#!/bin/bash
set -e
echo "-----> Custom assemble script"

if [ -x /usr/libexec/s2i/assemble.original ]; then
    /usr/libexec/s2i/assemble.original
fi

echo "-----> Installing dev dependencies"
npm install --production=false

echo "✅ Assemble complete"
```

**run** :

```bash
#!/bin/bash
echo "-----> Custom run script"
export NODE_ENV=production

if [ -x /usr/libexec/s2i/run.original ]; then
    exec /usr/libexec/s2i/run.original
fi
```

Rendre les scripts exécutables :

```bash
chmod +x .s2i/bin/*
```

---

### ✅ 2. Créer l’image builder dans OpenShift

```bash
oc new-build --name=custom-nodejs-s2i --binary
oc start-build custom-nodejs-s2i --from-dir=. --follow
```

---

### ✅ 3. Utiliser cette image pour builder une app GitHub

```bash
oc new-app custom-nodejs-s2i~https://github.com/sam1zdat/sample-node-app.git --name=my-node-app
```

---

### ✅ 4. Exposer l’application

```bash
oc expose service my-node-app
```

---

### ✅ 5. Tester dans le navigateur

```bash
oc get route my-node-app
```

Ouvre l’URL indiquée 🎉

---