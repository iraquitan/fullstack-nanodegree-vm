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

from catalog import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    _password = db.Column(db.String(128))
    picture = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }

    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True
        return False


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

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
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now,
                             onupdate=datetime.datetime.now)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'picture': self.picture
        }

