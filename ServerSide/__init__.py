from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import influxdb_client
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

db = SQLAlchemy()

from apscheduler.schedulers.background import BackgroundScheduler
def deadmanAlert(sender,fridge,measure):
    #sender="ensParis"
    #fridge="CH1"
    #measure="T"
    print("Deadman check:", sender,fridge,measure)
    
    tables = query_api.query('from(bucket:"'+sender+'") |> range(start: 0, stop: now()) |> filter(fn: (r) => r["_measurement"] == "'+fridge+'")|> filter(fn: (r) => r["_field"] == "'+measure+'")|> last()')
    if len(tables) == 0:
        return "NEWDATA"
    import pytz
    import datetime
    d = tables[0].records[0]["_time"].astimezone(pytz.timezone("Europe/Paris"))#.strftime("%d-%m-%y,%H:%M:%S")
    print("Last recorded value:",d)
    now = datetime.datetime.now().astimezone(pytz.timezone("Europe/Paris"))
    print("Current time:",now)
    minutesSinceData = (now - d).total_seconds()/60
    print(minutesSinceData)
    if minutesSinceData > 2:
        import requests
        webhook = "https://hooks.slack.com/services/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"
        message = {"text": f"Deadman alert !\nHaven't received news from {sender} - {fridge} in {str(minutesSinceData)} minutes !"}
        x = requests.post(webhook, json = message)
        print("Deadman triggered !", x)
    return d #please
    
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "secret-key-wow"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../ServerSide/db.sqlite'

    from .models import User
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(fridge_id):
        return User.query.get(int(fridge_id))
    
    #blueprint for auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #blueprint for the rest
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #blueprint for the InfluxDB database
    from .influx import influx as influx_blueprint
    app.register_blueprint(influx_blueprint)

    from .grafana import grafana as grafana_blueprint
    app.register_blueprint(grafana_blueprint)
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(deadmanAlert, 'interval',["ensParis", "demo_T", "T0"], seconds=30)
    scheduler.start()

    return app