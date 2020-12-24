# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/hosts.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1490 bytes
__doc__ = '\nUtilities to resolve a string to Mongo host, or a Arctic library.\n'
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