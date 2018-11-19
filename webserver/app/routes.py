from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from app import app, engine
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from config import Config
import datetime



@app.route('/')
def home():
    product_brand = engine.execute("""
                SELECT pid, p.name as product_name, b.name as brand_name, price
                FROM products as p, brands as b
                WHERE p.bid = b.bid;
                """)
    # print(product_brand.keys())
    return render_template('index.html', products=product_brand, login="Log In", username='')
    
@app.route('/index/<username>')
def index(username):
    product_brand = engine.execute("""
                    SELECT pid, p.name as product_name, b.name as brand_name, price
                    FROM products as p, brands as b
                    WHERE p.bid = b.bid;
                    """)

    return render_template('index.html', products=product_brand, login="Log Out", username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(engine, form.username.data)
        if user is None or user.password != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        user = Customer(user)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index', username=form.username.data))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

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

@app.route('/product/<int:pid>')
def product(pid):
    product = engine.execute("""
    select * from products 
    where pid = '%s'
    """ % (pid)).fetchone()
    # comments = engine.execute("""
    # SELECT * from place_order as p, comments_followed as c
    # WHERE p.oid = c.oid and p.pid = '%s'
    # """ % (pid))
    # print(comments.keys())
    return render_template('product.html', product=product)

@app.route('/profile/<username>')
def profile(username):
    print(username, type(username))
    user = find_user(engine, username)
    user = Customer(user)
    orders = engine.execute("""
    SELECT name, oid, price , p.pid as pid 
    from place_order as o, products as p
    where o.uid = '%s' and p.pid = o. pid;
    """%(user.uid))
    return render_template('profile.html', user = user, orders = orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = []
    return render_template('checkout.html', cart=cart)



