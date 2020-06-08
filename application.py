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
  if g.user is None:
    return redirect(url_for('index'))

  global db
  limit = 50
  index = {}
  page = {}
  isbn = request.args.get("isbn", default="", type=str)
  title = request.args.get("title", default="", type=str)
  author = request.args.get("author", default="", type=str)
  page["current"] = request.args.get("page", default=None, type=int)

  if page["current"] is None:
    return redirect(request.full_path + "&page=1")

  offset = (page["current"]-1) * limit
  index["low"] = offset + 1
  books = None
  sql_clause = " FROM book"
  params = None

  if title != "" or author != "" or isbn != "":
    sql_clause += " WHERE "
    params = {}
    if isbn != "":
      sql_clause += "isbn ~~* :isbn AND "
      params["isbn"] = '%' + isbn.strip().replace('-', '').replace(' ', '') + '%'
    if title != "":
      sql_clause += "title ~~* :title AND "
      params["title"] = '%' + title.strip() + '%'
    if author != "":
      sql_clause += "author ~~* :author AND "
      params["author"] = '%' + author.strip() + '%'
    sql_clause = sql_clause[:-5]

  sql = "SELECT COUNT(id) AS total" + sql_clause + ';'

  if params is not None:
    index["total"] = db.execute(sql, params).fetchone().total
  else:
    index["total"] = db.execute(sql).fetchone().total

  page["total"] = -(-index["total"] // limit) # round_up

  if index["total"] == 0:
    index["low"] = 0
    page["total"] = 1

  if title != "" or author != "" or isbn != "":
    sql_clause += " ORDER BY "
    if title != "":
      sql_clause += "LENGTH(title), "
    if author != "":
      sql_clause += "LENGTH(author), "
    if isbn != "":
      sql_clause += "isbn, "
    sql_clause = sql_clause[:-2]

  sql = "SELECT id, title, author, isbn" + sql_clause + f" LIMIT {limit} OFFSET {offset};"

  if params is not None:
    books = db.execute(sql, params)
  else:
    books = db.execute(sql)

  index["high"] = offset + books.rowcount

  params = {}
  params["title"] = title.strip()
  params["author"] = author.strip()
  params["isbn"] = isbn.strip()

  urls = {}
  base_url = request.full_path.rstrip("0123456789")
  if page["current"] > 1:
    urls["first"] = base_url + "1"
    urls["previous"] = base_url + str(page["current"] - 1)
  if page["current"] < page["total"]:
    urls["next"] = base_url + str(page["current"] + 1)
    urls["last"] = base_url + str(page["total"])

  return render_template("search.html", page=page, index=index, books=books, params=params, urls=urls)

@app.route("/home/book/<int:id>", methods=["GET"])
def book(id):
  pass

