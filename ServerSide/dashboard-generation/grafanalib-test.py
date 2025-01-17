from grafanalib.core import (
    Dashboard, TimeSeries, Target, GridPos, Ae3ePlotly
)
from grafanalib.influxdb import InfluxDBTarget
from grafanalib._gen import DashboardEncoder
import json
import requests
from decouple import config #Used for environment variables


with open("simple-query.flux", 'r') as f:
    query = f.read()

dashboard = Dashboard(
    title = "Python generated example dashboard",
    description = "Example description",
    tags = [
        'example'
    ],
    timezone='browser',
    panels=[
        TimeSeries(
            title="Random Walk",
            dataSource='default',
            maxDataPoints = 1000,
            targets=[
                InfluxDBTarget(
                    datasource='FrigoQ',
                    query=query
                ),
            ],
            gridPos=GridPos(h=8, w=16, x=0, y=0)
        ),
        # Ae3ePlotly(
        #    title = "Plotly Panel",
        #    dataSource = "FrigoQ",
        #    targets = [
        #         InfluxDBTarget(
        #             datasource='FrigoQ',
        #             query=query
        #         ),
        #    ]
        # )
    ]
).auto_panel_ids()

def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    '''
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param dashboard - Dashboard() created via grafanalib
    '''

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)

def upload_to_grafana(json, server, api_key, verify=True):
    '''
    upload_to_grafana tries to upload dashboard to grafana and prints response

    :param json - dashboard json generated by grafanalib
    :param server - grafana server name
    :param api_key - grafana api key with read and write privileges
    '''

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    r = requests.post(f"http://{server}/api/dashboards/db", data=json, headers=headers, verify=verify)
    # TODO: add error handling
    print(f"{r.status_code} - {r.content}")

GRAFANA_API_KEY = config("GRAFANA_API_KEY")
GRAFANA_SERVER = config("GRAFANA_SERVER")
print(GRAFANA_API_KEY)
print(GRAFANA_SERVER)

my_dashboard_json = get_dashboard_json(dashboard=dashboard, overwrite=True)
upload_to_grafana(my_dashboard_json, GRAFANA_SERVER, GRAFANA_API_KEY)