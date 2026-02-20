from datetime import timedelta

# webapp configuration file

class Config:
    DEBUG = True
    SECRET_KEY = 'eaa95e0db900ed440ac15fe05a1dda2e621f2f2cb5d793140ad96b91cbc79edf'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)