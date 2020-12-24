# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_support_page/support_handlers.py
# Compiled at: 2018-06-05 21:43:21
from django.conf import settings
from django.core import exceptions
from importlib import import_module

def init_support_handlers():
    handler_paths = getattr(settings, 'SUPPORT_PAGE_HANDLERS', [
     'django_support_page.handlers.mail_handler.mail_handler'])
    handlers = []
    for handler_path in handler_paths:
        try:
            h_module, h_funcname = handler_path.rsplit('.', 1)
        except ValueError:
            raise exceptions.ImproperlyConfigured("%s isn't a django_support_page handler" % handler_path)

        try:
            mod = import_module(h_module)
        except ImportError as e:
            msg = 'Error importing django_support_page handler %s: "%s"'
            raise exceptions.ImproperlyConfigured(msg % (h_module, e))

        try:
            h_func = getattr(mod, h_funcname)
        except AttributeError:
            raise exceptions.ImproperlyConfigured('django_support_page handle "%s" does not define a "%s" function' % (
             h_module, h_funcname))

        handlers.append(h_func)

    return handlers