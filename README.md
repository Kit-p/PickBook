# Project 1

Web Programming with Python and JavaScript

# Author

Kit-p

# Description

~~App deployed at: https://pickbook-kitp.herokuapp.com/~~  
App no longer deployed due to the recent Heroku policy changes, i.e., removing the free tier Heroku-18 stack.

This project intends to build a web application that allows users to search for and write reviews for books. It will contain log-in system and be connected with database, while also providing public API access methods.

# Objectives

1. Use SQL, Python, and HTML to create a web application.
2. Make use of tools like SQLAlchemy, Flask, and Jinja2 to facilitate functionality.
3. Practise using database, back-end web server, Git and GitHub.
4. Providing API access for the web application.

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
- Duplicated account or invalid credentials handled

**`home.html`**  
This is the home page after user logged in.  
It allows user to search for books.  
*----------Tasks Accomplished----------*  
- Logged in users can logout
- Logged in users can search for books
  - by Title
  - by Author
  - by ISBN

**`search.html`**  
This is the page displaying search results.  
It links users to specific book details page.  
Users can navigate between result pages.  
*----------Tasks Accomplished----------*  
- Displayed search results
- Linked users to specific book page
- Handled all combination of search queries

**`book.html`**  
This is the page displaying book details.  
It contains reviews written for the specific book.  
Users can write and submit new review here.  
It contains Goodreads data for the specific book.  
*----------Tasks Accomplished----------*  
- Displayed title, author, publication year and ISBN of book
- Displayed book reviews by all users
- Displayed statistics from *Goodreads*
- Users logged in can submit reviews
  - Including a rating scale of 1 to 5
  - Including a text segment
  - Constraint of 1 review per book per user handled

**`application.py`**  
This is the Flask app.  
It contains all the code for supporting the functionalities listed above.  
It connects to the postgreSQL database and handle data querying.  
It provides API access at route `/api/<isbn>`.  
*----------Tasks Accomplished----------*  
- Provided API access of book data in `JSON` format
- Returned `404` error for invalid ISBN
- Constraint of raw SQL only (no ORM used)

**`requirements.txt`**  
This is a list of Python packages required to run the Flask app.  
*----------Tasks Accomplished----------*  
- Listed all package requirements

**`README.md`**  
This is the current file.  
It includes brief description of the project and each file.  
*----------Tasks Accomplished----------*  
- Described project
- Described each file

# Resources

~~Heroku (database & app): https://www.heroku.com/~~  
Adminer (database management): https://adminer.cs50.net/  
Goodreads (api): https://www.goodreads.com/api  
