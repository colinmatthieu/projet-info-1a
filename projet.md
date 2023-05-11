# Fridger (todo: trouver nom)
Application de suivi et de notification de l'état des frigos de l'ens

## Setup
1) Installer docker et créer l'image influxDB: lancer le script setupDocker.sh (ou juste la commande) attendre quelques secondes puis aller dans le dossier config créé et recopier le tocken d'identification dans le code python du serveur
2) Lancer le ServerSide/FlaskServer.py (il doit être lançé depuis ce dossier !)
3) Lancer le watcher rust: FridgeSide/main.rs
4) Lancer le frigo de test: FakeFridge/generateDummyData.py
   
### Todo: faire script qui se charge de lancer tout ça ^ automatiquement 

## Utilisation
1) Rien faire (attendre que des données soient update par les frigos)
2) Aller sur localhost:5000/getData/d pour voir l'historique des données de température de la journée