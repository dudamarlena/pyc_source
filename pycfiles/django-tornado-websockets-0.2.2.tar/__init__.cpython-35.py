# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kocal/Dev/Python/django-tornado-websockets/tornado_websockets/__init__.py
# Compiled at: 2016-12-19 16:32:09
# Size of source mod 2**32: 338 bytes
__version_info__ = ('0', '2', '2')
__version__ = '.'.join(__version_info__)

def django_app():
    import django.core.handlers.wsgi, tornado.wsgi
    django.setup()
    app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    app = ('.*', tornado.web.FallbackHandler, dict(fallback=app))
    return app