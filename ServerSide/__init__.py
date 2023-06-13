from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "secret-key-wow"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../ServerSide/db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(fridge_id):
        return User.query.get(int(fridge_id))
    
    #blueprint for auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #blueprint for the rest
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app