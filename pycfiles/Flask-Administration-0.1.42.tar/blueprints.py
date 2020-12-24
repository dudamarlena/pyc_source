# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bluemoon/Desktop/flask-administration/flask_administration/blueprints.py
# Compiled at: 2012-03-20 17:37:17
from flask import jsonify, Blueprint, request, Response, render_template
from .utils import static_folder, template_folder, encode_model
admin = Blueprint('main', 'flask.ext.administration.main', static_folder=static_folder, template_folder=template_folder)