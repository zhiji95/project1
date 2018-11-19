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
    product_brand = engine.execute("""
        with product_brand(pid, price, product_name, brand_name) as
        (select pid, price, products.name as product_name, brands.name as brand_name 
        from products, brands
        where products.bid = brands.bid)
        select p.pid, price, product_name,brand_name, avg(c.rating) as rating 
        from product_brand as p, comments_followed_post as c, place_order as o 
        where p.pid = o.pid and o.oid = c.oid
        group by p.pid, price, product_name, brand_name;
        """)


    print(product_brand.keys())
    return render_template('index.html', products=product_brand)
@app.route('/index')
def index():
    products = engine.execute("""
    select * 
    from products
    """)
    print(products.keys())
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(engine, form.username.data)

        if user is None or user.password != form.password.data:
        	flash('Invalid username or password')
        	return redirect(url_for('login'))
        user = User(user)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        uid = engine.execute("""
                select max(uid) 
                from users
                """).fetchone()[0] + 1
        insert(
            engine, "user", uid,
            phone_number=form.phone_number,
            address = form.birthday,
            gender = form.gender,
            birth_date = form.birthday,
            password = form.password,
            username = form.username)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = []
    return render_template('checkout.html', cart=cart)
# @app.route("/logout")
# def logout():



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False, host='0.0.0.0', port=4000)