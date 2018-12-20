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
	location = db.Column(db.String(128), nullable=False)
	families = db.relationship('Family',secondary=family_identifier)
	current_family = db.Column(db.Integer)

	def dump(self):
		print ("USER: {}:{} pass={}".format(self.username,self.email,self.password_hash))

class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	country = db.Column(db.String(50))
	location = db.Column(db.String(100))
	members = db.relationship('User',secondary=family_identifier)
	join_requests = db.relationship('Join_Request', backref='family', lazy=True)
	reminders = db.relationship('Reminder', backref='family_reminder', lazy=True)
	lists = db.relationship('List', backref='family_list', lazy=True)

class Join_Request(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	requester_id = db.Column(db.Integer)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'),nullable=False)

class Reminder(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	family = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
	body = db.Column(db.String(100), nullable=False)
	date_time = db.Column(db.String(100), nullable=False)
	user = db.Column(db.String(50), nullable=False)

class List(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable=False)
	elements = db.Column(db.String(1000))
	user = db.Column(db.String(50), nullable=False)
	date_time = db.Column(db.String(100), nullable=False)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'))