from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    db.create_all()
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fridge_name=current_user.fridge_name)