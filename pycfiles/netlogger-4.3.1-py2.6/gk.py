# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/gk.py
# Compiled at: 2010-04-29 00:14:32
"""
Simplified Globus Toolkit GT2 Gatekeeper log parser.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: gk.py 24753 2010-04-29 04:14:31Z dang $'
from logging import DEBUG
import re
from netlogger.nlapi import Level
from netlogger.parsers.base import BaseParser
from netlogger.nldate import parseSyslogDate, getLocaltimeISO

def _ns(e):
    return 'globus.gk.%s' % e


class Parser(BaseParser):
    """Simplified Globus Toolkit GT2 Gatekeeper log parser.

    All event types are prefixed with 'globus.gk.'
    The event type suffix is one of the following:
    start (first event), auth (user authorized),
    info (DN, host, and JobManager ID), end (last event, success or failure),
    unknown (some other event).
    
    Parameters:
        - drop_unknown {yes,no,yes*}: If yes, don't emit unrecognized events
    """
    PID_RE = re.compile('\\s*PID: (?P<pid>\\d+) -- Notice: (?P<level>\\d+):\\s*(?P<rest>.*)')
    FAIL_RE = re.compile('\\s*PID: (?P<pid>\\d+) -- Failure:\\s*(?P<msg>.*)')
    LOOKUP_FAIL_RE = re.compile('Gridmap lookup failure:.* map (?P<dn>.*)')
    START_RE = re.compile('pid=(?P<pid>\\d+) starting at (?P<date>.*)')
    CONN_RE = re.compile('[Gg]ot connection (?P<ip>(?:\\d\\d?\\d?\\.){3}\\d\\d?\\d?) at (?P<date>.*)')
    AUTH_RE = re.compile('[Aa]uthenticated globus user:\\s*(?P<dn>.*)')
    END_RE = re.compile('[Cc]hild (?P<pid>\\d+) started')
    DATE_PAT = '\\d\\d\\d\\d-\\d\\d-\\d\\d\\.\\d\\d:\\d\\d:\\d\\d'
    JM_RE = re.compile('GATEKEEPER_JM_ID (?P<date>%s)\\.(?P<job>\\S+) for (?P<dn>.*?) on (?P<ip>.*)' % DATE_PAT)

    def __init__(self, f, drop_unknown=True, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self._cur_time = 0
        self._tz = None
        self._unknown = not drop_unknown
        return

    def process(self, line):
        if line.startswith('TIME'):
            self._setTime(line[6:])
            return ()
        else:
            m = self.FAIL_RE.match(line)
            if m:
                msg = m.group('msg')
                pid = int(m.group('pid'))
                e = {'ts': self._cur_time, 'event': _ns('end'), 
                   'status': -1, 'msg': msg, 'process.id': pid, 
                   'level': Level.ERROR}
                return (
                 e,)
            m = self.LOOKUP_FAIL_RE.match(line)
            if m:
                e = {'ts': self._cur_time, 'event': _ns('error'), 'msg': 'Gridmap lookup failure', 
                   'DN': m.group('dn'), 
                   'level': Level.ERROR}
                return (
                 e,)
            m = self.PID_RE.match(line)
            if not m:
                if self._unknown:
                    return (
                     {'ts': self._cur_time, 'event': _ns('unknown'), 'process.id': -1, 
                        'msg': line},)
                else:
                    return ()
            pid = int(m.group('pid'))
            level = int(m.group('level'))
            line = m.group('rest')
            e = {'ts': self._cur_time, 'process.id': pid}
            m = self.JM_RE.search(line)
            if m:
                tmp_date = ('T').join(m.group('date').split('.'))
                if not self._tz:
                    self._tz = getLocaltimeISO(tmp_date)
                iso_date = tmp_date + self._tz
                e.update({'ts': iso_date, 'event': _ns('info'), 
                   'DN': m.group('dn'), 
                   'host': m.group('ip'), 
                   'jm.id': m.group('job')})
                return (
                 e,)
            m = self.START_RE.search(line)
            if m:
                self._setTime(m.group('date'))
                pid = int(m.group('pid'))
                e.update({'ts': self._cur_time, 'event': _ns('start'), 'process.id': pid})
                return (
                 e,)
            m = self.CONN_RE.search(line)
            if m:
                self._setTime(m.group('date'))
                ip = m.group('ip')
                e.update({'ts': self._cur_time, 'event': _ns('conn'), 'host': ip})
                return (
                 e,)
            m = self.AUTH_RE.search(line)
            if m:
                e.update({'event': _ns('auth'), 'DN': m.group('dn')})
                return (
                 e,)
            m = self.END_RE.search(line)
            if m:
                cpid = int(m.group('pid'))
                e.update({'event': _ns('end'), 'status': 0, 'child.process.id': cpid})
                return (
                 e,)
            if self._unknown:
                e.update({'event': _ns('unknown'), 'msg': line})
                return (
                 e,)
            return ()

    def _setTime(self, date):
        t = parseSyslogDate(date)
        if t < self._cur_time:
            self.log.debug('setTime.ignoreEarlier', earlier=t, current=self._cur_time)
        else:
            self._cur_time = t