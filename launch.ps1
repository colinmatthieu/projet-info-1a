#docker container first
docker container start FrigoDB
#FlaskServer
#cd ServerSide
start powershell {cd ServerSide; python FlaskServer.py}
#Watcher

cargo run --manifest-path FridgeSide/Cargo.toml
#Fake fridge (only if we say we want it)

