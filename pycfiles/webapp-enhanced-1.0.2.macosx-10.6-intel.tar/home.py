# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/static/controllers/home.py
# Compiled at: 2014-04-20 18:29:54
from controllers.core import Controller

class Home(Controller):
    """/"""

    def index(self):
        self.send_data(foo='Hello, World!')