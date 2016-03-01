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
from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from catalog import db, app
from catalog.forms import CategoryForm, ItemForm, DeleteForm, UserForm
from catalog.models import Category, Item, User

profile = Blueprint('profile', __name__)


@profile.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data, user=current_user)
        db.session.add(new_category)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Category {} added!".format(
                    (new_category.id, new_category.name)
                )
            )
        flash("Category {} added!".format(
            (new_category.id, new_category.name)), 'success'
        )
        return redirect(url_for('home.index'))
    return render_template("profile/category.html", action="Add",
                           data_type="a category",
                           form_action='profile.new_category',
                           form=form)


@profile.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    owner = category.user
    if current_user.id != owner.id:
        flash("You are not authorized to edit this category. "
              "Please create your own category in order to edit.", 'warning')
        return redirect(url_for('home.index'))
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
            (category.id, category.name)), 'success'
        )
        return redirect(url_for('home.index'))
    return render_template("profile/category.html", action="Edit",
                           data_type=category,
                           form_action='profile.edit_category', form=form)


@profile.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    owner = category.user
    if current_user.id != owner.id:
        flash("You are not authorized to delete this category. "
              "Please create your own category in order to delete.", 'warning')
        return redirect(url_for('home.index'))
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(category)
        db.session.commit()
        if app.debug:
            app.logger.debug("Category {} deleted!".format(
                (category.id, category.name)))
        flash("Category {} deleted!".format(
            (category.id, category.name)), 'success')
        return redirect(url_for('home.index'))
    else:
        return render_template('profile/delete.html', form=form,
                               action='category',
                               form_action='profile.delete_category',
                               object=category)


@profile.route('/category/<int:category_id>', defaults={'page': 1})
@profile.route('/category/<int:category_id>/page/<int:page>')
def category_items(category_id, page):
    categories = Category.query.all()
    sel_category = Category.query.filter_by(id=category_id).first_or_404()
    items = Item.query.filter_by(category_id=category_id).order_by('name').paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    if not items and page != 1:
        abort(404)
    return render_template('profile/category_items.html', pagination=items,
                           items=items.items, sel_category=sel_category,
                           categories=categories)


@profile.route('/item/<int:item_id>')
def item_profile(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    owner = User.query.filter_by(id=item.user_id).first_or_404()
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
        category = Category.query.filter_by(id=form.category.data).first_or_404()
        new_item = Item(name=form.name.data, description=form.description.data,
                        picture=form.picture.data, category=category,
                        user=current_user)
        db.session.add(new_item)
        db.session.commit()
        if app.debug:
            app.logger.debug(
                "Item {} added!".format(
                    (new_item.id, new_item.name)
                )
            )
        flash("Item {} added!".format(
            (new_item.id, new_item.name)), 'success'
        )
        return redirect(url_for('home.index'))
    return render_template("profile/item.html", action="Add",
                           data_type="an item",
                           form_action='profile.new_item',
                           form=form)


@profile.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    owner = item.user
    if current_user.id != owner.id:
        flash("You are not authorized to edit this item. "
              "Please create your own item in order to edit.", 'warning')
        return redirect(url_for('home.index'))

    form = ItemForm(obj=item)
    categories = Category.query.all()
    if categories:
        form.category.choices = [(cat.id, cat.name) for cat in categories]
        form.category.data = item.category_id
    else:
        form.category.choices = [(0, 'None')]
    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first_or_404()
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
            (item.id, item.name)), 'success'
        )
        return redirect(url_for('home.index'))
    return render_template('profile/item.html', action='Edit',
                           data_type=item,
                           form_action='profile.edit_item',
                           form=form)


@profile.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    owner = item.user
    if current_user.id != owner.id:
        flash("You are not authorized to delete this item. "
              "Please create your own item in order to delete.", 'warning')
        return redirect(url_for('home.index'))
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        if app.debug:
            app.logger.debug("Item {} deleted!".format(
                (item.id, item.name)))
        flash("Category {} deleted!".format(
            (item.id, item.name)), 'success')
        return redirect(url_for('home.index'))
    else:
        return render_template('profile/delete.html', form=form,
                               action='item',
                               form_action='profile.delete_item',
                               object=item)


@profile.route('/user/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if current_user.id != user.id:
        flash("You are not authorized to view this user profile.", 'warning')
        return redirect(url_for('home.index'))
    return render_template('profile/user_profile.html', user=user)


@profile.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user)
    del form.name  # Remove name so user can't change name
    if current_user.id != user.id:
        flash("You are not authorized to update this user info. ", 'warning')
        return redirect(url_for('home.index'))
    if form.validate_on_submit():
        user.email = form.email.data
        user.password = form.password.data
        user.picture = form.picture.data
        db.session.add(user)
        db.session.commit()
        if app.debug:
            app.logger.debug("User {} info updated!".format(
                (user.id, user.name)))
        flash("User {} info updated!".format(
            (user.id, user.name)), 'success')
        return redirect(url_for('profile.user_profile', user_id=user.id))
    return render_template('profile/edit_user.html', form=form, user=user)
