# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/pbs.py
# Compiled at: 2010-04-29 16:01:18
"""
Parse contents of PBS accounting file

PBS log format: 
timestamp;rec_type;job_id;pbs_record
in the above line "pbs_record" is a set of key value pairs

sample line:
07/23/2008 00:43:53;S;545489.myhost.domain.com;user=foo group=bar account=testrepo jobname=STDIN queue=debug ctime=1216799025 qtime=1216799025 etime=1216799025 start=1216799033 owner=foo@myhost.domain.com exec_host=nodename343/1+nodename343/0 Resource_List.neednodes=nodename343:ppn=2 Resource_List.nodect=1 Resource_List.nodes=1:ppn=2 Resource_List.walltime=00:30:00 
"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id: pbs.py 24755 2010-04-29 20:01:18Z dang $'
import time
from netlogger.parsers.base import BaseParser
from netlogger import util

class Parser(BaseParser):
    """Parse contents of PBS accounting file.

    Parameters:
        - site {STRING,org.mydomain*}: Site name, for site-specific processing.
          Current recognized sites are: *.nersc.gov = NERSC.
        - suppress_hosts {yes,no,no*}: If yes, do not include the list of hosts 
          in the output. This list could be very long if the job has a high degree
          of parallelism.
    """
    DEFAULT_KEYMAP = {'Exit_status': 'status'}

    def __init__(self, f, site='org.mydomain', suppress_hosts=False, **kw):
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._site = site
        self._suppress_hosts = util.as_bool(suppress_hosts)
        self._keymap = self.DEFAULT_KEYMAP
        if self._site.endswith('.nersc.gov'):
            self._other = self._otherNersc
        else:
            self._other = None
        return

    def _otherNersc(self, key, value):
        """Process NERSC 'other' field.
        """
        (qsubpid, ppid, submit_host) = value.split(':', 2)
        return (('qsubpid', qsubpid), ('ppid', ppid), ('submit_host', submit_host))

    def _resourceListNodes(self, key, value):
        """Process NERSC 'Resource_List.nodes' field.
        """
        if value.find(':ppn=') > -1:
            (nodes, ppnstring) = value.split(':', 1)
            (ppnkey, ppnvalue) = ppnstring.split('=', 1)
            return (
             (
              'nodes', nodes), (ppnkey, ppnvalue), ('num_procs', int(nodes) * int(ppnvalue)))
        else:
            return (
             key, value)

    def process(self, line):
        """Process one PBS job record.
        """
        (timestamp, rectype, jobid, record) = line.split(';', 3)
        parsed_ts = time.strptime(timestamp, '%m/%d/%Y %H:%M:%S')
        d = dict(ts=time.mktime(parsed_ts), event='pbs.job.' + rectype, type=rectype, job__id=jobid, site=self._site)
        if record:
            for item in record.split(' '):
                (k, v) = item.split('=', 1)
                if k == 'other' and self._other:
                    for (kk, vv) in self._other(k, v):
                        d[kk] = vv

                elif k == 'Resource_List.nodes':
                    for (kk, vv) in self._resourceListNodes(k, v):
                        d[kk] = vv

                elif self._suppress_hosts and (k == 'exec_host' or k == 'Resource_List.neednodes'):
                    continue
                else:
                    k = self._keymap.get(k, k)
                    d[k] = v

        return (
         d,)