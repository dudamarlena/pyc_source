# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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