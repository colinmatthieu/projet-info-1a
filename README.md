# FridgeWatcher
Application de suivi et de notification de l'état des frigos de l'ens

## Requirements
Installer **influxdb-client, flask et plotly** (avec pip install)
Installer également **flask_login et flask_sqlalchemy**


Sur linux: `chmod +x launch.sh linuxSetupDocker.sh` ("éventuellement a faire avec sudo)

## Setup avec script:
0) Lancer winSetupDocker.bat ou linuxSetupDocker.sh seulement pour initialiser l'image docker, cela lancera automatiquement le script launch
1) Quand le container docker a déjà été initialisé, lancer le script launch (bat ou sh selon l'os)
2) Il faut pour l'instant lancer le FakeFridge manuellement

**Info importante: si on détruit l'image Docker, penser a supprimer le contenu du dossier influxDB_volume (le volume Docker) avant de relancer le script winSetupDocker (il attend automatiquement que le fichier de config soit créé avant de lancer launch)**

## Setup Grafana
Mêmes manipulations que pour le reste, mais il faut en plus
- créer un réseau Docker : <br>`docker network create nom-du-reseau`
- lancer un container depuis l'image Grafana : <br>`docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss:10.0.0` pour la version 10.0.0 par exemple
- Attacher les containers InfluxDB et Grafana au réseau Docker pour qu'ils puissent communiquer entre eux : <br>
`docker network connect nom-du-reseau grafana`
<br>
`docker network connect nom-du-reseau FrigoDB`

## Setup Grafana
Mêmes manipulations que pour le reste, mais il faut en plus
- créer un réseau Docker : <br>`docker network create nom-du-reseau`
- lancer un container depuis l'image Grafana : <br>`docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss:10.0.0` pour la version 10.0.0 par exemple
- Attacher les containers InfluxDB et Grafana au réseau Docker pour qu'ils puissent communiquer entre eux : <br>
`docker network connect nom-du-reseau grafana`
<br>
`docker network connect nom-du-reseau FrigoDB`

## Pour utiliser grafanalib
Après avoir installé grafanalib, il faut créer un fichier .env dans le dossier ServerSide/dashboard-generation et mettre à l'intérieur :
```
GRAFANA_API_KEY = une-clé-api-grafana-avec-droits-d-edition-préalablement-générée
GRAFANA_SERVER = localhost:3000
```

Pour créer une clé api Grafana, il suffit de se connecter en admin puis d'aller dans l'onglet Administration, Service Accounts, créer un service account.

## Setup (ancien)
1) Installer docker et créer l'image influxDB: lancer le script setupDocker.sh (ou juste la commande) attendre quelques secondes puis aller dans le dossier config créé et recopier le tocken d'identification dans le code python du serveur
2) Lancer le ServerSide/FlaskServer.py (il doit être lançé depuis ce dossier !)
3) Lancer le watcher rust: FridgeSide/main.rs
4) Lancer le frigo de test: FakeFridge/generateDummyData.py


## Utilisation (sans Grafana)
1) Ne rien faire (attendre que des données soient update par les frigos)
2) Aller sur `localhost:5000/dashboard` pour voir l'historique des données de température de la journée

## Fonctionnement de [Tauri](https://tauri.app/) dans ce projet

### Prérequis
- Avoir [node.js](https://nodejs.org) et [Rust](https://www.rust-lang.org) installé sur sa machine.
### Développement
- Aller dans le dossier `tauri/fridgewatcher` puis lancer `npm run tauri dev`.
- L'application Tauri va alors se lancer

Le code source Rust se situe dans le dossier `src-tauri`, le frontend dans le dossier `src`.

Piste de travail : utiliser le logger en tant que binaire externe (cf [cette page](https://tauri.app/v1/guides/building/sidecar/))

## TODO
- [ ] Améliorer ce readme
- [ ] Ajouter de la doc
- [x] Faire un script de nettoyage de la BD 
- [ ] Refactorer le code
- [ ] Placer les éléments de configuration du serveur dans un fichier de configuration à part (qui devrait être lu par le watcher et le serveur au moins)
- [x] Ajouter un protocole de communication watcher/serveur pour envoyer uniquement les lignes nécessaires
- [ ] Optimiser l'envoie des données du serveur a influxDB
- [x] Gérer les différents types de données/mesures (prendre en compte que les données sont placées dans des dossiers journaliers)
- [ ] Détecter la non réception régulière des données pour envoyer une notif slack
- [ ] Designer et coder l'interface web 
- [ ] Débugguer le script de lancement sur Linux (ouvre qu'un seul terminal)
- [ ] Ajouter un système de comptes pour les différentes équipes
- [ ] Créer un script/Dockerfile pour la procédure de déploiement de tous les services (InfluxDB, comptes, serveur Flask)