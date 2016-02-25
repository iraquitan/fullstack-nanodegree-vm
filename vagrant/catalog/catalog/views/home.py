# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: home
 * Date: 2/23/16
 * Time: 15:33
 * To change this templates use File | Settings | File Templates.
"""
import json
import random
import string

import crypt
import httplib2
from flask import url_for, render_template, redirect, request, session, abort, \
    make_response, flash
from flask.ext.login import login_user, logout_user, login_required
from oauth2client import client
from oauth2client.client import FlowExchangeError

from catalog import app, db
from catalog.forms import EmailPasswordForm, UserForm, CategoryForm, ItemForm
from catalog.models import Category, Item, User


# @app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = random_string()
    return session['_csrf_token']


def random_string():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for x in xrange(32))
    return state


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', action="Sign up",
                           form_action='signup',
                           form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', action="Login",
                           form_action='login',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.all()
    recent_items = Item.query.order_by('date_created').all()
    return render_template('index.html', categories=categories,
                           items=recent_items)


@app.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        pass
    return render_template("category.html", action="Add",
                           data_type="a category",
                           form_action='new_category',
                           form=form)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.filte_by(id=category_id).one()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        pass
    return render_template("category.html", action="Edit",
                           data_type=category.name,
                           form_action='edit_category', form=form)


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    categories = Category.query.all()
    if categories:
        form.category.choices = [(cat.id, cat.name) for cat in categories]
    else:
        form.category.choices = [(0, 'None')]
    if form.validate_on_submit():
        pass

    return render_template("item.html", action="Add",
                           data_type="an item",
                           form_action='new_item',
                           form=form)


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.filter_by(id=item_id).one()
    form = ItemForm(obj=item)
    categories = Category.query.all()
    if categories:
        form.category.choices = [(cat.id, cat.name) for cat in categories]
    else:
        form.category.choices = [(0, 'None')]
    if form.validate_on_submit():
        pass
    return render_template('item.html', action='Edit',
                           data_type=item.name,
                           form_action='edit_item',
                           form=form)


@app.route('/google_signin', methods=['POST'])
def google_signin():
    # Validate CSRF Token
    if request.args.get('_csrf_token') != session['_csrf_token']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    auth_code = request.data
    try:
        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            app.config['GOOGLE_CLIENT_SECRETS'],
            ['profile', 'email'],
            auth_code)
        # flow = client.flow_from_clientsecrets(
        #     'client_secrets.json',
        #     scope='',
        #     redirect_uri='postmessage')
        # credentials = flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to exchange authorization code.'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    # Get profile info from ID token
    userid = credentials.id_token['sub']
    email = credentials.id_token['email']
    output = ''
    output += '<h1>Welcome, '
    # output += login_session['username']
    # output += '!</h1>'
    # output += '<img src="'
    # output += login_session['picture']
    # output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("You are now logged in as {}".format(email))
    return output
