# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/app/modules/localmodule.py
# Compiled at: 2015-12-07 10:19:15


class LocalModule(object):

    def on_get(self, req, resp):
        resp.body = "Hello! I'm LocalModule."


local_module = LocalModule()

def install_module(app):
    app.add_route('/', local_module)