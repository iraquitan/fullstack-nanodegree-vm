# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: runserver
 * Date: 2/23/16
 * Time: 14:39
 * To change this templates use File | Settings | File Templates.
"""
from catalog import app, db
import os

# Create database if not exist
if not os.path.exists("./catalog/catalog.db"):
    db.create_all()
app.run(host='0.0.0.0', port=8000)
