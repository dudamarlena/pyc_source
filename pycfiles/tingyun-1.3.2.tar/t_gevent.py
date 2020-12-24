# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/matrix/t_gevent.py
# Compiled at: 2016-06-30 06:13:10
"""Define this module for basic armory for gevent

"""
from tingyun.armoury.trigger.wsgi_entrance import wsgi_app_wrapper_entrance
from tingyun.logistics.basic_wrapper import trace_in_function

def trace_wsgi_server(*args, **kwargs):

    def instance_parameters(instance, listener, application, *args, **kwargs):
        return (
         instance, listener, application, args, kwargs)

    self, listener, application, _args, _kwargs = instance_parameters(*args, **kwargs)
    application = wsgi_app_wrapper_entrance(application)
    _args = (
     self, listener, application) + _args
    return (
     _args, _kwargs)


def detect_pywsgi(module):
    """
    """
    trace_in_function(module, 'WSGIServer.__init__', trace_wsgi_server)


def detect_wsgi(module):
    """
    """
    trace_in_function(module, 'WSGIServer.__init__', trace_wsgi_server)