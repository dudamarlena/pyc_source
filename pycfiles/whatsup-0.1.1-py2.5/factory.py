# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/whatsup/factory.py
# Compiled at: 2009-06-15 14:58:54
from whatsup import WhatsupView
from paste.httpexceptions import HTTPExceptionHandler

def factory(global_conf, **app_conf):
    """create a webob view and wrap it in middleware"""
    keystr = 'whatsup.'
    args = dict([ (key.split(keystr, 1)[(-1)], value) for (key, value) in app_conf.items() if key.startswith(keystr)
                ])
    app = WhatsupView(**args)
    return HTTPExceptionHandler(app)