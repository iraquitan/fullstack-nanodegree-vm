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
from flask import url_for, render_template, redirect, request, session, \
    abort, flash, Blueprint, current_app, make_response
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy import desc
from catalog import app, db
from catalog.auth import OAuthSignIn
from catalog.forms import EmailPasswordForm, UserForm
from catalog.models import Category, Item, User, UserSocialProfile

# Define home Blueprint
home = Blueprint('home', __name__)


# Generate CSRF token to be used for CSRF check, add a session state key
def generate_csrf_token():
    if 'state' not in session:
        session['state'] = random_string()
    return session['state']


# Function to generate random string
def random_string():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for x in xrange(32))
    return state


@home.route('/')
@home.route('/index')
def index():
    categories = Category.query.all()
    # Recent added items ordered by date_created in descending order
    recent_items = Item.query.order_by(desc('date_created')).limit(10)
    return render_template('home/index.html', categories=categories,
                           items=recent_items)


@home.route('/signup', methods=["GET", "POST"])
def signup():
    # Check if current user is anonymous, else send to index page
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    # Use the defined UserForm
    form = UserForm()
    if form.validate_on_submit():  # Add user to database if validate
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
    # Check if current user is anonymous, else send to index page
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    # Use the defined EmailPasswordForm
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        # Check if sent form password is correct
        if user.is_correct_password(form.password.data):
            # Define the login session key to internal login not oauth provider
            session['login'] = 'internal'
            login_user(user, True)  # Login the user using Flask-Login
            return redirect(url_for('home.index'))
    return render_template('home/login.html', action="Login",
                           form_action='home.login',
                           form=form)


@home.route('/logout')
@login_required
def logout():
    if session.get('login'):
        del session['login']  # Delete session login key (provider)
    logout_user()  # Logout user using Flask-Login
    flash("You are now logged out", category='success')
    return redirect(url_for('home.index'))


@home.route('/callback/<provider>', methods=['POST'])
def oauth_callback(provider):
    # Check if current user is anonymous, else send to index page
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    # CSRF token check
    token = session.pop('state', None)
    if not token or token != request.args.get('state'):
        abort(403)
    # Get Oauth Class defined in auth.py for provider
    oauth = OAuthSignIn.get_provider(provider)
    # If user already signed in the response is not a code, it's the user email
    user = User.query.filter_by(email=request.data).first()
    if user:  # If user is signed up, login
        session['login'] = provider  # Set a session login key to provider
        login_user(user, True)  # Login user using Flask-Login
    else:  # If response is code
        user_info, social_info = oauth.callback()  # Try to retrieve user info
        if user_info is None:  # If retrieve fail flash and return to login
            flash('Authentication failed.', category='error')
            return redirect(url_for('home.login'))
        # Search user by retrieved email info
        user = User.query.filter_by(email=user_info[1]).first()
        if not user:  # If not user, signed up
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
        else:  # If user signed up, add social profile to user social table
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
        login_user(user, True)  # Login user using Flask-Login
    flash("You are now logged in as {}".format(user.name), category='success')
    output = ''
    output += '<h1>Welcome, '
    output += user.name
    output += '!</h1>'
    output += '<img src="'
    output += user.picture
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    return output


# A route for generating sitemap.xml for static, categories and items pages
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
      url = url_for('profile.item_profile', item_slug=item.slugfield)
      picture_url = item.picture
      picture_caption = item.name
      modified_time = item.last_updated.strftime("%Y-%m-%d")
      item_pages.append((url, picture_url, picture_caption, modified_time))

    # items model pages
    categories = Category.query.order_by(Category.last_updated).all()
    for category in categories:
      url = url_for('profile.category_items', category_slug=category.slugfield)
      modified_time = item.last_updated.strftime("%Y-%m-%d")
      category_pages.append((url, modified_time))

    sitemap_xml = render_template('home/sitemap_template.xml', statics=pages,
                                  items=item_pages, categories=category_pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
