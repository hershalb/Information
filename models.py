from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Projects(db.Model):
  __tablename__ = 'projects'
  name = db.Column(db.String(100))
  p_id = db.Column(db.Integer, primary_key = False)
  u_id = db.Column(db.Text, db.ForeignKey('users.uid'), nullable=False)
  goal = db.Column(db.String(50))
  plan = db.Column(db.String(300))
  num = db.Column(db.Integer, primary_key = True)

  def __init__(self, project_id, projectname, user_id, goal, plan):
    self.p_id = project_id
    self.name = projectname.title()
    self.u_id = user_id
    self.goal = goal
    self.plan = plan

class Progress(db.Model):
  __tablename__ = 'progress'
  projid = db.Column(db.Integer, db.ForeignKey('projects.num'), nullable=False)
  addition = db.Column(db.String(300))
  userid = db.Column(db.Text, db.ForeignKey('users.uid'), nullable=False)
  num = db.Column(db.Integer, primary_key = True)

  def __init__(self, project_id, plan, user_id):
    self.projid = project_id
    self.addition = plan
    self.userid = user_id

