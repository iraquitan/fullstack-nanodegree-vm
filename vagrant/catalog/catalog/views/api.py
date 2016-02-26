# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: api
 * Date: 2/26/16
 * Time: 11:26
 * To change this template use File | Settings | File Templates.
"""
from flask import Blueprint, jsonify

from catalog.models import Category, Item

api = Blueprint('api', __name__)


@api.route('/catalog.json')
def catalog_api():
    categories = Category.query.all()
    all_result = []
    for category in categories:
        items = Item.query.filter_by(category_id=category.id).all()
        result = category.serialize
        result['Item'] = [i.serialize for i in items]
        all_result.append(result)
    return jsonify(Category=all_result)


@api.route('/category/<int:category_id>/json')
def category_api(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    return jsonify(category=category.serialize)


@api.route('/category/<int:category_id>/items.json')
def category_items_api(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    items = Item.query.filter_by(category_id=category.id).all()
    result = category.serialize
    result['item'] = [i.serialize for i in items]
    return jsonify(category=result)


@api.route('/item/<int:item_id>/item.json')
def item_api(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    return jsonify(item=item.serialize)
