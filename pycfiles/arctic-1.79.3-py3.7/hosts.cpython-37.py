# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/hosts.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1490 bytes
"""
Utilities to resolve a string to Mongo host, or a Arctic library.
"""
import logging, re
from weakref import WeakValueDictionary
import six
__all__ = [
 'get_arctic_lib']
logger = logging.getLogger(__name__)
arctic_cache = WeakValueDictionary()
CONNECTION_STR = re.compile('(^\\w+\\.?\\w+)@([^\\s:]+:?\\w+)$')

def get_arctic_lib(connection_string, **kwargs):
    """
    Returns a mongo library for the given connection string

    Parameters
    ---------
    connection_string: `str`
        Format must be one of the following:
            library@trading for known mongo servers
            library@hostname:port

    Returns:
    --------
    Arctic library
    """
    m = CONNECTION_STR.match(connection_string)
    if not m:
        raise ValueError('connection string incorrectly formed: %s' % connection_string)
    library, host = m.group(1), m.group(2)
    return _get_arctic(host, **kwargs)[library]


def _get_arctic(instance, **kwargs):
    key = (
     instance, frozenset(six.iteritems(kwargs)))
    arctic = arctic_cache.get(key, None)
    if not arctic:
        from .arctic import Arctic
        arctic = Arctic(instance, **kwargs)
        arctic_cache[key] = arctic
    return arctic