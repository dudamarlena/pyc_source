# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/pager/pagerparamsadapter/pagerparamsadapter.py
# Compiled at: 2007-11-08 12:36:38
"""SiteUrl adapters for the Zope 3 based issue package

$Id: pagerparamsadapter.py 1408 2007-09-18 14:56:18Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 1408 $'
__date__ = '$Date: 2007-09-18 17:56:18 +0300 (Вт, 18 сен 2007) $'
from zope.interface import Interface, implements
from zope.publisher.browser import BrowserView
from ks.pager.interfaces import IPagerParams
from zope.component import adapts
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema.fieldproperty import FieldProperty

class PagerParamsAdapterBase(object):
    __module__ = __name__
    startKey = FieldProperty(IPagerParams['startKey'])
    defaultStart = FieldProperty(IPagerParams['defaultStart'])
    chunkSizeKey = FieldProperty(IPagerParams['chunkSizeKey'])
    defaultChunkSize = FieldProperty(IPagerParams['defaultChunkSize'])
    chunkCountKey = FieldProperty(IPagerParams['chunkCountKey'])
    defaultChunkCount = FieldProperty(IPagerParams['defaultChunkCount'])
    objectURL = FieldProperty(IPagerParams['objectURL'])

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def start(self):
        """See IPagerParams interface"""
        return int(self.request.form.get(self.startKey, self.defaultStart))

    @property
    def chunkSize(self):
        """See IPagerParams interface"""
        return int(self.request.form.get(self.chunkSizeKey, self.defaultChunkSize))

    @property
    def chunkCount(self):
        """See IPagerParams interface"""
        return int(self.request.form.get(self.chunkCountKey, self.defaultChunkCount))


class PagerParamsAdapter(PagerParamsAdapterBase):
    __module__ = __name__
    adapts(Interface, IHTTPRequest)
    implements(IPagerParams)