# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/metadirectives.py
# Compiled at: 2007-12-05 09:41:22
"""
"""
__docformat__ = 'restructuredtext'
import zope.interface, zope.schema
from zope.app.i18n import ZopeMessageFactory as _

class IIWMemcachedServer(zope.interface.Interface):
    __module__ = __name__
    server = zope.schema.TextLine(title=_('Server'), description=_('ip:port of the memcached server for the namespace'), required=False)
    name = zope.schema.TextLine(title=_('Name space'), description=_('Name space for the cache.  This is used by application code when locating a cache utility.'), required=True)
    maxage = zope.schema.Int(title=_('Max Age'), description=_('Max age in second to keep value in cache'), required=False)


class IIWRAMCache(zope.interface.Interface):
    __module__ = __name__
    name = zope.schema.TextLine(title=_('Name space'), description=_('Name space for the cache.  This is used by application code when locating a cache utility.'), required=True)
    maxage = zope.schema.Int(title=_('Max Age'), description=_('Max age in second to keep value in cache'), required=False)