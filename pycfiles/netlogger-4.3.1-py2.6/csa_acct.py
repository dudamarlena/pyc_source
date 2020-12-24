# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/csa_acct.py
# Compiled at: 2010-04-28 23:54:16
"""
Parse output file from SGI csa process accounting
"""
__author__ = 'Tina Declerck tinad@nersc.gov'
__rcsid__ = '$Id: csa_acct.py 000 2008-07-31 12:42:00 tinad $'
import sys, time
from netlogger import nldate
from netlogger.parsers.base import BaseParser
NS = 'csa.'
EVENT_BOTH = '%sprocess' % NS
EVENT_START = '%sprocess.start' % NS
EVENT_END = '%sprocess.end' % NS

class Parser(BaseParser):
    """SGI Comprehensive System Accounting (CSA) process accounting parser.
    See also http://oss.sgi.com/projects/csa/.

    Parameters:
       - one_event {yes,no,yes*}: csa.process instead of csa.process.start/csa.process.end

    """

    def __init__(self, f, one_event='yes', **kw):
        """
        """
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._one_event = self.boolParam(one_event)

    def process(self, line):
        parts = line.split()
        if len(parts) != 17:
            return ()
        else:
            e = {'cmd': parts[0], 'local_user': parts[1], 
               'walltime': parts[4], 
               'cputime': parts[5], 
               'ignore': parts[6], 
               'pid': parts[7], 
               'ppid': parts[8]}
            tm = (' ').join((parts[9], parts[10], parts[11], parts[2], parts[12]))
            start = nldate.parseSyslogDate(tm)
            tm = (' ').join((parts[13], parts[14], parts[15], parts[3], parts[16]))
            end = nldate.parseSyslogDate(tm)
            if self._one_event:
                e.update({'ts': start, 'event': EVENT_BOTH, 'dur': end - start})
                return (
                 e,)
            e1 = {'ts': start, 'event': EVENT_START, 'pid': e['pid'], 
               'ppid': e['ppid']}
            e.update({'ts': end, 'event': EVENT_END})
            return (e1, e)