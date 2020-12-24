# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/dispatchers.py
# Compiled at: 2013-07-28 11:50:49
"""
All dispatcher plugins go here.
"""

class RoutesDispatcher(object):
    from _routes import routes

    def __init__(self, app):
        self.app = app

    def handle(self, *args, **kwargs):
        return self.app.routes.match(*args, **kwargs)