FROM nginx:alpine

# Copie ta page HTML dans le répertoire par défaut de NGINX
COPY index.html /usr/share/nginx/html/index.html

# Expose le port HTTP
EXPOSE 80

# Commande pour lancer NGINX au premier plan
CMD ["nginx", "-g", "daemon off;"]
