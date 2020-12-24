# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/bp.py
# Compiled at: 2010-09-20 01:22:40
"""
Parse 'best practices' logs, essentially a no-op.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: bp.py 25222 2010-09-20 05:22:38Z dang $'
import logging
from netlogger import nllog
from netlogger.parsers.base import NLFastParser

class Parser(NLFastParser):
    """Parse Best-Practices logs into Best-Practices logs.

    Parameters:
        - has_gid {yes,no,no*}: If 'yes', the "gid=" keyword in the input will be
          replaced by the currently correct "guid=".
       - ignore_prefix {yes,no,no*}: Ignore any text before the record body.
        - verify {yes,no,yes*}: Verify the format of the input, otherwise simply
          pass it through without looking at it.
    """

    def __init__(self, f, has_gid=False, verify=True, ignore_prefix='no', **kwargs):
        self._fix_gid = has_gid
        self._verify = self.boolParam(verify)
        self._ignore_prefix = self.boolParam(ignore_prefix)
        NLFastParser.__init__(self, f, verify=self._verify, **kwargs)

    def process(self, line):
        if self._ignore_prefix:
            ts_pos = line.find('ts=')
            if ts_pos < 0:
                return ()
            if ts_pos > 0:
                line = line[ts_pos:]
        datum = self.parseLine(line)
        if self._fix_gid:
            datum['guid'] = datum['gid']
            del datum['gid']
        return (
         datum,)