import sqlite3
from flask import Flask

app = Flask(__name__)

def setup_database():
    # Mettez ici le code pour recharger votre base de données
    db = connect_db()
    db.cursor().execute('DROP TABLE IF EXISTS comments')
    db.cursor().execute('DROP TABLE IF EXISTS users')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS comments '
                        '(id INTEGER PRIMARY KEY, '
                        'comment TEXT)')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS users '
                        '(id INTEGER PRIMARY KEY, '
                        'username TEXT, '
                        'password TEXT, '
                        'isadmin BOOLEAN)')
    db.commit()
    db.close()

def connect_db():
    db = sqlite3.connect('database.db')
    return db

def add_user(username, password, isadmin):
    db = connect_db()
    db.cursor().execute('INSERT INTO users (username, password, isadmin) '
                        'VALUES (?, ?, ?)', (username, password, isadmin,))
    db.commit()
    db.close()

def get_users():
    db = connect_db()
    get_all_query = 'SELECT username, password, isadmin FROM users'
    results = db.cursor().execute(get_all_query).fetchall()
    db.close()
    return results

def add_comment(comment):
    db = connect_db()
    db.cursor().execute('INSERT INTO comments (comment) '
                        'VALUES (?)', (comment,))
    db.commit()
    db.close()

def get_comments(search_query=None):
    db = connect_db()
    results = []
    get_all_query = 'SELECT comment FROM comments'
    for (comment,) in db.cursor().execute(get_all_query).fetchall():
        if search_query is None or search_query in comment:
            results.append(comment)
    db.close()
    return results

# Vos routes et autres configurations Flask ici
