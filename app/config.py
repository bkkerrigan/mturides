import os
from secretKeys import GOOGLE_LOGIN_CLIENT_ID, GOOGLE_LOGIN_REDIRECT_URI, GOOGLE_LOGIN_CLIENT_SECRET
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'mturides.db')
WTF_CSRF_ENABLED = False #This needs to be changed, because it is insecure
SECRET_KEY = 'secret'
