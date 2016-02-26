# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: forms
 * Date: 2/23/16
 * Time: 14:55
 * To change this templates use File | Settings | File Templates.
"""
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
    PasswordField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import InputRequired, Optional, url, email, EqualTo, \
    NoneOf


class DeleteForm(Form):
    delete = SubmitField('Delete')


class UserForm(Form):
    name = StringField('User name', [
        InputRequired(message='User name is required')])
    email = EmailField('Email', validators=[email(), InputRequired(
        message='Email is required'
    )])
    password = PasswordField('Password', validators=[InputRequired(
        message='Password is required'), EqualTo(
        'confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password', validators=[
        InputRequired(message='Password confirmation required')
    ])
    picture = URLField('User picture', [url(message='Not a valid URL'),
                                        Optional()])


class CategoryForm(Form):
    name = StringField('Category name', [
        InputRequired(message='Category name is required'),
        NoneOf(values=[], message='Category already exist!')])


class DeleteForm(Form):
    delete = SubmitField('Delete')


class ItemForm(Form):
    name = StringField('Item name', [
        InputRequired(message='Item name is required')])
    category = SelectField('Category', coerce=int)
    description = TextAreaField('Description', validators=[Optional()])
    picture = URLField('User picture', [url(message='Not a valid URL'),
                                        Optional()])


class EmailPasswordForm(Form):
    email = EmailField('Email', validators=[email(), InputRequired(
        message='Email is required'
    )])
    password = PasswordField('Password', validators=[InputRequired(
        message='Password is required'
    )])
