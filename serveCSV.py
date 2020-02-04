from flask import Flask, request
from flask import g
from flask import render_template
import sqlite3
import datetime

app = Flask(__name__)

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def serveCSV():
    cur = get_db().cursor()
    cur.execute("select * from data")
    data = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    cur.close()
    return render_template("view.html", data=data, col_names=col_names)


@app.route("/logs")
def serveLogs():
    cur = get_db().cursor()
    cur.execute("select * from logs")
    data = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    cur.close()
    return render_template("view.html", data=data, col_names=col_names)


@app.before_request
def log_request():
    method = request.method
    client = request.remote_addr
    date = str(datetime.datetime.now())

    cur = get_db().cursor()
    cur.execute("INSERT INTO logs(method,client,datetime) VALUES (?,?,?)", (method, client, date))
    cur.close()
    get_db().commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
