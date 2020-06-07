import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def create_table(db, tname, columns, constraints=None):
  sql = f"CREATE TABLE IF NOT EXISTS {tname}("
  msg = f"Created table {tname}("
  for cname, cprop in columns.items():
    sql += f"  {cname} {cprop},"
    msg += f"{cname}, "
  if constraints is not None:
    for constraint in constraints:
      sql += f"  {constraint},"
  sql = sql[:-1]
  sql += ");"
  msg = msg[:-2]
  msg += ")."
  db.execute(sql)
  db.commit()
  print(msg)


def main():
  if not os.getenv("DATABASE_URL"):
    raise Exception("DATABASE_URL is not set")

  f = open("books.csv")
  if not f:
    raise Exception("books.csv is not found")
  reader = csv.reader(f)

  engine = create_engine(os.getenv("DATABASE_URL"))
  db = scoped_session(sessionmaker(bind=engine))

  columns = {
    "id": "SERIAL PRIMARY KEY",
    "username": "VARCHAR UNIQUE NOT NULL",
    "password": "VARCHAR NOT NULL"
  }
  create_table(db, "reader", columns)

  columns = {
    "id": "SERIAL PRIMARY KEY",
    "isbn": "VARCHAR UNIQUE NOT NULL",
    "title": "VARCHAR NOT NULL",
    "author": "VARCHAR",
    "year": "INTEGER"
  }
  create_table(db, "book", columns)

  columns = {
    "reader_id": "INTEGER REFERENCES reader",
    "book_id": "INTEGER REFERENCES book",
    "rating": "INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)",
    "content": "VARCHAR"
  }
  constraints = [
    "PRIMARY KEY (reader_id, book_id)"
  ]
  create_table(db, "review", columns, constraints)
    
  print("\nAll tables created.\n")
  print("Start inserting records...\n")

  sql = (
    "INSERT INTO book (isbn, title, author, year) VALUES (:isbn, :title, :author, :year);"
  )
  for isbn, title, author, year in reader:
    try:
      year = int(year)
    except ValueError:
      continue
    isbn = isbn.strip().replace('-', '').replace(' ', '')
    result = db.execute(sql, {"isbn": isbn, "title": title, "author": author, "year": year})
    print(f"Inserted record into BOOK with isbn({isbn}).")

  db.commit()

  print("\nAll records from books.csv are inserted.\n")



if __name__ == "__main__":
  main()