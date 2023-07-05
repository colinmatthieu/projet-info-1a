import pytz

from flask import Flask, redirect, url_for, request, send_file
app = Flask(__name__)

import influxdb_client, os
from influxdb_client.client.write_api import SYNCHRONOUS

import configparser
config = configparser.ConfigParser()
config.read("influxDB_volume/config/influx-configs")

token=config["default"]["token"][1:-1] #WE REMOVE THE QUOTES

org = "FrigoQ"
url = "http://localhost:8086"
#bucket="Frigo1"

print(token)
db_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = db_client.write_api(write_options=SYNCHRONOUS)
query_api = db_client.query_api()
buckets_api = db_client.buckets_api()


def processLine(line,path,bucket):
    d,t,v=line.split(",")
    if d[0] == " ": d=d[1:]
    measurement,field,_ = os.path.basename(path).split(" ")
    #tags="fridgeName=frigo1"
    #fields="temp="+v
    
    from datetime import datetime
    
    date= datetime.strptime(d+" "+t,"%d-%m-%y %H:%M:%S")
    #date = str(date)+"+01:00"
    #print(date)
    
    local = pytz.timezone("Europe/Paris")
    local_dt = local.localize(date, is_dst=False)
    utc_dt = local_dt.astimezone(pytz.utc)
    #print(utc_dt)
    if float(v) >= 10.5698e-9:
        import requests
        webhook = "https://hooks.slack.com/services/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"
        message = {"text": "Seuil de temp dépassé !"}
        x = requests.post(webhook, json = message)
        print("Threshold triggered !", x)

    p = influxdb_client.Point(measurement).field(field, float(v)).time(utc_dt.isoformat())
    write_api.write(bucket=bucket, org=org, record=p)
    

@app.route('/sendData',methods = ['POST'])
def sendData():
    bucket = request.json["sender"]
    
    path = request.json["path"]
    for line in request.json["contents"].splitlines():
        #print(line)
        processLine(line,path,bucket)
    
    return "done" #please do not redirect to the dashboard

@app.route('/notifyData',methods = ['POST'])
def notifyData():
    print(request.json)
    bucket = request.json["sender"]
    if buckets_api.find_bucket_by_name(bucket) is None:
        buckets_api.create_bucket(bucket_name=bucket)
    path = request.json["path"]
    fridge,measure,_ = os.path.basename(path).split(" ")
    tables = query_api.query('from(bucket:"'+request.json["sender"]+'") |> range(start: 0, stop: now()) |> filter(fn: (r) => r["_measurement"] == "'+fridge+'")|> filter(fn: (r) => r["_field"] == "'+measure+'")|> last()')
    if len(tables) == 0:
        return "NEWDATA"
    
    d = tables[0].records[0]["_time"].astimezone(pytz.timezone("Europe/Paris")).strftime("%d-%m-%y,%H:%M:%S")
    #print(d)
    return d #please do not redirect to the dashboard
    
@app.route("/dashboard")
def dashboard(): #the source parameter is now ignored
    return open("template.html",encoding="utf-8").read()
    
@app.route("/genViz/<viz>.html")
def genViz(viz):
    rangeParam = "range(start: today())"
    if viz == "today":
        rangeParam = "range(start: date.sub(from: today(), d:1y))"
    elif viz == "realFridge":
        rangeParam = "range(start: date.sub(from: today(), d:3y), stop: date.sub(from: today(), d:1y))"
    query = f"""import "date"
                from(bucket: "Frigo1")
                |> {rangeParam}
                |> filter(fn: (r) => r["_measurement"] == "ens")
                |> filter(fn: (r) => r["_field"] == "temp1")"""

    df = query_api.query_data_frame(org=org, query=query)
    if len(df) == 0:
        return "NO DATA"

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(
            mode="lines",
            x=df["_time"],
            y=df["_value"],
            name="Température en K",
            line=dict(color="blue", width=2),
        ))
    generated="generated"+viz+".html"
    fig.write_html(generated)
    return open(generated,encoding="utf-8").read()
    
@app.route("/<file>") #Used to return the generated html (embedded in the template.html) (this might evolve later)
def generated(file):
    ext=file.split(".")[-1]
    type = "text/"+ext
    return send_file(file,mimetype=type)

@app.route("/images/<file>") #Used to send the favicon
def images(file):
    ext=file.split(".")[-1]
    type = "image/"+ext
    return send_file(file,mimetype=type)

if __name__ == '__main__':
    app.run(debug = True)
    
