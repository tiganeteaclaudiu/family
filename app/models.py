from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique=True,nullable=False)
	email = db.Column(db.String(64),index=True, unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	family = db.Column(db.String(50), db.ForeignKey('family.id'))

	def dump(self):
		print ("USER: {}:{} pass={}".format(self.username,self.email,self.password_hash))

family_identifier = db.Table('family_identifier',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('family_id', db.Integer, db.ForeignKey('family.id'))
)

class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	members = db.relationship('User',secondary=family_identifier)

class Families(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	db.Column('family_id', db.Integer, db.ForeignKey('family.id'))
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
