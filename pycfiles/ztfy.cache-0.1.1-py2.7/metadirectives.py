# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/metadirectives.py
# Compiled at: 2012-06-11 15:33:55
from zope.configuration.fields import GlobalInterface
from zope.interface import Interface
from zope.schema import TextLine
from ztfy.cache import _

class ICacheProxyHandlerBase(Interface):
    """Cache proxy handler base interface"""

    def getCache(self):
        """Get the real cache utility"""
        pass


class ICacheProxyHandlerInfo(Interface):
    """A cache handler is a proxy to an actual cache utility"""
    name = TextLine(title=_('Cache handler name'), required=False)
    cache_interface = GlobalInterface(title=_('Cache utility interface'), required=True)
    cache_name = TextLine(title=_('Cache utility name'), required=False)


class ICacheProxyHandler(ICacheProxyHandlerBase, ICacheProxyHandlerInfo):
    """Cache proxy handler interface"""
    pass