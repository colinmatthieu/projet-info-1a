from flask import Blueprint, render_template, current_app, request, send_file
from flask_login import login_required, current_user
from . import db_client, write_api, query_api, bucket, org, token
import influxdb_client

influx = Blueprint('influx', __name__)

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
    
    if float(v) >= 10.5698e-9:
        import requests
        webhook = "https://hooks.slack.com/services/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"
        message = {"text": "Seuil de temp dépassé !"}
        x = requests.post(webhook, json = message)
        print("Threshold triggered !", x)

    p = influxdb_client.Point(measurement).field("temp1", float(v)).time(utc_dt.isoformat())
    write_api.write(bucket=bucket, org=org, record=p)

@influx.route('/sendData',methods = ['POST'])
def sendData():
    for line in request.json["contents"].splitlines():
        #print(line)
        processLine(line)
    
    return "no" 

@influx.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
@influx.route('/style.css')
def render_dashboard_css():
    return send_file("templates/style.css")

@influx.route("/genViz/<viz>.html")
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
    return open(generated,encoding="utf-8").read() # render_template ?