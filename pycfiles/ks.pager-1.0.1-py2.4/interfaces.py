# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/pager/interfaces.py
# Compiled at: 2007-11-08 12:36:39
"""Inrefaces for the Zope 3 based pager package

$Id: interfaces.py 12510 2007-10-30 13:53:20Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'GPL'
__version__ = '$Revision: 12510 $'
__date__ = '$Date: 2007-10-30 15:53:20 +0200 (Вт, 30 окт 2007) $'
from zope.interface import Interface
from zope.schema import Int, URI, Bool, Tuple, Object, TextLine, ASCIILine
import zope.i18nmessageid
_ = zope.i18nmessageid.MessageFactory('ks.pager')

class IPagerFactory(Interface):
    """Pager Factory"""
    __module__ = __name__

    def init(self, iterable):
        """Get Adapted Iterable"""
        pass


class IPagerParams(Interface):
    """Pager Params"""
    __module__ = __name__
    start = Int(title=_('Start Element'))
    defaultStart = Int(title=_('Default Start Element'), default=0)
    startKey = ASCIILine(title=_('Start Key'), default='start')
    chunkSize = Int(title=_('Chunk Size'))
    defaultChunkSize = Int(title=_('Default Chunk Size'), default=4)
    chunkSizeKey = ASCIILine(title=_('Chunk Size Key'), default='cnt')
    chunkCount = Int(title=_('Chunk Count on Page'))
    defaultChunkCount = Int(title=_('Default Chunk Count on Page'), default=10)
    chunkCountKey = ASCIILine(title=_('Chunk Count Key'), default='chnkcnt')
    objectURL = ASCIILine(title=_('Object URL for Chunk URLs'))


class IChunk(Interface):
    __module__ = __name__
    title = TextLine(title=_('Title'), required=False)
    url = URI(title=_('Url'))
    selected = Bool(title=_('Selected'), required=False)


class IPagedSource(Interface):
    __module__ = __name__

    def getCount(*kv, **kw):
        """Get Full Element List Count"""
        pass

    def getChunk(start, chunkSize, *kv, **kw):
        """Get Chunk of Data"""
        pass


class IPager(Interface):
    __module__ = __name__
    nextChunkUrl = URI(title=_('Next Chunk URL'))
    prevChunkUrl = URI(title=_('Next Chunk URL'))
    haveNextChunk = Bool(title=_('Have Next Chunk'))
    havePrevChunk = Bool(title=_('Have Previous Chunk'))
    chunkUrlList = Tuple(title=_('Chunk URL List'), value_type=Object(title=_('Chunk URL'), schema=IChunk))
    chunk = Tuple(title=_('Chunk Element List'), value_type=Object(schema=IChunk))
    count = Int(title=_('Full Element List Count'))
    currentChunk = Int(title=_('Current Chunk Number'))
    firstChunkUrl = URI(title=_('First Chunk URL'))
    onFirstChunk = Bool(title=_('On First Chunk Flag'))
    lastChunkUrl = URI(title=_('Last Chunk URL'))
    onLastChunk = Bool(title=_('On Last Chunk Flag'))

    def init(*kv, **kw):
        """Init Pager"""
        pass