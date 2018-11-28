from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import User, Family

# u = User(username='claudiu10',email='claudiu10@gmail.com',password='claudiu')
# v = User(username='claudiu9',email='claudiu11@gmail.com',password='claudiu')
# w = User(username='claudiu8',email='claudiu12@gmail.com',password='claudiu')
# f = Family(name='tiganetea4')

# f.members.append(u)
# f.members.append(v)
# f.members.append(w)

# db.session.add(f)
# db.session.commit()

# v = User(username='susan', email='susan@example.com')
# db.session.add(u)
# db.session.add(v)
# db.session.commit()
# try:
# 	users = User.query.all()
# 	for user in users:
# 		user.dump()
# except Exception as e:
# 	print(e)

from app import routes