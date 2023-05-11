from flask import Flask, redirect, url_for, request
app = Flask(__name__)

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

from datetime import datetime
import pytz
def processLine(line):
    d,t,v=line.split(",")
    if d[0] == " ": d=d[1:]
    measurement = "ens"
    tags="fridgeName=frigo1"
    fields="temp="+v
    #print(fields)
    
    date= datetime.strptime(d+" "+t,"%d-%m-%y %H:%M:%S")
    local = pytz.timezone("Europe/Paris")
    local_dt = local.localize(date, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    #print(date.tzinfo)
    #print(date.isoformat())
    timestamp = str(int(datetime.timestamp(date)))
    #return measurement+","+tags+" "+fields+" "+timestamp
    p = influxdb_client.Point(measurement).field("temp1", float(v)).time(utc_dt.isoformat())
    write_api.write(bucket=bucket, org=org, record=p)
    
    
@app.route('/success/<name>')
def success(name):
    print("youhou",name)
    return 'welcome %s' % name

@app.route('/sendData',methods = ['POST'])
def sendData():
    #print(request.form)
    #print(request.json)

    user = request.json["fridgeName"]
    #for line in request.json["contents"].splitlines():
        #print(processLine(line))
    influxLines = list(map(processLine,request.json["contents"].splitlines()))
    #print(influxLines)
    #write_api.write("Frigo1",  influxLines)
    """f = open("BDD/data", "a")
    f.write(request.json["contents"])
    f.close()"""
    return redirect(url_for('success',name = user))

@app.route("/getData/<source>")
def getData(source):
    return open("BDD/"+source).read()
    
if __name__ == '__main__':
    app.run(debug = True)
    
