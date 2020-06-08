import os

from flask import Flask, g, redirect, render_template, request, session, url_for
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

@app.before_first_request
def init():
  g.user = None
  if "user_id" in session:
    session.pop("user_id", None)

@app.before_request
def before_request():
  global db
  if "user_id" in session:
    try:
      g.user
    except AttributeError:
      g.user = None

    if g.user is None:
      users = db.execute("SELECT id, username FROM reader WHERE reader.id = :id", {"id": session["user_id"]})
      if users.rowcount == 1:
        user = users.fetchone()
        g.user = user
  else:
    g.user = None

@app.route("/", methods=["GET"])
def index():
  if g.user is not None:
    return redirect(url_for('home'))
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "GET":
    if g.user is not None:
      return redirect(url_for('home'))
    return redirect(url_for('index'))

  global db
  username = request.form.get("username")
  password = request.form.get("password")
  users = db.execute("SELECT * FROM reader WHERE reader.username = :username", {"username": username})
  if users.rowcount != 0:
    return render_template("error.html", message=f"The username '{username}' has been used!")
  db.execute("INSERT INTO reader (username, password) VALUES (:username, :password)", {"username": username, "password": password})
  db.commit()
  return render_template("success.html", message="Registration Successful!", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    if g.user is not None:
      return redirect(url_for('home'))
    return redirect(url_for('index'))

  if g.user is not None:
    session.pop("user_id", None)
  
  global db
  username = request.form.get("username")
  password = request.form.get("password")
  users = db.execute("SELECT * FROM reader WHERE reader.username = :username", {"username": username})
  if users.rowcount == 0:
    return render_template("error.html", message="User does not exist!")
  elif users.rowcount != 1: # Impossible to happen
    return render_template("error.html", message="Duplicated users!")
  else:
    user = users.fetchone()
    if user.password != password:
      return render_template("error.html", message="Incorrect password!")
    session["user_id"] = user.id
    return redirect(url_for('home'))

@app.route("/logout", methods=["GET"])
def logout():
  if g.user is not None:
    session.pop("user_id", None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET"])
def home():
  if g.user is None:
    return redirect(url_for('index'))
  return render_template("home.html")

@app.route("/home/search", methods=["GET"])
def search():
  pass

