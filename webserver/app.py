from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import render_template, flash, redirect, url_for, request, g

# from app.models import *
from config import Config
import datetime
from sqlalchemy import *
import os

app = Flask(__name__)

DB_USER = "ll3235"
DB_PASSWORD = "tf7uykkz"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

username = None
password = None
# for row in result:
#     print(row['username'] == "peiwenliu")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = "peiwenliu"
    password = None
    result = engine.execute("""SELECT username, password from users;""")
    for row in result:
        if (row['username'].encode('ascii', 'ignore') == username
                and row['password'].encode('ascii', 'ignore') == password):
            return render_template("index.html")
    print("Incorrect Username")
    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return render_template("index.html")

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    return render_template("checkout.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False, host='0.0.0.0', port=4000)