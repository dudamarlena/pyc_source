# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/SLInventoryParser.py
# Compiled at: 2019-12-11 16:37:57
"""Parser for Secret Library Web API inventory format

   For a description of the format see the Secret Library API at
   http://www.secretlibrary.info/api.php.

   The example inventory given in the API documentation is:

   ***SL***CRYPT***
   2;2;Abebe
   2;2;Alan Sovereign (Adv)
   4;3;François Warden Loehr
   ***SL***LIBRARY***
   1;1;Absimiliard's Army
   5;5;Ahriman's Demesne
   4;4;Atonement
   1;1;Textbook Damnation, The
   8;8;Watch Commander
   ***SL***ENDEXPORT***
   """
import re
from sutekh.base.Utility import move_articles_to_front
from sutekh.base.io.IOBase import CardSetParser

class SLInventoryParser(CardSetParser):
    """Parser for the Secret Library web API inventory format."""
    oCardLineRegexp = re.compile('^(?P<have>[0-9]+)\\s*;\\s*(?P<want>[0-9]+)\\s*;\\s*(?P<name>.*)$')

    def __init__(self):
        self._dSectionParsers = {'crypt': self._crypt_section, 
           'library': self._library_section, 
           'endexport': self._no_section}

    def _switch_section(self, sLine):
        """Return a new section parser based on the given heading line."""
        sSection = sLine[len('***SL***'):-len('***')].lower()
        if sSection in self._dSectionParsers:
            return self._dSectionParsers[sSection]
        raise IOError('Unknown section heading in Secret Library inventory format')

    def _no_section(self, _sLine, _oHolder):
        """Initial parser -- seeing a line here is an error."""
        raise IOError('Data line outside of section for Secret Library inventory format')

    def _crypt_section(self, sLine, oHolder):
        """Parse a crypt entry."""
        oMatch = self.oCardLineRegexp.match(sLine)
        if oMatch is None:
            raise IOError('Unrecognised crypt line for Secrety Library deck format')
        iNum = int(oMatch.group('have'))
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
        iNum = int(oMatch.group('have'))
        sName = oMatch.group('name')
        sName = move_articles_to_front(sName)
        oHolder.add(iNum, sName, None, None)
        return

    def parse(self, fIn, oHolder):
        """Parse the SL inventory in fIn into oHolder."""
        fLineParser = self._no_section
        for sLine in fIn:
            sLine = sLine.strip()
            if not sLine:
                continue
            if sLine.startswith('***'):
                fLineParser = self._switch_section(sLine)
            else:
                fLineParser(sLine, oHolder)