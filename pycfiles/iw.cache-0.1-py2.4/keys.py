# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/keys.py
# Compiled at: 2007-12-05 09:41:22
"""
cache keys
"""
__docformat__ = 'restructuredtext'
import zope.interface
from cPickle import dumps, UnpickleableError
import md5, types, inspect

def hash_instance(instance):
    """ get the class name

        >>> from iw.cache.keys import hash_instance
        >>> from smtplib import SMTP
        >>> server = SMTP()
        >>> print hash_instance(server)
        smtplib.SMTP
    """
    return '%s.%s' % (instance.__module__, instance.__class__.__name__)


def hash_func(func):
    """ func representation
        >>> from iw.cache.keys import hash_func
        >>> from smtplib import SMTP
        >>> server = SMTP()
        >>> print hash_func(server.sendmail)
        smtplib.sendmail
    """
    return '%s.%s' % (func.__module__, func.func_name)


def hash_context(context):
    return context._poid


def hash_view(view):
    return hash_instance(view) + hash_context(view.context)


def hash_value(key, arg):
    if type(arg) in (types.IntType, types.BooleanType) + types.StringTypes:
        value = dumps(arg)
    elif inspect.isfunction(arg) or inspect.ismethod(arg):
        return hash_func(arg)
    elif hasattr(arg, 'aq_inner'):
        value = hash_context(arg)
    elif zope.interface.Interface.providedBy(arg):
        if hasattr(arg, 'context'):
            value = hash_view_context(arg)
        return hash_instance(arg)
    else:
        try:
            value = dumps(arg)
        except UnpickleableError:
            value = str(arg)

    return '%s=%s' % (key, value)


def cache_key(*args, **kwargs):
    """ cache key::

        >>> import zope.interface
        >>> from iw.cache.keys import cache_key
        >>> import md5

        >>> def valid_key(key, attended):
        ...     return key == md5.new(attended).hexdigest()

        >>> def a(*args, **kwargs): pass
        >>> key = cache_key(a)
        >>> valid_key(cache_key(a),
        ...           'cache.tests.test_cachedocstrings.a')
        True

        >>> class A(object):
        ...     zope.interface.implements(zope.interface.Interface)
        ...     def a(self): pass

        >>> valid_key(cache_key(A.a, A()),
        ...  'cache.tests.test_cachedocstrings.a::cache.tests.test_cachedocstrings.A')
        True

    """
    hash_key = []
    for (i, arg) in enumerate(args):
        hash_key.append(hash_value(i, arg))

    hash_key.extend([ hash_value(key, value) for (key, value) in kwargs.items() ])
    hash_key = ('::').join(hash_key)
    return md5.new(hash_key).hexdigest()