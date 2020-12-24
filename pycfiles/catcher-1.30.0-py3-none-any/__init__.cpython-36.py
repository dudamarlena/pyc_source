# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/__init__.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 162 bytes
from flask import Flask
from .router_bot import RouterBot
from .routes import register_routes
__version__ = '0.0.2'
app = Flask(__name__)
register_routes(app)