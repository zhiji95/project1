from flask import flash, url_for, g
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegistrationForm
from models import *
from sqlalchemy import *
import os
from flask_login import LoginManager
app = Flask(__name__)
DB_USER = "ll3235"
DB_PASSWORD = "tf7uykkz"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)
login = LoginManager(app)


@app.route('/')
def home():
    return render_template('index.html', title='Home')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = find_user(engine, form.username.data)

        if user is None or user.password != form.password.data:
        	flash('Invalid username or password')
        	return redirect(url_for('login'))
        user = User(user)
        login_user(user, remember = form.remember_me.data) 
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


# @app.route("/logout")
# def logout():



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False, host='0.0.0.0', port=4000)