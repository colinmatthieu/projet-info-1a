import influxdb_client, os
from influxdb_client.client.write_api import SYNCHRONOUS

import configparser
config = configparser.ConfigParser()
config.read("ServerSide/influxDB_volume/config/influx-configs")

token=config["default"]["token"][1:-1] #WE REMOVE THE QUOTES

org = "FrigoQ"
url = "http://localhost:8086"
bucket="Frigo1"

print(token)
db_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = db_client.write_api(write_options=SYNCHRONOUS)
query_api = db_client.query_api()
delete_api = db_client.delete_api()

start = "1970-01-01T00:00:00Z"
stop = "2100-01-01T00:00:00Z"

delete_api.delete(start, stop, '_measurement="ens"', bucket, org)