# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rajatg/pyProjects/beacons/beacons/__init__.py
# Compiled at: 2015-12-29 01:16:33
from flask import Flask
import logging
from logging import FileHandler, Formatter
from beacons.portal.view import portal
app = Flask(__name__)
app.config['LOG_FILE'] = 'application.log'
file_handler = FileHandler(app.config['LOG_FILE'])
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.register_blueprint(portal)