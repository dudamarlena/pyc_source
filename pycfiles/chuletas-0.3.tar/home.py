# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./scripts/../apps/example/webapp/controller/home.py
# Compiled at: 2011-07-30 01:36:12
from chula.www import controller

class Home(controller.Controller):

    def index(self):
        return 'Hello <a href="home/foo">world</a>'

    def foo(self):
        return 'This is the method "foo" of the home controller'

    def raw(self):
        return self.env.form_raw