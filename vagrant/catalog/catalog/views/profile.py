# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: profile
 * Date: 2/25/16
 * Time: 14:28
 * To change this template use File | Settings | File Templates.
"""
from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required

from catalog import db, app
from catalog.forms import CategoryForm, ItemForm, DeleteForm
from catalog.models import Category, Item, User

profile = Blueprint('profile', __name__)


@profile.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Category {} added!".format(
                    (new_category.id, new_category.name)
                )
            )
        flash("Category {} added!".format(
            (new_category.id, new_category.name))
        )
        return redirect(url_for('home.index'))
    return render_template("profile/category.html", action="Add",
                           data_type="a category",
                           form_action='profile.new_category',
                           form=form)


@profile.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.filter_by(id=category_id).one()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Category {} edited!".format(
                    (category.id, category.name)
                )
            )
        flash("Category {} edited!".format(
            (category.id, category.name))
        )
        return redirect(url_for('home.index'))
    return render_template("profile/category.html", action="Edit",
                           data_type=category,
                           form_action='profile.edit_category', form=form)


@profile.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).one()
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(category)
        db.session.commit()
        if app.debug:
            app.logger.debug("Category {} deleted!".format(
                (category.id, category.name)))
        flash("Category {} deleted!".format(
            (category.id, category.name)))
        return redirect(url_for('home.index'))
    else:
        return render_template('profile/delete.html', form=form,
                               action='category',
                               form_action='profile.delete_category',
                               object=category)


@profile.route('/item/<int:item_id>')
def item_profile(item_id):
    item = Item.query.filter_by(id=item_id).one()
    owner = User.query.filter_by(id=item.user_id).one()
    return render_template('profile/item_profile.html', item=item, owner=owner)


@profile.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    categories = Category.query.all()
    if categories:
        form.category.choices = [(cat.id, cat.name) for cat in categories]
    else:
        form.category.choices = [(0, 'None')]
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).one()
        new_item = Item(name=form.name.data, description=form.description.data,
                        picture=form.picture.data, category=category)
        db.session.add(new_item)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Item {} added!".format(
                    (new_item.id, new_item.name)
                )
            )
        flash("Item {} added!".format(
            (new_item.id, new_item.name))
        )
        return redirect(url_for('home.index'))
    return render_template("profile/item.html", action="Add",
                           data_type="an item",
                           form_action='profile.new_item',
                           form=form)


@profile.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
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
        category = Category.query.filter_by(id=form.category.data).one()
        item.name = form.name.data
        item.description = form.description.data
        item.picture = form.picture.data
        item.category = category
        db.session.add(item)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Item {} edited!".format(
                    (item.id, item.name)
                )
            )
        flash("Item {} edited!".format(
            (item.id, item.name))
        )
        return redirect(url_for('home.index'))
    return render_template('profile/item.html', action='Edit',
                           data_type=item,
                           form_action='profile.edit_item',
                           form=form)


@profile.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id).one()
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        if app.debug:
            app.logger.debug("Item {} deleted!".format(
                (item.id, item.name)))
        flash("Category {} deleted!".format(
            (item.id, item.name)))
        return redirect(url_for('home.index'))
    else:
        return render_template('profile/delete.html', form=form,
                               action='item',
                               form_action='profile.delete_item',
                               object=item)
