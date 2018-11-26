from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from app import app, engine
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
import datetime
from config import Config
import datetime



@app.route('/', methods=['GET', 'POST'])
def home():
    product_brand = get_product_brand(engine)
    return render_template('index.html', products=product_brand, login="Log In", username='')
    

@app.route('/index/<username>', methods=['GET', 'POST'])
def index(username):
    product_brand = get_product_brand(engine)
    if request.method == 'POST' and 'search' in request.form:
        keyword = request.form['search'].lower()
        product_brand = search_product(engine, keyword)

        
    return render_template('index.html', products=product_brand, login="Log Out", username=username)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    form = ManagerForm()

    if form.validate_on_submit():
        brand = engine.execute("""Select bid from brands where brands.name = '%s';"""%(form.brand)).fetchone()
        print(brand)
        if brand == None:
            brand_id = engine.execute("""
			SELECT max(bid)
			FROM brands
			""" ).fetchone()[0]+1
            engine.execute("""
            INSERT INTO brands
            values('%s', '%s', 'No Description');
            """%(brand_id, form.brand.data))
        else:
            brand_id = brand[0]

        product_id =  engine.execute("""
			SELECT max(pid)
			FROM products
			""").fetchone()[0]+1
        engine.execute("""
        INSERT INTO products
        VALUES ('%s','%s','%s','%s');
        """%(product_id, brand_id,form.price.data, form.name.data))
        return redirect(url_for('home'))
    return render_template('manager.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username, form.password)
        if form.username.data in ["zhiji", "linnanli", "zphですよ"] and form.password.data == "coms4111":
            return redirect(url_for('manager'))
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
        uid = add_id(engine, 'uid', 'users')
        insert(
            engine, "users", uid,
            phone_number=form.phone_number.data,
            address = form.birthday.data,
            gender = form.gender.data,
            birth_date = form.birthday.data,
            password = form.password.data,
            username = form.username.data)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/product/<int:pid>',methods=['GET', 'POST'])
def product(pid):
    username = request.args.get('username', None)
    print(username)
    form = ProductForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = find_user(engine, username)
        user = Customer(user)
        insert_to_cart(engine, pid, user.uid, form.quantity.data, time)

    product = get_products(engine, pid)
    comments = get_comments(engine, pid)
    print(comments.keys())
    return render_template('product.html', product=product, comments=comments, form=form, username=username)


@app.route('/profile/<username>',methods=['GET', 'POST'])
def profile(username):
    user = find_user(engine, username)
    user = Customer(user)
    form = ProfileForm()

    if form.validate_on_submit():
        cid = add_id(engine, 'cid', 'comments_followed_post')
        print(cid, form.oid.data, user.uid, form.pid.data, form.comment.data,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), form.rating.data)
        print(engine.execute('select * from comments_followed_post').keys())
        insert_to_comments(engine, cid, form.oid.data, user.uid, form.pid.data, form.comment.data, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), form.rating.data)
        
    orders = get_orders(engine, user.uid)
    return render_template('profile.html', user=user, orders=orders, form=form)


@app.route('/cart/<username>',methods=['GET', 'POST'])
def cart(username):
    form = CartForm()
    user = find_user(engine, username)
    user = Customer(user)

    if form.validate_on_submit():
        delete_item_in_cart(engine, form.uid.data, form.pid.data)
        redirect(url_for('cart', username = user.username))

    items = get_item_to_checkout(engine, user.uid)
    return render_template('cart.html', user=user, items=items, form = form)


@app.route('/payment/<username>',methods=['GET', 'POST'])
def payment(username):
    user = find_user(engine, username)
    user = Customer(user)
    form = PaymentForm()

    if form.validate_on_submit():
        method_id = add_id(engine, 'method_id', 'user_payment')
        add_method(engine, form.payphone.data, form.account.data, form.paybank.data, form.billaddress.data, form.payname.data, user.uid, method_id)
        redirect(url_for('payment', username=username))

    payments = find_address(engine, user.uid)
    return render_template('payment.html', payments=payments, username=username, form=form)

@app.route('/checkout/<username>', methods=['GET', 'POST'])
def checkout(username):
    """
    TODO 1. 写一个返回总价格的sql放给checkout 2. if items_new is None and items is not none, remove all items in cart and insert them into order"""
    user = find_user(engine, username)
    user = Customer(user)
    items = get_item_to_checkout(engine, user.uid)
    items_new = items
    price = request.args.get('price', 1000)
    avaliable_payments = find_address(engine, user.uid)
    payment_list = [(str(p['uid']), str(p['account_number'])) for p in avaliable_payments]
    form = CheckoutForm()
    form.payments.choices = payment_list

    if request.method == "POST" and "placeorder" in request.form:
        new_items = list(items_new)
        # delete your items from your cart
        for i in new_items:
            print(i)
            oid = add_id(engine, 'oid', 'place_order')
            item_to_add = get_item_in_cart(engine, user.uid, i[0])
            add_order(engine, oid, user.uid, i[0], i[2])
            delete_item_in_cart(engine, user.uid, i[0])
        return redirect(url_for("placeorder", username=username, items=new_items))

    return render_template('checkout.html',items=items_new, price=price, username=username, form=form)


@app.route('/placeorder/<username>/<items>', methods=['GET', 'POST'])
def placeorder(username, items):
    items = eval(items)
    print(items[0])
    return render_template('choose_payment.html', username=username, items=items)

