from extensions import db
from flask import Flask

def init_extensions(app):
    db.init_app(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['MySQL_HOST'] = 'localhost'
    app.config['MySQL_USER'] = 'root'
    app.config['MySQL_PASSWORD'] = 'bzx20020814'
    app.config['MySQL_DB'] = 'admin'
    app.config['MySQL_PORT'] = 3306
    init_extensions(app)
    return app
