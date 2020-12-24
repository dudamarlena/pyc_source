# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/IndexController.py
# Compiled at: 2017-03-29 12:18:51
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import request, render_template, url_for, redirect, current_app as app
from flask.ext.login import login_required
from onyx.api.assets import Json
from onyx.api.widgets import *
json = Json()
box = Widgets()

@core.route('/')
@login_required
def index():
    json.json = box.get()
    boxs = json.decode()
    return render_template('index/index.html', boxs=boxs)