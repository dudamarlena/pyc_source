# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/routes/_eventum.py
# Compiled at: 2016-04-19 10:47:47
from flask import Blueprint, current_app, send_from_directory
eventum = Blueprint('eventum', __name__)

@eventum.route('/static/<path:filename>', methods=['GET'])
def static(filename):
    return send_from_directory(current_app.config['EVENTUM_STATIC_FOLDER'], filename)