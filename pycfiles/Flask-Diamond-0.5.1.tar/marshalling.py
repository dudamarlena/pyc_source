# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/marshalling.py
# Compiled at: 2016-11-26 10:59:16
from flask_marshmallow import Marshmallow
ma = Marshmallow()

def init_marshalling(self):
    """
    Initialize Marshmallow.

    :returns: None
    """
    ma.app = self.app
    ma.init_app(self.app)