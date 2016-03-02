# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: models
 * Date: 2/23/16
 * Time: 14:46
 * To change this templates use File | Settings | File Templates.
"""
import datetime

from flask.ext.login import UserMixin

from catalog import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from slugify import slugify


class UserSocialProfile(db.Model):
    __tablename__ = 'social_profile'
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(150), nullable=False)
    social_id = db.Column(db.String(250))
    profile = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# User model using Flask-Login UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    _password = db.Column(db.String(128))
    picture = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)
    social_profiles = db.relationship(UserSocialProfile)

    @hybrid_property
    def password(self):
        return self._password

    # Define the password setter to store the hashed password isntead of the
    # raw password in the database
    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    # Check if password is correct comparing the password hash in database
    # with the password sent by the client
    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True
        return False

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'date_created': self.date_created,
            'las_updated': self.last_updated
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    slugfield = db.Column(db.String(250), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)

    # Define a unique slug to the added category using the slugify library
    def __init__(self, *args, **kwargs):
        if 'slugfield' not in kwargs:
            kwargs['slugfield'] = slugify(kwargs.get('name', ''))
        super(Category, self).__init__(*args, **kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slugfield': self.slugfield,
            'user_id': self.user_id,
            'date_created': self.date_created,
            'last_updated': self.last_updated
        }


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500))
    picture = db.Column(db.String(250))
    slugfield = db.Column(db.String(250), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)

    # Define a unique slug to the added item using the slugify library
    def __init__(self, *args, **kwargs):
        if 'slugfield' not in kwargs:
            kwargs['slugfield'] = slugify(kwargs.get('category', '').name +
                                          ' ' + kwargs.get('name', ''))
        super(Item, self).__init__(*args, **kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'slugfield': self.slugfield,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'date_created': self.date_created,
            'last_updated': self.last_updated
        }
