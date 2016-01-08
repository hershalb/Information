from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name = StringField("First name", validators=[DataRequired("Please enter your first name.")])
	last_name = StringField("Last name", validators=[DataRequired("Please enter your last name.")])
	email = StringField("Email", validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
	password = PasswordField("Password", validators=[DataRequired("Please enter your password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField("Sign up")

class LoginForm(Form):
	email = StringField("Email", validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	password = PasswordField("Password", validators=[DataRequired("Please enter your password.")])
	submit = SubmitField('Sign in')

class ProjectForm(Form):
	groupname = StringField("Project", validators=[DataRequired("Please enter your group name.")])
	friends = StringField("Friends")
	goal = TextAreaField("Goal", validators=[DataRequired("Please enter your goal for the project."), Length(min=50, max=100, message="Goals must be from 50 to 100 characters.")])
	accomplish = TextAreaField("Accomplish", validators=[DataRequired("Please enter how you plan on accomplishing your goal."), Length(min=100, max=300, message="You must write from 100 to 300 characters.")])
	submit = SubmitField("Begin")

class FriendProjectForm(Form):
	goal = TextAreaField("Goal", validators=[DataRequired("Please enter your goal for the project."), Length(min=50, max=100, message="Goals must be from 50 to 100 characters.")])
	accomplish = TextAreaField("Accomplish", validators=[DataRequired("Please enter how you plan on accomplishing your goal."), Length(min=100, max=300, message="You must write from 100 to 300 characters.")])
	submit = SubmitField("Add!")

class PlanForm(Form):
	plan = TextAreaField("Plan", validators=[DataRequired("Please enter how you plan on accomplishing your goal."), Length(min=50, max=100, message="Plans must be from 50 to 100 characters.")])
	submit = SubmitField("Add!")