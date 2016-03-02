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

# Define api Blueprint for JSON endpoints
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


@api.route('/category/<string:category_slug>.json')
def category_api(category_slug):
    category = Category.query.filter_by(slugfield=category_slug).first_or_404()
    return jsonify(category=category.serialize)


@api.route('/category/<string:category_slug>/items.json')
def category_items_api(category_slug):
    category = Category.query.filter_by(slugfield=category_slug).first_or_404()
    items = Item.query.filter_by(category_id=category.id).all()
    result = category.serialize
    result['item'] = [i.serialize for i in items]
    return jsonify(category=result)


@api.route('/item/<string:item_slug>.json')
def item_api(item_slug):
    item = Item.query.filter_by(slugfield=item_slug).first_or_404()
    return jsonify(item=item.serialize)
