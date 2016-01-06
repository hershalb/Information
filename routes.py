from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Projects
from forms import SignupForm, LoginForm, ProjectForm
import random
import requests
import json


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/information'
db.init_app(app)

app.secret_key = "development-key"

project_list = []

def project_nums():
	global project_list
	project_id = int(random.random()*100000000)
	if project_id in project_list:
		return project_nums()
	return project_id

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if 'email' in session:
		email = session['email']
		user = User.query.filter_by(email=email).first()
		firstname, lastname = user.firstname, user.lastname
		return redirect(url_for('home', firstname=firstname, lastname = lastname))

	form = SignupForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("signup.html", form = form)
		else:
			firstname = form.first_name.data
			lastname = form.last_name.data
			newuser = User(firstname, lastname, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('home', firstname=firstname, lastname=lastname))
	
	elif request.method == "GET":
		return render_template("signup.html", form = form)

@app.route('/<firstname>.<lastname>', methods = ['GET', 'POST']) # <firstname>.<lastname>
def home(firstname, lastname):
	if 'email' not in session:
		return redirect(url_for('login'))

	email = session['email']
	user = User.query.filter_by(email=email).first()
	user_id = user.uid

	if firstname != user.firstname:
		return redirect(url_for('home', firstname=user.firstname, lastname=user.lastname))

	# old_people = User.query.filter_by()  '''INCLUDES THE NAMES OF ALL THE PEOPLE IN THE DATABASE'''
	# new_people = []
	# for person in old_people:
	# 	new_people.append(person.firstname)

	user_projects_table = Projects.query.filter_by(u_id = user_id)
	# user_projects_names = []
	# for project in user_projects_table:
	# 	user_projects_names.append(project.name)

	return render_template('home.html', firstname = firstname, lastname = lastname, projects = user_projects_table)#, people = new_people)

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

@app.route("/login", methods = ["GET", "POST"])
def login():
	if 'email' in session:
		email = session['email']
		user = User.query.filter_by(email=email).first()
		firstname, lastname = user.firstname, user.lastname
		return redirect(url_for('home', firstname=firstname, lastname = lastname))

	form = LoginForm()
	if request.method == "POST":
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()

			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				firstname = user.firstname
				lastname = user.lastname
				return redirect(url_for('home', firstname = firstname, lastname = lastname))
			else:
				return redirect(url_for('login'))
	

	elif request.method == "GET":
		return render_template('login.html', form=form)

@app.route("/new-project", methods = ["GET", "POST"])
def form():
	form = ProjectForm()
	email = session['email']
	project_id = project_nums()
	user = User.query.filter_by(email=email).first()
	user_id = user.uid
	firstname, lastname = user.firstname, user.lastname
	
	if request.method == "POST":
		if form.validate() == False:
			return render_template('form.html', form=form, firstname=firstname, lastname=lastname)
		else:
			name = form.groupname.data
			goal = form.goal.data
			accomplish = form.accomplish.data
			friends = form.friends.data
			new_user_project = Projects(project_id, name, user_id, goal, accomplish)
			if friends:
				friends = friends.split(" ")
				for i in friends:
					friend = None
					if "@" in i:
						friend = User.query.filter_by(email=i[1:-2]).first()
						print(i[:-1])
						print(i)
						friend_id = friend.uid
					if friend:
						new_friend_project = Projects(project_id, name, friend_id, '', '')
						db.session.add(new_friend_project)
						db.session.commit()
			db.session.add(new_user_project)
			db.session.commit()

			return redirect(url_for('home', firstname = firstname, lastname = lastname))


	return render_template("form.html", form=form, firstname=firstname, lastname= lastname)

@app.route("/<projectnum>", methods = ["GET", "POST"])
def project(projectnum):
	email = session['email']
	projects = Projects.query.filter_by(p_id=projectnum).all()
	modal = False
	new_projects = []
	user = User.query.filter_by(email=email).first()
	firstname, lastname = user.firstname, user.lastname
	all_users = [project.u_id for project in projects]
	if user.uid not in all_users:
		return redirect(url_for("home", firstname=firstname, lastname=lastname))
	for project in projects:
		if project.goal:
			new_projects.append(project)
	if user.uid in [project.u_id for project in new_projects]:
		modal = True
	print(modal)
	return render_template("projects.html", firstname=firstname, lastname=lastname, users = new_projects, modal = modal)

@app.route("/checkform", methods=['GET', 'POST'])
def checkform():
	email = session['email']
	user = User.query.filter_by(email=email).first()
	data = request.form['letter']
	check = User.query.filter(User.firstname.contains(str(data))).all()
	if check is not None:
		if user in check:
			check.remove(user)
		names = [r.firstname + ' ' + r.lastname + ' (' + r.email + ")" for r in check]
		user = str(names)
		password = "password"
		return json.dumps({'status':'OK','user':user,'pass':password})
	else:
		pass
	

if __name__ == "__main__":
	app.run(debug=True)







