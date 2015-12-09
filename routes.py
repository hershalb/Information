from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/information'
db.init_app(app)

app.secret_key = "development-key"

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
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return "Success!" # redirect(url_for('home'))
	
	elif request.method == "GET":
		return render_template("signup.html", form = form)

@app.route('/<firstname>.<lastname>', methods = ['GET', 'POST'])
def home(firstname, lastname):
	if 'email' not in session:
		return redirect(url_for('login'))

	email = session['email']
	user = User.query.filter_by(email=email).first()
	if firstname != user.firstname:
		firstname = user.firstname

	# old_people = User.query.filter_by()  '''INCLUDES THE NAMES OF ALL THE PEOPLE IN THE DATABASE'''
	# new_people = []
	# for person in old_people:
	# 	new_people.append(person.firstname)

	return render_template('home.html', firstname = firstname, lastname = lastname)#, people = new_people)

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

if __name__ == "__main__":
	app.run(debug=True)