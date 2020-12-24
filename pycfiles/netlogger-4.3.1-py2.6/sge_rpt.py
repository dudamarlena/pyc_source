# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/sge_rpt.py
# Compiled at: 2010-04-29 16:01:18
"""
Parse output file from Sun Grid Engine 'reporting'

For sample input, see netlogger/tests/data/sge_rpt-basic.log
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: sge_rpt.py 24755 2010-04-29 20:01:18Z dang $'
from logging import DEBUG
import re, sys, time
from netlogger.parsers.base import BaseParser, autoParseValue
from netlogger import util
NS = 'sge.rpt'
EVENT_HOSTC = 'sge.rpt.hc'
EVENT_JOBL = 'sge.rpt.jl'
RSRC_FIELD = 'r'
VALUE_FIELD = 'v'
MAX_FIELD = 'max'
MAX_SFX = '.max'

class Parser(BaseParser):
    """Parse output file from Sun Grid Engine 'reporting' logs.
    The parameters control which types of SGE reporting output are parsed.
    With no parameters, no types are parsed.

    Parameters:
        - host_consumable {yes,no,no*}: Parse 'host_consumable' records.
        - hc_perhost {yes,no,no*}: Show per-host as well as 'global' records.
        - hc_one {yes,no,yes*}: Produce 1 event with all host consumable attributes.
        - hc_attr {REGEX}: Regex for host consumable attributes to include
        - hc_delta {yes,no,no*}: If yes, only show changed values.
        - job_log {yes,no,no*}: If yes, parse  'job_log' and 'new_job' records.
    """

    def __init__(self, f, host_consumable=False, job_log=False, hc_one=True, hc_attr='', hc_delta=0, hc_perhost=False, **kw):
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        host_consumable = self.boolParam(host_consumable)
        if host_consumable:
            self._hc_one = self.boolParam(hc_one)
            self._hc_host = self.boolParam(hc_perhost)
            if hc_attr:
                self._hc_re = re.compile(hc_attr)
            else:
                self._hc_re = None
            if self.boolParam(hc_delta):
                self._hc_last = {}
            else:
                self._hc_last = None
        job_log = self.boolParam(job_log)
        self._parsers = [
         (
          False, self._hostConsumable)[host_consumable],
         (
          False, self._jobLog)[job_log]]
        self._parsers = filter(None, self._parsers)
        return

    def process(self, line):
        if not self._parsers:
            return ()
        fields = line.split(':')
        for parse_fn in self._parsers:
            events = parse_fn(fields)
            if events:
                break

        return events

    def _hostConsumable(self, fields):
        if len(fields) != 6:
            return ()
        else:
            if fields[1] != 'host_consumable':
                return ()
            else:
                host = fields[2]
                if not self._hc_host and host != 'global':
                    return ()
                ts = float(fields[0])
                if self._hc_one:
                    event = {'ts': ts, 'event': EVENT_HOSTC, 'host': host}
                else:
                    events = []
                for value in fields[5].split(','):
                    vf = value.split('=')
                    if self._hc_re and not self._hc_re.match(vf[0]):
                        continue
                    if self._hc_last is not None:
                        prev = self._hc_last.get(vf[0], None)
                        if vf[1] == prev:
                            continue
                        self._hc_last[vf[0]] = vf[1]
                    if self._hc_one:
                        event[vf[0]] = float(vf[1])
                        event[vf[0] + MAX_SFX] = float(vf[2])
                    else:
                        event = {'ts': ts, 'event': EVENT_HOSTC, 'host': host, RSRC_FIELD: vf[0], 
                           VALUE_FIELD: float(vf[1]), MAX_FIELD: float(vf[2])}
                        events.append(event)

                if self._hc_one:
                    return [event]
                return events
            return

    def _jobLog(self, fields):
        if len(fields) > 6 and fields[1] == 'job_log':
            msg = fields[(-1)]
            state = fields[3]
            if state == 'finished':
                if not msg.endswith('exited'):
                    state = 'deleting'
            return (
             {'ts': float(fields[0]), 'event': EVENT_JOBL, 'state': state, 
                'job.id': fields[4], 
                'host': fields[9], 
                'user': fields[14], 
                'group': fields[15], 
                'proj': fields[16]},)
        else:
            return ()