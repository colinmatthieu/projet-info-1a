from flask import Flask, redirect, url_for, request, make_response, send_file
app = Flask(__name__)

import influxdb_client, os, time
import io
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN") #export INFLUXDB_TOKEN=QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw==
token="QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw=="
org = "FrigoQ"
url = "http://localhost:8086"

db_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="Frigo1"

write_api = db_client.write_api(write_options=SYNCHRONOUS)
query_api = db_client.query_api()

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

import plotly.graph_objects as go
from plotly.subplots import make_subplots
@app.route("/getData/<source>")
def getData(source):
    query = """from(bucket: "Frigo1")
                |> range(start: today())
                |> filter(fn: (r) => r["_measurement"] == "ens")
                |> filter(fn: (r) => r["_field"] == "temp1")"""

    df = query_api.query_data_frame(org=org, query=query)
    print(df)
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(
            mode="lines",
            x=df["_time"],
            y=df["_value"],
            name="Température en K",
            line=dict(color="blue", width=2),
        ))
    #fig.show()
    fig.write_html("test.html")

    return open("template.html",encoding="utf-8").read()
    #return open("BDD/"+source).read()
    
@app.route("/getGenerated/<file>")
def generated(file):
    return open(file,encoding="utf-8").read()

@app.route("/images/<file>")
def images(file):
    print("dfvfdvdvdv", file)
    return send_file(file,mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)
    
