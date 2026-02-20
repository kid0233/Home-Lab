from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .weblog import log_config
from .config import Config

db = SQLAlchemy()


def webapp():
    app = Flask(__name__)
    app.config.from_object(Config)
    log_config(app)
    db.init_app(app)
    
    from .auth import auth
    from .main import main

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(main, url_prefix="/")

    from .model import User

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id: int):
        return User.query.get(int(id))

    return app

