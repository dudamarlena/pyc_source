# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/netstat.py
# Compiled at: 2010-04-29 16:01:18
"""
Parser for output of 'netstat' UNIX utility.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: netstat.py 24755 2010-04-29 20:01:18Z dang $'
from logging import DEBUG
import re, time
from netlogger.parsers.base import BaseParser
from netlogger.nlapi import getGuid

class Parser(BaseParser):
    """Parser for output of 'netstat' UNIX utility.

    Parameters:
       - display {i,r,g,n,n*}: Display mode. One-letter code matching the option for 
                       netstat: 'i' for interface, 'r' for routing, 'g' for
                       multicast, 'n' for base netstat.
    """
    TYPE_RE = re.compile('^Active (.*)|^(Internet6?):.*|^(\\w+)-?.* Multicast Group Memberships')

    def __init__(self, f, display='n', **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._dbg = self.log.isEnabledFor(DEBUG)
        self._event_pfx = 'netstat'
        self._type = None
        self._expect_hdr = False
        if display == 'i':
            self._type = 'interface'
            self._expect_hdr = True
        elif display == 'r':
            self._event_pfx = 'netstat.routing'
        elif display == 'g':
            self._event_pfx = 'netstat.multicast'
        self._hdr_cols = []
        self._start = time.time()
        self._id = getGuid()
        return

    def _normalize(self, s):
        s = s.replace('(', '').replace(')', '').replace('_', '.').replace('-', '.')
        return s.lower()

    def process(self, line):
        if self._dbg:
            self.log.debug('netstat.process.start')
        result = ()
        if len(line) == 0:
            pass
        elif self._expect_hdr:
            self._expect_hdr = False
            for addrtype in ('Foreign', 'Local', 'Link-layer'):
                line = line.replace('%s Address' % addrtype, '%s_Address' % addrtype)

            cols = line.split()
            self._hdr_cols = []
            for c in cols:
                self._hdr_cols.append(self._normalize(c))

        else:
            m = self.TYPE_RE.match(line)
            if m:
                grp = max(m.groups())
                self._type = self._normalize(grp.replace(' ', '_'))
                self._expect_hdr = True
            elif self._type is not None:
                fields = line.split()
                if len(fields) > len(self._hdr_cols):
                    return ()
                d = {'ts': self._start, 'guid': self._id, 'event': '%s.%s' % (self._event_pfx, self._type)}
                for i in range(len(fields)):
                    n, v = self._hdr_cols[i], fields[i]
                    d[n] = v

                for i in range(len(fields), len(self._hdr_cols)):
                    d[self._hdr_cols[i]] = ''

                result = (
                 d,)
            if self._dbg:
                self.log.debug('netstat.process.end', num=len(result))
            return result