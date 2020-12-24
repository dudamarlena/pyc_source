# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/wsgi_app/flask_wsgi.py
# Compiled at: 2016-01-09 00:25:44
from flask import Flask
from .base_wsgi import BaseWSGI

class FlaskWSGI(Flask, BaseWSGI):

    def __init__(self, *a, **kw):
        Flask.__init__(self, *a, **kw)
        BaseWSGI.__init__(self)

    def reflect_uri(self):
        return [ rule.rule for rule in self.url_map.iter_rules() ]