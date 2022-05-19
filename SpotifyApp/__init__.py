from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db as root_db, login_manager, ma

#import flask marshmallow
from flask_marshmallow import Marshmallow
#import flask cors
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app) 

migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # specify what page to load for non authenticated users

ma.init_app(app)

CORS(app)