import pandas as pd
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

books = pd.read_csv('books.csv')

for i, book in books.iterrows():

    title = book['title'].replace("\'", '')
    author = book['author'].replace("\'", '')
    query = f"""INSERT INTO books (isbn, author, title, year) VALUES ('{book['isbn']}', '{author}','{title}',{book['year']})"""
    db.execute(query)


db.commit()