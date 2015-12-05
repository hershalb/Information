from flask import Flask, render_template, request
from models import db
from forms import SignupForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/information'
db.init_app(app)

app.secret_key = "development-key"

@app.route("/", methods=["GET", "POST"])
def index():
	form = SignupForm()

	if request.method == "POST":
		return "Success!"
	elif request.method == "GET":
		return render_template("index.html", form = form)

# @app.route("/signup")
# def signup():
# 	form = SignupForm()
# 	return render_template("index.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)