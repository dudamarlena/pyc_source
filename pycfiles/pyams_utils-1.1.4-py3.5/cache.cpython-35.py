# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/cache.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3214 bytes
"""PyAMS_utils.cache module

This module provides a small set of adapters which can be used to provide a "cache key" value
to any kind of object.

The goal of such a cache key value is to provide a string representation, as stable as possible,
of a given object; this string can be used as a cache key, but also to define an object ID inside
an HTML page.
A TALES helper extension is also provided to get an object's cache key from a Chameleon template.
"""
from persistent.interfaces import IPersistent
from zope.interface import Interface
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

@adapter_config(context=object, provides=ICacheKeyValue)
def object_cache_key_adapter(obj):
    """Cache key adapter for any object

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from pyams_utils.interfaces import ICacheKeyValue
    >>> from pyams_utils.cache import object_cache_key_adapter
    >>> config.registry.registerAdapter(object_cache_key_adapter, (object, ), ICacheKeyValue)

    >>> value = object()
    >>> key = ICacheKeyValue(value)
    >>> key == str(id(value))
    True

    >>> tearDown()
    """
    return str(id(obj))


@adapter_config(context=str, provides=ICacheKeyValue)
def string_cache_key_adapter(obj):
    """Cache key adapter for string value

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from pyams_utils.interfaces import ICacheKeyValue
    >>> from pyams_utils.cache import string_cache_key_adapter
    >>> config.registry.registerAdapter(string_cache_key_adapter, (str, ), ICacheKeyValue)

    >>> value = 'my test string'
    >>> key = ICacheKeyValue(value)
    >>> key == value
    True

    >>> tearDown()
    """
    return obj


@adapter_config(context=IPersistent, provides=ICacheKeyValue)
def persistent_cache_key_adapter(obj):
    """Cache key adapter for persistent object"""
    if obj._p_oid:
        return str(int.from_bytes(obj._p_oid, byteorder='big'))
    return str(id(obj))


@adapter_config(name='cache_key', context=(Interface, Interface, Interface), provides=ITALESExtension)
class CacheKeyTalesExtension(ContextRequestViewAdapter):
    __doc__ = 'extension:cache_key(context) TALES extension\n\n    A PyAMS TALES extension which allows to render cache key value for a given context.\n    '

    def render(self, context=None):
        """Rendering of TALES extension"""
        if context is None:
            context = self.request.context
        return ICacheKeyValue(context)