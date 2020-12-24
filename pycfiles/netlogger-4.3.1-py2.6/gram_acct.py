# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/gram_acct.py
# Compiled at: 2010-04-29 00:14:32
"""
Parse Globus GRAM accounting logs
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: gram_acct.py 24753 2010-04-29 04:14:31Z dang $'
from logging import DEBUG
import re, time
from netlogger.parsers.base import BaseParser
SAMPLE_LOG = '\nJMA 2008/10/24 11:33:47 GATEKEEPER_JM_ID 2008-10-24.11:33:45.0000019999.0000000000 mapped to jmatykie (44581, 4002)\nJMA 2008/10/24 11:33:47 GATEKEEPER_JM_ID 2008-10-24.11:33:45.0000019999.0000000000 has GRAM_SCRIPT_JOB_ID 9636173|/u/jmatykie/.globus/job/pdsfgrid4.nersc.gov/20020.1224873225/stdout|/u/jmatykie/.globus/job/pdsfgrid4.nersc.gov/20020.1224873225/stderr manager type sge\n'
NS = 'globus.acct.%s'
JOB_EVENT = NS % 'job'

def parseDate(dt, tm):
    """Parse dt=2008/10/24, tm=11:33:45, as localtime
    """
    (y, m, d) = map(int, dt.split('/'))
    (hr, mins, sec) = map(int, tm.split(':'))
    sec = time.mktime((y, m, d, hr, mins, sec, 0, 0, -1))
    return sec


JMID_PFX = 'JMA (\\d\\d\\d\\d\\/\\d\\d\\/\\d\\d) (\\d\\d:\\d\\d:\\d\\d) GATEKEEPER_JM_ID ' + '\\d\\d\\d\\d-\\d\\d-\\d\\d.\\d\\d:\\d\\d:\\d\\d\\.(\\d+\\.\\d+) '
JMID_RE = re.compile(JMID_PFX + '(\\S+)')
MAPPED_RE = re.compile(' to (\\S+) \\((\\d+),.*(\\d+)\\)')
FOR_RE = re.compile(' (.*) on (.*)')
GSJI_RE = re.compile(' GRAM_SCRIPT_JOB_ID (?:(\\d+)\\|.*/(\\d+\\.\\d+)/stdout\\|.*/stderr|(\\d+)) manager type (.*)')

class Parser(BaseParser):
    """Globus GRAM accounting log parser
    Output events: globus.acct.job
    """

    def __init__(self, f, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._job_user = {}

    def process(self, line):
        result = ()
        m = JMID_RE.match(line)
        if m is None or len(m.groups()) != 4:
            raise ValueError("Invalid JMA line, '%s'" % line)
        (dt, tm, job_key, cmd) = m.groups()
        s = line[m.end():]
        if cmd == 'mapped':
            m = MAPPED_RE.match(s)
            if m is None or len(m.groups()) != 3:
                raise ValueError("Invalid 'mapped to' JobManager line")
            (username, uid, gid) = m.groups()
            self._addData(job_key, {'user.id': uid, 'group.id': gid, 'user': username})
        elif cmd == 'for':
            m = FOR_RE.match(s)
            if m is None or len(m.groups()) != 2:
                raise ValueError("Invalid 'for' JobManager line")
            (dn, host) = m.groups()
            self._addData(job_key, {'DN': dn, 'host': host})
        elif cmd == 'has':
            m = GSJI_RE.match(s)
            if m is None or len(m.groups()) < 2:
                raise ValueError("Invalid 'GRAM_SCRIPT_JOB_ID' JobManager line")
            sched_type = m.groups()[(-1)]
            if sched_type == 'sge':
                (sched_id, gram_id) = m.groups()[0:2]
            elif sched_type == 'condor':
                sched_id, gram_id = m.group(3), 'None'
            elif sched_type == 'managedfork':
                sched_id, gram_id = m.group(3), 'None'
            else:
                mushball = ''
                for data in m.groups()[0:3]:
                    if data:
                        mushball += data

                sched_id, gram_id = mushball, 'None'
            e = {'ts': parseDate(dt, tm), 'event': JOB_EVENT, 
               'jm.id': job_key, 
               'sched.id': sched_id, 
               'gram.id': gram_id, 
               'sched.type': sched_type}
            e.update(self._job_user.get(job_key, {}))
            result = (e,)
        return result

    def _addData(self, key, data):
        if self._job_user.has_key(key):
            self._job_user[key].update(data)
        else:
            self._job_user[key] = data