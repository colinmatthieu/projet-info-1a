echo off
rem docker container first
docker container start FrigoDB
rem FlaskServer
rem cd ServerSide
start powershell -command "cd ServerSide;set FLASK_DEBUG=1; flask --app . run; Read-Host"
rem Watcher

cargo run --manifest-path FridgeSide/Cargo.toml
rem Fake fridge (only if we say we want it)

echo on 