# Project 1

Web Programming with Python and JavaScript

# Author

Kit-p

# Description

This project intends to build a web application that allows users to search for and write reviews for books. It will contain log-in system and be connected with database, while also providing public API access methods.

# Objectives

1. Use SQL, Python, and HTML to create a web application.
2. Make use of tools like SQLAlchemy, Flask, and Jinja2 to facilitate functionality.
3. Practise using database, back-end web server, Git and GitHub.
4. Creating API access for the web application.

# Files

**`books.csv`**  
This is the initial records of books.  
It contains 5000 entries of books with `isbn`, `title`, `author`, and `year`.  

**`import.py`**  
This is the `.py` file that creates necessary relational tables.  
It reads data from `.csv` file and insert them into the corresponding table.  
*----------Tasks Accomplished----------*  
- Created `import.py`
- Created 3 relational tables `reader`, `book`, and `review`
- Read data from `books.csv` and insert them into the table `book`

**`layout.html`**  
This is the template for all other `.html` files.  
It contains basic structure of a HTML page.  
It defines header for non-logged-in and logged-in pages.  

**`success.html`**  
This is the template for all Success messages.  
It displays a simple page with the variable `message`.  
It greets the user with the corresponding variable `username`.  

**`error.html`**  
This is the template for all Error messages.  
It displays a simple page with the variable `message`.  
It describes the error leading to this page.  

**`index.html`**  
This is the default login page.  
It allows user to register or login with username and password.  
It makes `POST` request to url_for('register') or url_for('login').  
It verifies account duplication or invalid credentials by `application.py`.  
*----------Tasks Accomplished----------*  
- Users can register with username and password
- Users can login with a username and password
- Users logged in are redirected to `home.html`

**`home.html`**  
This is the home page after user logged in.  
It allows user to search for books.  
*----------Tasks Accomplished----------*  
- Logged in users can logout
- Logged in users can search for books
  - by Title
  - by Author
  - by ISBN

