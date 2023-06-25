# Fridger (todo: trouver nom)
Application de suivi et de notification de l'état des frigos de l'ens

## Requirements
Installer **influxdb-lient, flask, pytz et plotly** (avec pip install)

Sur linux: `chmod +x launch.sh linuxSetupDocker.sh` ("éventuellement a faire avec sudo)

## Setup avec script:
0) Lancer winSetupDocker.bat ou linuxSetupDocker.sh seulement pour initialiser l'image docker, cela lancera automatiquement le script launch
1) Quand le container docker a déjà été initialisé, lancer le script launch (bat ou sh selon l'os)
2) Il faut pour l'instant lancer le FakeFridge manuellement

**Info importante: si on détruit l'image docker, penser a supprimer le contenu du dossier influxDB_volume avant de relancer le script winSetupDocker (il attend automatiquement que le fichier de config soit créé avant de lancer launch)**


## Setup (ancien)
1) Installer docker et créer l'image influxDB: lancer le script setupDocker.sh (ou juste la commande) attendre quelques secondes puis aller dans le dossier config créé et recopier le tocken d'identification dans le code python du serveur
2) Lancer le ServerSide/FlaskServer.py (il doit être lançé depuis ce dossier !)
3) Lancer le watcher rust: FridgeSide/main.rs
4) Lancer le frigo de test: FakeFridge/generateDummyData.py
   

## Utilisation
1) Rien faire (attendre que des données soient update par les frigos)
2) Aller sur localhost:5000/dashboard pour voir l'historique des données de température de la journée

## TODO
- [ ] Améliorer ce readme
- [ ] Ajouter de la doc
- [x] Faire un script de nettoyage de la BD 
- [ ] Refactorer le code 
- [ ] Placer les éléments de configuration du serveur dans un fichier de configuration à part (qui devrait être lu par le watcher et le serveur au moins)
- [ ] Ajouter un protocole de communication watcher/serveur pour envoyer uniquement les lignes nécessaires
- [ ] Optimiser l'envoie des données du serveur a influxDB
- [ ] Gérer les différents types de données/mesures (prendre en compte que les données sont placées dans des dossiers journaliers)
- [ ] Détecter la non réception régulière des données pour envoyer une notif slack
- [ ] Designer et coder l'interface web 
- [ ] Débugguer le script de lancement sur Linux (ouvre qu'un seul terminal)