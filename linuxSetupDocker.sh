docker run -d -p 8086:8086 --name FrigoDB -v $PWD/ServerSide/influxDB_volume/data:/var/lib/influxdb2 -v $PWD/ServerSide/influxDB_volume/config:/etc/influxdb2 -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=admin -e DOCKER_INFLUXDB_INIT_PASSWORD=adminadmin -e DOCKER_INFLUXDB_INIT_ORG=FrigoQ -e DOCKER_INFLUXDB_INIT_BUCKET=Frigo1 influxdb:latest
until [ -f ServerSide/influxDB_volume/config/influx-configs ]
do
     sleep 2
done
./launch.sh