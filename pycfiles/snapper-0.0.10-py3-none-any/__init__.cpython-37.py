# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/revisor/Documents/Snapper/snapper/__init__.py
# Compiled at: 2019-08-22 18:17:04
# Size of source mod 2**32: 125 bytes
from flask import Flask
from flask_restful import Api
app = Flask(__name__)
api = Api(app)
import snapper.api_views