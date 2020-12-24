# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/JOLDeckParser.py
# Compiled at: 2019-12-11 16:37:58
"""Parser for JOL deck format"""
import re
from sutekh.base.Utility import move_articles_to_front
from sutekh.base.io.IOBase import BaseLineParser

class JOLDeckParser(BaseLineParser):
    """Parser for the JOL Deck format."""
    oCardLineRegexp = re.compile('((?P<num>[0-9]+)(\\s)*x(\\s)*)?(?P<name>.*)$')

    def _feed(self, sLine, oHolder):
        """Read the line into the given CardSetHolder"""
        oMatch = self.oCardLineRegexp.match(sLine)
        if oMatch is not None:
            dResults = oMatch.groupdict()
            if dResults['num']:
                iNum = int(dResults['num'])
            else:
                iNum = 1
            sName = dResults['name']
        else:
            raise IOError('Unrecognised line for JOL format')
        if sName.endswith('(advanced)'):
            sName = sName.replace('(advanced)', '(Advanced)')
        sName = move_articles_to_front(sName)
        oHolder.add(iNum, sName, None, None)
        return