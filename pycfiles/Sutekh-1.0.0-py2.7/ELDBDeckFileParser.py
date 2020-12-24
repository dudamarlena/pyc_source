# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/ELDBDeckFileParser.py
# Compiled at: 2019-12-11 16:37:58
"""Parser for ELDB deck format"""
from sutekh.core.ELDBUtilities import gen_name_lookups

class State(object):
    """Base class for the State Objects."""

    def __init__(self, oHolder, dNameCache):
        self._sData = ''
        self._oHolder = oHolder
        self._dNameCache = dNameCache

    def transition(self, sLine):
        """Transition to next state"""
        raise NotImplementedError

    def data(self, sData):
        """Add data to the state object."""
        self._sData += sData


class Name(State):
    """State for extracting Name."""

    def transition(self, sLine):
        """Process the line for Name - transitioning to author."""
        sValue = sLine.strip()
        if not sValue:
            return self
        sValue = sValue.strip('"')
        self._oHolder.name = sValue
        return Author(self._oHolder, self._dNameCache)


class Author(State):
    """State for extracting Author."""

    def transition(self, sLine):
        """Process the line for Author - transitioning to description."""
        sValue = sLine.strip()
        if not sValue:
            return self
        sValue = sValue.strip('"')
        if sValue:
            self._oHolder.author = sValue
        return Description(self._oHolder, self._dNameCache)


class Description(State):
    """State for extracting description"""

    def transition(self, sLine):
        """Process the lines for the description and transition to Cards
           state if needed."""
        sValue = sLine.strip()
        if sValue.endswith('"'):
            self.data(sValue.strip('"'))
            self._oHolder.comment = self._sData
            return Cards(self._oHolder, self._dNameCache)
        self.data(sValue.strip('"') + '\n')
        return self


class Cards(State):
    """State for extracting the cards"""

    def transition(self, sLine):
        """Extract the cards from the data.

           This is the terminating state, so we always return Cards from
           this.
           """
        sCard = sLine.strip()
        if not sCard.startswith('"'):
            return self
        else:
            sCard = sCard.strip('"')
            if sCard in self._dNameCache:
                sName = self._dNameCache[sCard]
            else:
                sName = sCard
            self._oHolder.add(1, sName, None, None)
            return self


class ELDBDeckFileParser(object):
    """Parser for the ELDB Deck format."""

    def __init__(self):
        super(ELDBDeckFileParser, self).__init__()
        self._dNameCache = gen_name_lookups()
        self._oState = None
        return

    def _feed(self, sLine):
        """Feed the next line to the current state object, and transition if
           required."""
        self._oState = self._oState.transition(sLine)

    def parse(self, fIn, oHolder):
        """Parse the file line-by-line"""
        self._oState = Name(oHolder, self._dNameCache)
        for sLine in fIn:
            self._feed(sLine)