from flask import Flask, redirect, url_for, request, send_file
app = Flask(__name__)

import influxdb_client, os
from influxdb_client.client.write_api import SYNCHRONOUS

#token = os.environ.get("INFLUXDB_TOKEN") #export INFLUXDB_TOKEN=QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw==
token="QOcPWIZWqhpCwiOMTPxLvK4X-xOIqRzhK3wbBnhYHFG1nTnjcLHzpCPiI2hfwI2S92p8oqzn_LZzefNoZIqLJw=="
org = "FrigoQ"
url = "http://localhost:8086"
bucket="Frigo1"

db_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = db_client.write_api(write_options=SYNCHRONOUS)
query_api = db_client.query_api()


def processLine(line):
    d,t,v=line.split(",")
    if d[0] == " ": d=d[1:]
    measurement = "ens"
    tags="fridgeName=frigo1"
    fields="temp="+v
    
    from datetime import datetime
    import pytz
    date= datetime.strptime(d+" "+t,"%d-%m-%y %H:%M:%S")
    local = pytz.timezone("Europe/Paris")
    local_dt = local.localize(date, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    p = influxdb_client.Point(measurement).field("temp1", float(v)).time(utc_dt.isoformat())
    write_api.write(bucket=bucket, org=org, record=p)
    

@app.route('/sendData',methods = ['POST'])
def sendData():
    for line in request.json["contents"].splitlines():
        processLine(line)
    
    return redirect(url_for('getData',source = "d"))


@app.route("/getData/<source>")
def getData(source): #the source parameter is now ignored
    query = """from(bucket: "Frigo1")
                |> range(start: today())
                |> filter(fn: (r) => r["_measurement"] == "ens")
                |> filter(fn: (r) => r["_field"] == "temp1")"""

    df = query_api.query_data_frame(org=org, query=query)

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
    fig.write_html("generated.html")

    return open("template.html",encoding="utf-8").read()
    
@app.route("/getGenerated/<file>") #Used to return the generated html (embedded in the template.html) (this might evolve later)
def generated(file):
    return open(file,encoding="utf-8").read()

@app.route("/images/<file>") #Used to send the favicon
def images(file):
    return send_file(file,mimetype='image/png')

if __name__ == '__main__':
    app.run(debug = True)
    
