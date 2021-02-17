import os

from flask import Flask, session, render_template, request, make_response, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session['user_id'] = None
    return render_template("login.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session.get('user_id'):
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html")
    elif request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        query = f"SELECT * FROM users WHERE (username='{username}') AND (password='{password}');"
        users = list(db.execute(query))
        for row in users:
            print(row)
            print(row['id'])
        print('log 1')
        print(users)
        if len(users):
            print('log 2')
            session['user_id'] = users[0]['id']
            return redirect(url_for('dashboard'))
        else:
            print('log 3')
            return render_template("login.html", message="User with this username and password does not exist! Please "
                                                         "try again or Sign up.")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}');"
        db.execute(query)
        db.commit()
        return render_template("success.html")
    elif request.method == "GET":
        return render_template("signup.html")
