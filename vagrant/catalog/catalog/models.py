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


class UserSocialProfile(db.Model):
    __tablename__ = 'social_profile'
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(150), nullable=False)
    social_id = db.Column(db.String(250))
    profile = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

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
            'social_id': self.social_id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'date_created': self.date_created
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500))
    picture = db.Column(db.String(250))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'category_id': self.category_id,
            'date_created': self.date_created,
            'last_updated': self.last_updated
        }

