# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gman/Documents/code/Flask-Blogging/test/__init__.py
# Compiled at: 2018-02-15 00:06:52
# Size of source mod 2**32: 622 bytes
import unittest
from flask import Flask
from flask_login import UserMixin
__author__ = 'gbalaraman'

class FlaskBloggingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

        @self.app.route('/')
        def index():
            return 'Hello World!'


class TestUser(UserMixin):

    def __init__(self, user_id):
        self.id = user_id