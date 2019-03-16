from flask import Flask, render_template,request, session, redirect, url_for
from functools import wraps
import flask_socketio
import json
import datetime
from app import app
from app import db
from app import socketio
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room, send, emit
import os
from app.models import User,Family,Join_Request,Reminder,List,Event,Chat,ChatMessage
from random import randint


def logged_in(f):
	@wraps(f)
	def wrapper():
		if 'logged_in' in session and session['logged_in'] == True:
			print("Operation allowed : {}".format(f))
			return f()
		else:
			print("Operation unallowed without login: {}".format(f))
			return redirect(url_for('login'))

	print("logged_in decorator called")
	return wrapper

@app.route('/')
@app.route('/index/')
@logged_in
def index():
	no_family = check_no_family(session['username'])
	return render_template('index.html',username = session['username'],no_family = no_family)

@app.route('/register/')
def register():
	return render_template('register.html')

@app.route('/post_register/',methods=['POST'])
def post_register():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		username = data['username']
		email = data['email']
		password = data['password']
		location = data['location_data']

		new_user = User(username=username,email=email,password=password,location=location)
		db.session.add(new_user)
		db.session.commit()

		print ('post_register added user:\n')
		print ('username: {}'.format(username))
		print ('email: {}'.format(email))
		print ('password: {}'.format(password))
		print ('location: {}'.format(location))

		return json.dumps({
			'status' : 'success'
			})

	except Exception as e:
		print ('post_register ERROR: {}'.format(e))
		return json.dumps({
			'status' : 'failure'
			})

@app.route('/login/')
def login():
	return render_template('login.html')

@app.route('/post_login/',methods=['POST'])
def post_login():
	try:
		session['logged_in'] = ''
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		username = data['username']
		password = data['password']

		print ('post_login tried user:\n')
		print ('username: {}'.format(username))
		print ('password: {}'.format(password))

		user = User.query.filter_by(username=username).first()

		if user is not None:
			if user.password == password:
				print ('logged in')
				session['logged_in'] = True
				session['username'] = username
				check_no_family(username)
				return json.dumps({'status' : 'success'})
			else:
				print ('password wrong')
				return json.dumps({'status' : 'failure'})
		else:
			print ('did not find user')
			return json.dumps({
				'status' : 'failure'
				})

	except Exception as e:
		print ('post_login ERROR: {}'.format(e))
		return json.dumps({
			'status' : 'failure'
			})


@app.route('/post_family/',methods=['POST'])
def post_family():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		name = data['name']
		country = data['country']
		location = data['location_data']
		phrase = data['phrase']

		new_room_id = generate_chat_room_id()
		print('new chat id: {}'.format(new_room_id))

		new_family = Family(name=name,country=country,location=location)

		db.session.add(new_family)

		db.session.flush()

		print('new family id: {}'.format(new_family.id))

		new_chat_room = Chat(family_id = new_family.id, room_id = new_room_id)

		db.session.add(new_chat_room)
		db.session.commit()

		print ('post_family added family:\n')
		print ('name: {}'.format(name))
		print ('country: {}'.format(country))
		print ('location: {}'.format(location))

		return json.dumps({
			'status' : 'success'
			})

	except Exception as e:
		print ('post_family ERROR: {}'.format(e))
		return json.dumps({
			'status' : 'failure'
			})

#generate random 10 digit numbers to use in Chat.room_id field
#checks if room_id already exists
def generate_chat_room_id():
	try:
		rooms = Chat.query.order_by(Chat.room_id).all()
		print('#generate_chat_room_id room_id:')
		for room in rooms:
			print(room.room_id)

		random_id = ''

		while True:
			random_id = randint(1000000000,9999999999)
			ok = True
			for room in rooms:
				if random_id == room.room_id:
					ok = False
				else:
					print('GENERATED: {}'.format(random_id))
			if ok:
				break

		return random_id

	except Exception as e:
		print('#generate_chat_room_id ERROR: {}'.format(e))


@app.route('/add_family_member/',methods=['POST'])
def add_family_member():
	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	username = data['username']
	family_name = data['family']

	print('add_family_member username = {} -- family_name = {}||'.format(username,family_name))

	family = ''
	user = ''

	try:
		try:
			family = Family.query.filter_by(name=family_name).first()
		except Exception as e:
			print("add_family_member family query failed. {}".format(e))

		try:
			user = User.query.filter_by(username=username).first()
		except Exception as e:
			print("add_family_member user query failed.")

		family.members.append(user)
		db.session.add(family)
		db.session.commit()
		return json.dumps({'status':'success'})

	except Exception as e:
		print('add_family_member ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

	family.members.append()

@app.route('/check_no_family/',methods=['POST'])
def check_no_family(username):
	try:

		user = User.query.filter_by(username=username).first()
		families = user.families

		no_family = False

		print('#check_no_family for user: {}'.format(user.families))
		if len(families) == 0:
			print('#check_no_family found no family.')
			no_family = True
		else:
			print('#check_no_family found {} families.'.format(len(families)))
			no_family = False

		session['no_family'] = no_family
		return no_family

	except Exception as e:
		print('#check_no_family ERROR: {}'.format(e))
		return 'ERROR'

@app.route('/query_families/',methods=['POST'])
def query_families():

	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	family_list = []

	try:

		if data['query_type'] == 'name':

			name = data['name']
			location = data['location_data']
			families = Family.query.filter(Family.name == name).filter(Family.location == location).all()
		elif data['query_type'] == 'id':
			id = data['id']
			families = Family.query.filter(Family.id == id).all()
		elif data['query_type'] == 'user':
			user = User.query.filter_by(username=data['username']).first()
			families = user.families

		print('query_families query result: {}'.format(families))

		for family in families:
			family_list.append({
				'id' : family.id,
				'name' : family.name,
				'country' : family.country,
				'location' : family.location,
				'members' : len(family.members)
				})

		print("Families: {}".format(family_list))

		return json.dumps({
			'status' : 'success',
			'families' : json.dumps(family_list, indent=4)
			})

	except Exception as e:
		print('query_all_families ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})


@app.route('/post_join_request/',methods=['POST'])
def post_join_request():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		user = data['user']
		family_id = int(data['id'])

		user_id = User.query.filter_by(username=user).first().id

		family = Family.query.filter_by(id=family_id).first()
		join_request = Join_Request(requester_id=user_id,family_id=family_id)

		family.join_requests.append(join_request)
		db.session.add(family)
		db.session.commit()

		families = Family.query.all()
		for family in families:
			print("post_join_request family: {}".format(family.join_requests))

		return json.dumps({'status' : 'success' })
	except Exception as e:
		print('post_join_request ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure' })

@app.route('/query_join_requests/',methods=['GET'])
def query_join_requests():
	try:
		username = session['username']

		user = User.query.filter_by(username=username).first()
		families = user.families

		returned_data = []

		for family in families:
			print('FAMILY {}'.format(family))

		for family in families:
			requests = family.join_requests

			requests_list = []

			for request in requests:
				print('REQUEST:{}'.format(request.requester_id))
				user = User.query.filter_by(id=request.requester_id).first()

				data = {
					'id' : user.id,
					'name' : user.username,
					'location' : user.location
				}

				requests_list.append(data)

			print("requests_list: {}".format(requests_list))

			family = Family.query.filter_by(id=family.id).first().name

			returned_data.append({
				'family' : family,
				'requests' : requests_list
				})

		print ("returned data: {}".format(returned_data))

		return json.dumps(returned_data)

	except Exception as e:
		print('query_join_requests ERROR: {}'.format(e))
		return ''


@app.route('/accept_join_request/',methods=['POST'])
def accept_join_request():

	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)
	data['family'] = data['family']
	family = Family.query.filter_by(name=data['family']).first()
	print('accept_join_request family: {}'.format(family.name))
	requester = User.query.filter_by(id=data['id']).first()
	join_request = Join_Request.query.filter(Join_Request.requester_id == data['id']).filter(Join_Request.family_id == family.id).first()
	family_join_requests = family.join_requests
	print('accept_join_request JOIN_REQUST: {}'.format(join_request))
	#delete request from database
	db.session.flush()
	db.session.delete(join_request)
	db.session.commit()
	#add requester to family members
	family.members.append(requester)
	db.session.add(family)
	db.session.commit()
	print('accept_join_request join_request: {}'.format(join_request))
	return ''

@app.route('/leave_family/',methods=['POST'])
def leave_family():
	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	id = data['id']
	username = data['user']


	try:
		user = User.query.filter_by(username=username).first()
		family = Family.query.filter_by(id=id).first()

		print('Family before:')
		print(family.members)
		print('User before:')
		print(user.families)
		user.families.remove(family)

		db.session.commit()

		user = User.query.filter_by(username=username).first()
		family = Family.query.filter_by(id=id).first()

		print('Family after:')
		print(family.members)
		print('User after:')
		print(user.families)

		return json.dumps({'status' : 'success'})

	except Exception as e:
		print('leave_family ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure'})

@app.route('/set_current_family/',methods=['POST'])
def set_current_family():
	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	try:
		family_name = data['family_name']
		username = data['username']

		user = User.query.filter_by(username=username).first()
		family = Family.query.filter_by(name=family_name).first()

		print('set_current_family current_family BEFORE: {}'.format(user.current_family))
		user.current_family = family.id

		db.session.add(user)
		db.session.commit()

		print('set_current_family current_family AFTER: {}'.format(user.current_family))

		join_chat_room(family.chat)

		# leave_room(room)
		# send(username + ' left the room.', room=room)

		
		return json.dumps({'status' : 'success'})

	except Exception as e:
		print('set_current_family ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure'})


@app.route('/get_current_family/',methods=['POST'])
def get_current_family():
	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	try:
		username = data['username']
		user = User.query.filter_by(username=username).first()

		current_family_id = user.current_family

		family = Family.query.filter_by(id=current_family_id).first()

		if family == None:
			return json.dumps({'status' : 'success','current_family' : ''})

		print('get_current_family current_family name: {}'.format(family.name))

		return json.dumps({'status' : 'success','current_family' : family.name})

	except Exception as e:
		print('get_current_family ERROR: {}'.format(e))

		return json.dumps({'status' : 'failure'})

@app.route('/post_reminders/',methods=['POST'])
def post_reminders():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		family_name = data['family_name']
		username = data['username']
		body = data['body']
		date_time = str(datetime.datetime.now())

		user = User.query.filter_by(username=username).first()
		family = Family.query.filter_by(name=family_name).first()

		family_id = family.id

		print('query_reminders date_time = {}'.format(type(date_time)))

		reminder = Reminder(family=family_id,body=body,date_time=date_time,user=username)

		db.session.add(reminder)
		db.session.commit()

		return json.dumps({'status':'success'})

	except Exception as e:
		print('post_reminders ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure' })


@app.route('/query_reminders/',methods=['POST'])
def query_reminders():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		print('query_reminders family_name = {}'.format(data['family_name']))

		family_name = data['family_name']
		family = Family.query.filter_by(name=family_name).first()

		reminders = family.reminders
		print('query_reminders family.reminders: {}'.format(family.reminders))

		reminders_list = []

		for reminder in reminders:
			reminders_list.append({'id':reminder.id,'body' : reminder.body,'date_time' :reminder.date_time,'user':reminder.user})

		reminders_dict = json.dumps({'reminders' : reminders_list})

		print('query_reminders reminders JSON:')
		print(json.dumps(reminders_dict))

		return json.dumps({'status':'success','reminders':reminders_dict})

	except Exception as e:
		print('query_reminders ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

@app.route('/delete_reminders/',methods=['POST'])
def delete_reminders():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		id = data['id']

		family_name = data['family_name']
		family = Family.query.filter_by(name=family_name).first()

		print('========='+id)

		reminder = family.reminders[int(id)]

		db.session.delete(reminder)
		db.session.commit()

		return json.dumps({'status':'success'})

	except Exception as e:
		print('delete_reminders ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

@app.route('/post_lists/',methods=['POST'])
def post_lists():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		family_name = data['family_name']
		username = data['username']
		title = data['title']
		date_time = str(datetime.datetime.now())
		elements_json = data['elements']

		user = User.query.filter_by(username=username).first()
		family = Family.query.filter_by(name=family_name).first()

		family_id = family.id

		print('query_lists date_time = {}'.format(type(date_time)))

		list_ = List(family_id=family_id,title=title,date_time=date_time,user=username,elements=elements_json)

		db.session.add(list_)
		db.session.commit()

		return json.dumps({'status':'success'})

	except Exception as e:
		print('post_lists ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure' })


@app.route('/query_lists/',methods=['POST'])
def query_lists():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		print('query_lists family_name = {}'.format(data['family_name']))

		family_name = data['family_name']
		family = Family.query.filter_by(name=family_name).first()

		lists = family.lists
		print('query_lists family.lists: {}'.format(family.lists))

		lists_list = []

		for list_ in lists:
			lists_list.append({'id':list_.id,'title' : list_.title,'date_time' :list_.date_time,'user':list_.user,'elements':list_.elements})

		lists_dict = json.dumps({'lists' : lists_list})

		print('query_lists lists JSON:')
		print(json.dumps(lists_dict))

		return json.dumps({'status':'success','lists':lists_dict})

	except Exception as e:
		print('query_lists ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

@app.route('/delete_lists/',methods=['POST'])
def delete_lists():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		id = data['id']
		print('got here1')
		print(id)

		# list = List.query.filter_by(id=id).first()

		family_name = data['family_name']
		family = Family.query.filter_by(name=family_name).first()

		list = family.lists[int(id)]

		print('got here2')
		print(list)

		db.session.delete(list)
		db.session.commit()

		print('got here3')

		return json.dumps({'status':'success'})

	except Exception as e:
		print('delete_lists ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

#======================== CALENDAR methods

@app.route('/post_events/',methods=['POST'])
def post_events():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		start_date = data['start_date']
		end_date = data['end_date']
		event_title = data['event_title']
		event_description = data['event_description']

		print('here1')

		family_id = get_current_family()
		family = Family.query.filter_by(id=family_id).first()

		print('here2')

		event = Event(family_id=family_id,title=event_title,start=start_date,end=end_date,description=event_description)

		print('here3')

		family.events.append(event)
		db.session.add(event)
		db.session.commit()

		print('here4')

		return json.dumps({'status':'success'})

	except Exception as e:
		print('post_lists ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure' })

@app.route('/query_events/',methods=['POST'])
def query_events():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		family_id = get_current_family()
		family = Family.query.filter_by(id=family_id).first()

		events = family.events
		print('query_events family.events: ')
		for event in family.events:
			print('id: {} title: {}'.format(event.id,event.title))

		events_list = []

		for event in events:
			events_list.append({"id":event.id,"title" : event.title,"description" :event.description,"start":event.start,"end":event.end})

		events_dict = json.dumps({"events" : events_list})

		print('query_events events JSON:')
		print(json.dumps(events_dict))

		return json.dumps({'status':'success','events':events_dict})

	except Exception as e:
		print('query_events ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

@app.route('/delete_event/',methods=['POST'])
def delete_events():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		id = data['id']

		# event = List.query.filter_by(id=id).first()

		family_id = get_current_family()
		family = Family.query.filter_by(id=family_id).first()

		events = family.events
		print('delete_event family.events: ')
		for event in family.events:
			print('id: {} title: {}'.format(event.id,event.title))

		print('ID: {}'.format(int(id)))

		event = Event.query.filter(Event.family_id == family_id).filter(Event.id == int(id)).first()

		print('delete_events Event:')
		print(event)

		db.session.delete(event)
		db.session.commit()

		print('got here3')

		return json.dumps({'status':'success'})

	except Exception as e:
		print('delete_events ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

@app.route('/update_event/', methods=['POST'])
def update_event():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		id = int(data['id'])
		title = str(data['title'])
		description = data['description']
		start_date = data['start_date']
		end_date = data['end_date']

		print('{} {}'.format(type(id),id))
		print('{} {}'.format(type(title),title))
		print('{} {}'.format(type(description),description))
		print('{} {}'.format(type(start_date),start_date))
		print('{} {}'.format(type(end_date),end_date))

		user = User.query.filter_by(username=session['username']).first()
		family_id = get_current_family()
		family = Family.query.filter_by(id=family_id).first()

		event = Event.query.filter(Event.family_id == family_id).filter(Event.id == id).first()
		event.title = title
		event.description = description
		event.start = start_date
		event.end = end_date

		print('update_event Event:')
		print(event)

		db.session.add(event)
		db.session.commit()

		print('got here3')

		return json.dumps({'status':'success'})

	except Exception as e:
		print('update_event ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

def get_current_family():
	user = User.query.filter_by(username=session['username']).first()
	print('get_current_family RESULT: {}'.format(user.current_family))
	return user.current_family

def get_current_family_object():
	family_id = get_current_family()

	family = Family.query.filter_by(id=family_id).first()
	print('get_current_family_object family: {}'.format(family))

	return family

def get_current_family_chatroom():
	chat_room_id = get_current_family_chat_object().room_id

	return chat_room_id

def get_current_family_chat_object():
	current_family = get_current_family_object()
	chat_room = current_family.chat[0]

	return chat_room

# ======================== CHAT ROOMS
#
@app.route('/post_chats/',methods=['POST'])
def post_chats():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		start_date = data['start_date']
		end_date = data['end_date']
		chat_title = data['chat_title']
		chat_description = data['chat_description']

		print('here1')

		family_id = get_current_family()
		family = Family.query.filter_by(id=family_id).first()

		print('here2')

		event = Event(family_id=family_id,title=event_title,start=start_date,end=end_date,description=event_description)

		print('here3')

		family.events.append(event)
		db.session.add(event)
		db.session.commit()

		print('here4')

		return json.dumps({'status':'success'})

	except Exception as e:
		print('post_lists ERROR: {}'.format(e))
		return json.dumps({'status' : 'failure' })

# ======================== SOCKETIO

@socketio.on('join_family_chat')
def join_chat_room(data):
	chat_room_id = get_current_family_chatroom()

	print('current family chat room id: {}'.format(chat_room_id))

	join_room(chat_room_id)
	emit(session['username'] + ' has entered the room.', room=chat_room_id)
	emit('joined_room', json.dumps({'username':session['username']}), room=chat_room_id)

@socketio.on('message')
def handle_message(message):
	print('socket io message')
	print(message)

@socketio.on('join')
def on_join(data):
	username = data['username']
	room = data['room']
	join_room(room)
	send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
	username = data['username']
	room = data['room']
	leave_room(room)
	send(username + ' left the room.', room=room)

@socketio.on('askformessage')
def askformessage(data):
	emit('chat message', json.dumps({'message':'TEST MESSAGE'}), room='testroom')

@socketio.on('chat_message')
def chat_message(data):
	print('[SOCKETIO] Chat message: \nfrom: {}\nbody: {}\ntimestamp: {}'.format(data['sender'],data['body'],data['timestamp']))

	sender = data['sender']
	body = data['body']
	timestamp = data['timestamp']

	family = get_current_family_object()

	chat_room = family.chat[0]
	chat_room_id = family.chat[0].id

	print('chat_message chat_room: {}'.format(chat_room_id))

	chat_message = ChatMessage(chat_id=chat_room_id, timestamp=timestamp,content=body,username=sender)
	db.session.add(chat_message)

	db.session.commit()

	print('[CHAT] chat_message added message:')
	print(chat_message)

	print('family messages:')
	print(chat_room.chat_messages)

	json_dict = {
		'body' : body,
		'timestamp' : timestamp,
		'sender' : sender
	}

	# user = User.query.filter_by(username=username).first()

	emit('chat_message', json.dumps(json_dict),
		 room=get_current_family_chatroom())
	
@app.route('/query_chat_messages/',methods=['POST'])
def query_chat_messages():
	try:
		JSONstring = json.dumps(request.get_json(force=True))
		data = json.loads(JSONstring)

		get_latest = False
		start_id = ''

		#check if id of last message is sent via request
		try:
			start_id = int(data['start_id'])-5;
			end_id = start_id + 5
		except Exception as e:
			print('[CHAT] No start and end id found.')
			get_latest = True

		chat_room = get_current_family_chat_object()
		print('[CHAT] query_chat_messages chat_room: {}'.format(chat_room))

		messages_list = []

		chat_messages = ChatMessage.query.filter(ChatMessage.chat_id == chat_room.id).order_by(ChatMessage.id.desc()).limit(16).all()
		filtered_chat_messages = []

		family_chat_messages = chat_room.chat_messages
		family_chat_filtered_messages = []

		print('[CHAT] Family chat messages:')
		print(family_chat_messages)

		if not get_latest:

			print('[CHAT] query_chat_messages getting messages between: {} and {}'.format(start_id,end_id))

			for message in family_chat_messages:
				if message.id > start_id and message.id < end_id:
					family_chat_filtered_messages.append(message)

			print('[CHAT] Family filtered messages: ')
			print(family_chat_filtered_messages)

			chat_messages = list(family_chat_filtered_messages)

		print('query_chat_messages all messages:')
		# limited_chat_messages = chat_room.chat_messages.filter_by(id)
		# print('query_chat_messages all messages:')

		chat_messages.reverse()

		for message in chat_messages:
			message_dict = {
				'id' : message.id,
				'body' : message.content,
				'timestamp' : message.timestamp,
				'username' : message.username
			}
			messages_list.append(message_dict)

		#debug printing:
		print('[CHAT] ALL MESSAGES:')
		for message in messages_list:
			print('----------------------')
			print('id : {}'.format(message['id']))
			print('body : {}'.format(message['body']))
			print('timestamp : {}'.format(message['timestamp']))
			print('username : {}'.format(message['username']))

		messages_dict = json.dumps({'messages' : messages_list})

		return json.dumps({'status':'success','messages':messages_dict})

	except Exception as e:
		print('query_chat_messages ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})