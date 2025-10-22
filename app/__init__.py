import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# ⚠️ Extensions : ne pas passer l'app ici
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SECRET_KEY'] = 'ma_cle_secrete'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.models import User, Post, ResourceRequest, ResourceInstance

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes_auth import auth
    from app.routes_main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # ----------------------------
    # Création automatique des tables
    # ----------------------------
    with app.app_context():
        db.create_all()

    return app
