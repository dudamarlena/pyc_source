# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\importpath.py
# Compiled at: 2014-04-29 06:05:21
from django.core.exceptions import ImproperlyConfigured

def importpath(path, error_text=None):
    """                                                                                               
    Import value by specified ``path``.                                                               
    Value can represent module, class, object, attribute or method.                                              
    If ``error_text`` is not None and import will
    raise ImproperlyConfigured with user friendly text.                                     
    """
    result = None
    attrs = []
    parts = path.split('.')
    exception = None
    while parts:
        try:
            result = __import__(('.').join(parts), {}, {}, [''])
        except ImportError as e:
            if exception is None:
                exception = e
            attrs = parts[-1:] + attrs
            parts = parts[:-1]
        else:
            break

    for attr in attrs:
        try:
            result = getattr(result, attr)
        except (AttributeError, ValueError) as error:
            if error_text is not None:
                raise ImproperlyConfigured('Error: %s can import "%s"' % (error_text, path))
            else:
                raise exception

    return result