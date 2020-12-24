# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/cache.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3214 bytes
__doc__ = 'PyAMS_utils.cache module\n\nThis module provides a small set of adapters which can be used to provide a "cache key" value\nto any kind of object.\n\nThe goal of such a cache key value is to provide a string representation, as stable as possible,\nof a given object; this string can be used as a cache key, but also to define an object ID inside\nan HTML page.\nA TALES helper extension is also provided to get an object\'s cache key from a Chameleon template.\n'
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
    """CacheKeyTalesExtension"""

    def render(self, context=None):
        """Rendering of TALES extension"""
        if context is None:
            context = self.request.context
        return ICacheKeyValue(context)