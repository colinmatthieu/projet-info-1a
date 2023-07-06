#docker container first
docker container start FrigoDB
docker container start grafana
#FlaskServer
#cd ServerSide
start powershell {cd ServerSide; python FlaskServer.py}
#Watcher

cargo run --manifest-path FridgeSide/Cargo.toml
#Fake fridge (only if we say we want it)

