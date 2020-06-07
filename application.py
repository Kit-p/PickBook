import os

from flask import Flask, session, render_template, request
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

@app.route("/register", methods=["POST"])
def register():
  global db
  username = request.form.get("username")
  password = request.form.get("password")
  users = db.execute("SELECT * FROM reader WHERE reader.username = :username", {"username": username})
  if users.rowcount != 0:
    return render_template("error.html", message=f"The username '{username}' has been used!")
  db.execute("INSERT INTO reader (username, password) VALUES (:username, :password)", {"username": username, "password": password})
  db.commit()
  return render_template("success.html", message="Registration Successful!", username=username)

@app.route("/login", methods=["POST"])
def login():
  pass

@app.route("/home")
def home():
  pass

