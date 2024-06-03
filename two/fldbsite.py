from flask import (Flask, render_template, url_for, request, flash, session,
                   redirect, g)
import os
import sqlite3
from FDataBase import FDataBase

DATABASE = 'flsk.db'
DEBUG = True
SECRET_KEY = "033dc051ec2c8ef6225617118e951c2761c50648"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.get_menu())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.errorhandler(404)
def page_not_found(error):
    # print(error)
    return render_template("page404.html", title='Станица не найдена', menu=[])


if __name__ == '__main__':
    app.run()
