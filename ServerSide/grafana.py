from flask import Blueprint, render_template

grafana = Blueprint('grafana', __name__)

@grafana.route('/dashboard-admin')
def dashboard_admin():
    render_template('dashboard-admin.html')