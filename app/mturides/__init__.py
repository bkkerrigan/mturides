from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

#Link the database to the app
db = SQLAlchemy(app)

#Google Authentication
from flask_googlelogin import GoogleLogin 
#from flask_login import LoginManager
googlelogin = GoogleLogin(app)
#Let the app use bootstrap
from flask_bootstrap import Bootstrap
Bootstrap(app)



#Let manager manage the app
from flask.ext.script import Manager
manager = Manager(app)

#routes
from . import routes
