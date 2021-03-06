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
	checkins = db.relationship('CheckIn', backref='user_checkins', lazy=True)

	def dump(self):
		print ("USER: {}:{} pass={}".format(self.username,self.email,self.password_hash))

class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	country = db.Column(db.String(50))
	location = db.Column(db.String(100))
	members = db.relationship('User',secondary=family_identifier)
	join_requests = db.relationship('Join_Request', backref='family_request', lazy=True)
	reminders = db.relationship('Reminder', backref='family_reminder', lazy=True)
	lists = db.relationship('List', backref='family_list', lazy=True)
	events = db.relationship('Event', backref='family_events', lazy=True)
	chat = db.relationship('Chat', backref='family_chat', lazy=True)
	cloud = db.relationship('Cloud', backref='family_cloud', lazy=True)
	checkins = db.relationship('CheckIn', backref='family_checkins', lazy=True)

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


class Event(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(300), nullable=True)
	start = db.Column(db.String(100), nullable=False)
	end = db.Column(db.String(100), nullable=False)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'))

class Chat(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
	room_id = db.Column(db.String(10))
	chat_messages = db.relationship('ChatMessage', backref='chat_messages', lazy=True)

class ChatMessage(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
	timestamp = db.Column(db.String(100), nullable=False)
	content = db.Column(db.String(400), nullable=False)
	username = db.Column(db.String(30), nullable=False)

class Cloud(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
	dir_path = db.Column(db.String(200), nullable=False)
	files = db.relationship('File', backref='cloud_files', lazy=True)

class File(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	cloud_id = db.Column(db.Integer, db.ForeignKey('cloud.id'))
	filename = db.Column(db.String(200), nullable=False)
	extension = db.Column(db.String(20), nullable=False)
	size = db.Column(db.Integer, nullable=False)
	username = db.Column(db.String(30), nullable=False)
	timestamp = db.Column(db.String(100), nullable=False)

class CheckIn(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.String(100), nullable=False)
	latitude = db.Column(db.String(100), nullable=False)
	longitude = db.Column(db.String(100), nullable=False)