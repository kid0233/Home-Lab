from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def webapp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "cenetlab"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
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

