# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/__init__.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 162 bytes
from flask import Flask
from .router_bot import RouterBot
from .routes import register_routes
__version__ = '0.0.2'
app = Flask(__name__)
register_routes(app)