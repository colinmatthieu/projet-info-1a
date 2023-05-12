docker run -d -p 8086:8086 --name FrigoDB -v %cd%/ServerSide/influxDB_volume/data:/var/lib/influxdb2 -v %cd%/ServerSide/influxDB_volume/config:/etc/influxdb2 -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=admin -e DOCKER_INFLUXDB_INIT_PASSWORD=adminadmin -e DOCKER_INFLUXDB_INIT_ORG=FrigoQ -e DOCKER_INFLUXDB_INIT_BUCKET=Frigo1 influxdb:latest

echo off
:waitloop
IF EXIST "ServerSide/influxDB_volume/config/influx-configs" GOTO waitloopend
echo "Loading... be patient ..."
sleep 5
goto waitloop
:waitloopend
echo on
launch.bat