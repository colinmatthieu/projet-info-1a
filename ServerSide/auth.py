from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #login code
    fridge_name = request.form.get('fridge_name')
    secret_key = request.form.get('secret_key')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(fridge_name=fridge_name).first()

    if not user or not check_password_hash(user.secret_key, secret_key):
        flash('Vérifiez vos informations')
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to the database
    fridge_name = request.form.get('fridge_name')
    secret_key = request.form.get('secret_key')

    user = User.query.filter_by(fridge_name=fridge_name).first()
    if user:
        flash('Le frigo existe déjà')
        return redirect(url_for('auth.signup'))

    new_user = User(fridge_name=fridge_name, secret_key=generate_password_hash(secret_key, method='sha256'))

    # add new user to database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))