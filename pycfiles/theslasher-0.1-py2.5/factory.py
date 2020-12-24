# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/theslasher/factory.py
# Compiled at: 2010-01-11 17:46:59
from paste.httpexceptions import HTTPExceptionHandler
from theslasher import TheSlasher
from webob import Response

def example(environ, start_response):
    return Response(content_type='text/plain', body=environ['PATH_INFO'])(environ, start_response)


def factory(global_conf, **app_conf):
    """create a webob view and wrap it in middleware"""
    return TheSlasher(example)