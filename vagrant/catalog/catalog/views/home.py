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
from flask import url_for, render_template, redirect
from flask.ext.login import login_user, logout_user

from catalog import app, db
from catalog.forms import EmailPasswordForm, UserForm, CategoryForm, ItemForm
from catalog.models import Category, Item, User


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', action="Sign",
                           data_type="up",
                           form_action='signup',
                           form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
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
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        pass
    return render_template("category.html", action="Add",
                           data_type="a category",
                           form_action='new_category',
                           form=form)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.filte_by(id=category_id).one()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        pass
    return render_template("category.html", action="Edit",
                           data_type=category.name,
                           form_action='edit_category', form=form)


@app.route('/item/new', methods=['GET', 'POST'])
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
