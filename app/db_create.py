from mturides import db
from config import SQLALCHEMY_DATABASE_URI
db.drop_all()
db.create_all()