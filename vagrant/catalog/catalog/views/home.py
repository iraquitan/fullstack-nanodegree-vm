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
import random
import string

from datetime import datetime, timedelta
from flask import url_for, render_template, redirect, request, session, \
    abort, flash, Blueprint, current_app, make_response
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy import desc

from catalog import app, db
from catalog.auth import OAuthSignIn
from catalog.forms import EmailPasswordForm, UserForm
from catalog.models import Category, Item, User, UserSocialProfile

home = Blueprint('home', __name__)


# @app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('state', None)
        if not token or token != request.form.get('state'):
            abort(403)


def generate_csrf_token():
    if 'state' not in session:
        session['state'] = random_string()
    return session['state']


def random_string():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for x in xrange(32))
    return state


@home.route('/')
@home.route('/index')
def index():
    categories = Category.query.all()
    recent_items = Item.query.order_by(desc('date_created')).limit(10)
    return render_template('home/index.html', categories=categories,
                           items=recent_items)


@home.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,
                    password=form.password.data, picture=form.picture.data)
        db.session.add(user)
        db.session.commit()
        if app.debug:
            app.logger.debug("User {} signed up!".format(
                (user.id, user.name)))
        flash("You are now signed up. Please login to your account",
              category='success')
        return redirect(url_for('home.index'))

    return render_template('home/signup.html', action="Sign up",
                           form_action='home.signup',
                           form=form)


@home.route('/login', methods=["GET", "POST"])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            session['login'] = 'internal'
            login_user(user, True)
            return redirect(url_for('home.index'))
    return render_template('home/login.html', action="Login",
                           form_action='home.login',
                           form=form)


@home.route('/logout')
@login_required
def logout():
    if session.get('login'):
        del session['login']
    logout_user()
    flash("You are now logged out", category='success')
    return redirect(url_for('home.index'))


@home.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    token = session.pop('state', None)
    if not token or token != request.args.get('state'):
        abort(403)
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@home.route('/callback/<provider>', methods=['POST'])
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    token = session.pop('state', None)
    if not token or token != request.args.get('state'):
        abort(403)
    oauth = OAuthSignIn.get_provider(provider)
    user = User.query.filter_by(email=request.data).first()
    if user:
        session['login'] = provider
        login_user(user, True)
    else:
        user_info, social_info = oauth.callback()
        if user_info is None:
            flash('Authentication failed.', category='error')
            return redirect(url_for('home.index'))
        user = User.query.filter_by(email=user_info[1]).first()
        if not user:
            user = User(name=user_info[0], email=user_info[1],
                        picture=user_info[2])
            db.session.add(user)
            db.session.flush()
            social = UserSocialProfile(provider=social_info[0],
                                       social_id=social_info[1],
                                       profile=social_info[2], user_id=user.id)
            db.session.add(social)
            db.session.commit()
            if app.debug:
                app.logger.debug("User {} signed up!".format(
                    (user.id, user.name)))
        else:
            social = UserSocialProfile.query.filter_by(
                social_id=social_info[1]).first()
            if not social:
                social = UserSocialProfile(provider=social_info[0],
                                           social_id=social_info[1],
                                           profile=social_info[2], user_id=user.id)
                db.session.add(social)
                db.session.commit()
                if app.debug:
                    app.logger.debug("User {0} signed in with {1}!".format(
                        (user.id, user.name), social.provider))
        login_user(user, True)
    flash("You are now logged in as {}".format(user.name), category='success')
    output = ''
    output += '<h1>Welcome, '
    output += user.name
    output += '!</h1>'
    output += '<img src="'
    output += user.picture
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    return output


# a route for generating sitemap.xml for static, categories and items pages
@home.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []
    item_pages = []
    category_pages = []
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(rule.rule)

    # items model pages
    items = Item.query.order_by(Item.last_updated).all()
    for item in items:
      url = url_for('profile.item_profile', item_id=item.id)
      picture_url = item.picture
      picture_caption = item.name
      modified_time = item.last_updated.strftime("%Y-%m-%d")
      item_pages.append((url, picture_url, picture_caption, modified_time))

    # items model pages
    categories = Category.query.order_by(Category.last_updated).all()
    for category in categories:
      url = url_for('profile.category_items', category_id=category.id)
      modified_time = item.last_updated.strftime("%Y-%m-%d")
      category_pages.append((url, modified_time))

    sitemap_xml = render_template('home/sitemap_template.xml', statics=pages,
                                  items=item_pages, categories=category_pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
