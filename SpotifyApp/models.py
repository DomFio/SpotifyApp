from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

#imports for login manager
from flask_login import UserMixin
#import for flask login
from flask_login import LoginManager
#import for flask-marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# make sure to add in usermixin to user class
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name = '', last_name = '', id = '', password='', token='', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
        
    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Artist(db.Model):
    artist = db.Column(db.String, primary_key = True )
    related_artist = db.Column(db.String(150), nullable = False, default = '')
    genres = db.Column(db.String(150), nullable = False, default = '')
    images = db.Column(db.String(150), nullable = False, default = '')

    def __init__(self, data):
        self.artist = data['artist']
        self.related_artist = data['artist']['name']
        self.genres = data['artist']['genres'][0]
        self.images = data['artist']['images'][2]['url']

