from flask import Blueprint, render_template, current_app, request, send_file, redirect
from flask_login import login_required, current_user
from . import db_client, write_api, query_api,buckets_api, org, token
import influxdb_client

import os
import pytz

influx = Blueprint('influx', __name__)

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
    THRESHOLD = 0.
    if "T" in field:
        if float(v) >= THRESHOLD:
            import requests
            webhook = "https://hooks.slack.com/services/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"
            message = {"text": f"Threshold triggered. Sender : {bucket}, fridge: {measurement}, type: {field}, value: {v}"}
            x = requests.post(webhook, json = message)
            print("Threshold triggered !", x)

    p = influxdb_client.Point(measurement).field(field, float(v)).time(utc_dt.isoformat())
    write_api.write(bucket=bucket, org=org, record=p)

@influx.route('/sendData',methods = ['POST'])
def sendData():
    bucket = request.json["sender"]
    
    path = request.json["path"]
    for line in request.json["contents"].splitlines():
        #print(line)
        processLine(line,path,bucket)
    
    return "done" #please do not redirect to the dashboard
    
@influx.route('/notifyData',methods = ['POST'])
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

@influx.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
@influx.route('/style.css')
def render_dashboard_css():
    return send_file("templates/style.css")

@influx.route("/genViz/<viz>.html")
def genViz(viz):
    lab = "ensParis"
    fridge = "CH1"
    measure = "P"
    rangeParam = "range(start: today())"
    if viz == "today":
        rangeParam = "range(start: date.sub(from: today(), d:1y))"
        fridge = "fakeFridge1"
        measure = "T"
    elif viz == "realFridge":
        rangeParam = "range(start: date.sub(from: today(), d:3y), stop: date.sub(from: today(), d:1y))"
    query = f"""import "date"
                from(bucket: "{lab}")
                |> {rangeParam}
                |> filter(fn: (r) => r["_measurement"] == "{fridge}")
                |> filter(fn: (r) => r["_field"] == "{measure}")"""

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
    
@influx.route('/visualize')
def render_visualization():
    return render_template('visualization.html')

@influx.route('/grafanaLink')
def render_grafana_link():
    return redirect("http://localhost:3000/d-solo/null?orgId=1&from=1609455651000&to=1686666994000&panelId=123124")