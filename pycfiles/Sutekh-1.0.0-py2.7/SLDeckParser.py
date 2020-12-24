# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/SLDeckParser.py
# Compiled at: 2019-12-11 16:37:57
"""Parser for Secret Library Web API deck format.

   For a description of the format see the Secret Library API at
   http://www.secretlibrary.info/api.php.

   The example deck given in the API documentation is:

   ***SL***TITLE***
   NAME OF THE DECK
   ***SL***AUTHOR***
   CREATOR OF THE DECK
   ***SL***CREATED***
   YYYY-MM-DD
   ***SL***DESCRIPTION***
   DESCRIPTION OF THE DECK
   MAY SPAN ON MULTIPLE LINES
   ***SL***CRYPT***
   2 Count Germaine
   2 Count Germaine (Adv)
   2 François Warden Loehr
   ***SL***LIBRARY***
   10 Cloak the Gathering
   2 Coven, The
   2 Carlton Van Wyk (Hunter)
   ***SL***ENDDECK***
   """
import re
from sutekh.base.Utility import move_articles_to_front
from sutekh.base.io.IOBase import CardSetParser

class SLDeckParser(CardSetParser):
    """Parser for the Secret Library Web API deck format."""
    oCardLineRegexp = re.compile('^(?P<num>[0-9]+)\\s+(?P<name>.*)$')

    def __init__(self):
        self._dSectionParsers = {'title': self._title_section, 
           'author': self._author_section, 
           'created': self._created_section, 
           'description': self._description_section, 
           'crypt': self._crypt_section, 
           'library': self._library_section, 
           'enddeck': self._no_section}

    def _switch_section(self, sLine):
        """Return a new section parser based on the given heading line."""
        sSection = sLine[len('***SL***'):-len('***')].lower()
        if sSection in self._dSectionParsers:
            return self._dSectionParsers[sSection]
        raise IOError('Unknown section heading in Secret Library Deck Format')

    def _no_section(self, _sLine, _oHolder):
        """Initial parser -- seeing a line here is an error."""
        raise IOError('Data line outside of section for Secret Library Deck format')

    def _title_section(self, sLine, oHolder):
        """Parse a title line."""
        oHolder.name = sLine

    def _author_section(self, sLine, oHolder):
        """Parse an author line."""
        oHolder.author = sLine

    def _created_section(self, sLine, oHolder):
        """Parse a created section line."""
        sCreatedLine = 'Created on %s' % (sLine,)
        if oHolder.comment:
            oHolder.comment += '\n' + sCreatedLine
        else:
            oHolder.comment = sCreatedLine

    def _description_section(self, sLine, oHolder):
        """Parse a description line. """
        if oHolder.comment:
            oHolder.comment += '\n' + sLine
        else:
            oHolder.comment = sLine

    def _crypt_section(self, sLine, oHolder):
        """Parse a crypt entry."""
        oMatch = self.oCardLineRegexp.match(sLine)
        if oMatch is None:
            raise IOError('Unrecognised crypt line for Secrety Library deck format')
        iNum = int(oMatch.group('num'))
        sName = oMatch.group('name')
        if sName.endswith('(Adv)'):
            sName = sName.replace('(Adv)', '(Advanced)')
        sName = move_articles_to_front(sName)
        oHolder.add(iNum, sName, None, None)
        return

    def _library_section(self, sLine, oHolder):
        """Parse a library entry."""
        oMatch = self.oCardLineRegexp.match(sLine)
        if oMatch is None:
            raise IOError('Unrecognised library line for Secrety Library deck format')
        iNum = int(oMatch.group('num'))
        sName = oMatch.group('name')
        sName = move_articles_to_front(sName)
        oHolder.add(iNum, sName, None, None)
        return

    def parse(self, fIn, oHolder):
        """Parse the SL deck in fIn into oHolder."""
        fLineParser = self._no_section
        for sLine in fIn:
            sLine = sLine.strip()
            if not sLine:
                continue
            if sLine.startswith('***'):
                fLineParser = self._switch_section(sLine)
            else:
                fLineParser(sLine, oHolder)