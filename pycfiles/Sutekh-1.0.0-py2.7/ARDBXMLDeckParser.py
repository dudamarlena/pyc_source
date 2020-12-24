# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/ARDBXMLDeckParser.py
# Compiled at: 2019-12-11 16:37:58
"""Parser for ARDB XML deck formats"""
from sutekh.io.ARDBXMLInvParser import ARDBInvXMLState, ARDBXMLInvParser

class ARDBDeckXMLState(ARDBInvXMLState):
    """Simple State tracker used by the XMLParser"""
    ROOTTAG, NOTAG, DECKNAME, DECKAUTHOR, DECKCOMMENT, INCARD, CARDNAME, CARDSET, ADVANCED = range(9)
    COUNT_KEY = 'count'
    ROOT = 'deck'

    def start(self, sTag, dAttributes):
        """Start tag encountered"""
        if self._iState == self.NOTAG and sTag in ('name', 'author', 'description'):
            if sTag == 'name':
                self._iState = self.DECKNAME
            elif sTag == 'author':
                self._iState = self.DECKAUTHOR
            elif sTag == 'description':
                self._iState = self.DECKCOMMENT
        else:
            super(ARDBDeckXMLState, self).start(sTag, dAttributes)

    def end(self, sTag):
        """End tag encountered"""
        if self._iState == self.DECKAUTHOR and sTag == 'author':
            self._oHolder.author = self._sData
            self._set_no_tag()
        elif self._iState == self.DECKNAME and sTag == 'name':
            self._oHolder.name = self._sData
            self._set_no_tag()
        elif self._iState == self.DECKCOMMENT and sTag == 'description':
            self._oHolder.comment = self._sData
            self._set_no_tag()
        else:
            super(ARDBDeckXMLState, self).end(sTag)

    def _set_no_tag(self):
        """Set state back to NOTAG state"""
        self._iState = self.NOTAG
        self._sData = ''


class ARDBXMLDeckParser(ARDBXMLInvParser):
    """Parser for the ARDB XML deck format."""
    _cState = ARDBDeckXMLState