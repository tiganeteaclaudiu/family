from app import app
from app import db
from flask import render_template,request, session, redirect, url_for
from app.models import User, Family
from functools import wraps
import json

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
	return render_template('index.html')

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

		new_user = User(username=username,email=email,password=password)
		db.session.add(new_user)
		db.session.commit()

		print ('post_register added user:\n')
		print ('username: {}'.format(username))
		print ('email: {}'.format(email))
		print ('password: {}'.format(password))

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

@app.route('/family/')
def family():
	return render_template('family.html')

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
