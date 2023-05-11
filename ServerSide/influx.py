import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN") #export INFLUXDB_TOKEN=QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw==
token="QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw=="
org = "FrigoQ"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="Frigo1"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="FrigoQ", record=point)
  time.sleep(1) # separate points by 1 second
  
query_api = write_client.query_api()

query = """from(bucket: "Frigo1")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="FrigoQ")

for table in tables:
  for record in table.records:
    print(record)
print("-"*10)

#----------------
query_api = write_client.query_api()

query = """from(bucket: "Frigo1")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="FrigoQ")

for table in tables:
    for record in table.records:
        print(record)