from app import db
from datetime import datetime

family_identifier = db.Table('family_identifier',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('family_id', db.Integer, db.ForeignKey('family.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique=True,nullable=False)
	email = db.Column(db.String(64),index=True, unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	families = db.relationship('Family',secondary=family_identifier)

	def dump(self):
		print ("USER: {}:{} pass={}".format(self.username,self.email,self.password_hash))

class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	country = db.Column(db.String(50))
	location = db.Column(db.String(100))
	members = db.relationship('User',secondary=family_identifier)
	join_requests = db.relationship('Join_Request', backref='family', lazy=True)

class Join_Request(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	requester_id = db.Column(db.Integer)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'),nullable=False)

