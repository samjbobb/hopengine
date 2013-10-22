from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') # load configuration 
db = SQLAlchemy(app) # setup database

# Login stuff
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# Finally, set up the views and modules
from app import views, models