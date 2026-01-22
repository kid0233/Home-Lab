from flask import request, has_request_context
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import zipfile
import os
from os.path import basename

os.makedirs("applogs", exist_ok=True)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        
        return super().format(record)

class CustomFilter(logging.Filter):
    def filter(self, record):
        ...

def rotator(source, dest):
    zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED).write(source, basename(source))
    os.remove(source)
    
def log_config(app):
    app.logger.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler("applogs/logs.log", when="midnight", interval=1, backupCount=7)
    file_handler.namer = lambda name: name.replace(".log", "") + ".zip"
    file_handler.setLevel(logging.INFO)
    file_handler.rotator = rotator

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    formatter = CustomFormatter("[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s in %(module)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)

    logging.getLogger('werkzeug').addHandler(file_handler)