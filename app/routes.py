from app import app
from app import db
from flask import render_template,request, session, redirect, url_for
from app.models import User, Family, Join_Request, family_identifier, Reminder, List
from functools import wraps
import json
import datetime


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

		new_family = Family(name=name,country=country,location=location)
		db.session.add(new_family)
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

	get_current_family()

	JSONstring = json.dumps(request.get_json(force=True))
	data = json.loads(JSONstring)

	data['family'] = data['family']

	family = Family.query.filter_by(name=data['family']).first()

	requester = User.query.filter_by(id=data['id']).first()

	join_request = Join_Request.query.filter(Join_Request.requester_id == data['id']).filter(Join_Request.family_id == family.id).first()

	db.session.delete(join_request)

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

		reminder = Reminder.query.filter_by(id=id).first()

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

		list_ = List.query.filter_by(id=id).first()

		db.session.delete(list_)
		db.session.commit()		

		return json.dumps({'status':'success'})

	except Exception as e:
		print('delete_lists ERROR: {}'.format(e))
		return json.dumps({'status':'failure'})

def get_current_family():
	user = User.query.filter_by(username=session['username']).first()
	print('get_current_family RESULT: {}'.format(user.current_family))
	return user.current_family

