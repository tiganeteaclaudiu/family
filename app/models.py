from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(64),index=True, unique=True)
	password = db.Column(db.String(128))

	def dump(self):
		print ("USER: {}:{} pass={}".format(self.username,self.email,self.password_hash))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def dump(self):
    	print ("POST: {}:{} pass={}".format(self.body,self.timestamp,self.user_id))
