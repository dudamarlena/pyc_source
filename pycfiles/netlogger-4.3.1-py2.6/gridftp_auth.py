# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/gridftp_auth.py
# Compiled at: 2010-04-29 16:01:18
"""
Parse GridFTP (server) authorization logs.

For examples of the input format, see files in tests/data/gridftp-auth.*
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: gridftp_auth.py 24755 2010-04-29 20:01:18Z dang $'
import logging, re, sys
from netlogger.parsers.base import BaseParser
from netlogger.nldate import parseSyslogDate
from netlogger import util

def ns(s):
    return 'gridftp_auth.%s' % s


class Parser(BaseParser):
    """Parse GridFTP server authorization logs.
    
    Parameters:
    - error_events {yes,no,yes*}: If 'yes', hold on to transfer-starting 
    events untila matching transfer-end is encountered. 
    If none is found, or a transfer-end 
    precedes a transfer-start, report a transfer-error event instead.
    - error_timeout {*h,*m,*s,24h*}: How long to wait for the 
    transfer-end event. Ignored if error_events is False.
    """

    def __init__(self, f, error_events=True, error_timeout='24h', **kw):
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._batch = []
        self._cur_pid = None
        self._gen_errs = error_events
        if self._gen_errs:
            self._hdr_host = None
            self._match_events = {}
            self._gen_err_ts = 3000000000
            try:
                self._err_timeout = util.timeToSec(error_timeout)
            except ValueError, E:
                raise ValueError('error_timeout parameter cannot be parsed: %s' % E)

        pid_str = '^\\[(\\d+)\\]'
        self._line_re = re.compile(pid_str + '(.*?)::.(.*)$')
        return

    def process(self, line):
        self.log.debug('process.start', line=line)
        m = self._line_re.match(line)
        if not m:
            self.log.debug('process.end', status=0, n=0)
            return ()
        (pid, date, message) = m.groups()
        msg_type = 0
        if message.startswith('Server'):
            event = dict(event=ns('start'))
        elif message.startswith('Configuration'):
            event = dict(event=ns('config'))
        elif message.startswith('New'):
            m = re.search('from:\\s*(\\S+)', message)
            (host, port) = m.group(1).split(':')
            event = dict(event=ns('conn.start'), host=host, port=int(port))
        elif message.startswith('DN'):
            m = re.search('DN\\s+(\\/.*)\\s+successfully', message)
            event = dict(event=ns('conn.auth.dn'), DN=m.group(1))
        elif message.startswith('User'):
            m = re.search('User\\s+(\\S+)\\s+successfully', message)
            event = dict(event=ns('conn.auth.user'), user=m.group(1))
        elif message.startswith('Starting'):
            m = re.search('transfer "([^"]*)"', message)
            event = dict(event=ns('conn.transfer.start'), filename=m.group(1))
            msg_type = 1
        elif message.startswith('Finished'):
            m = re.search('transferring "([^"]*)"', message)
            event = dict(event=ns('conn.transfer.end'), filename=m.group(1))
            msg_type = 2
        elif message.startswith('Closed'):
            event = dict(event=ns('end'))
        else:
            self.log.debug('process.end', status=0, n=0)
            return ()
        event['ts'] = parseSyslogDate(date)
        event['PID'] = int(pid)
        event_list = (event,)
        if self._gen_errs:
            if msg_type > 0:
                event_list = self._generateErrors(event, msg_type)
            if event['ts'] >= self._gen_err_ts:
                event_list += self._scanErrors(event['ts'])
        self.log.debug('process.end', status=0, n=1)
        return event_list

    def _generateErrors(self, event, msg_type):
        """Generate error events if one of the following two types 
        of event is not found (but the other is):
            [15317] Tue Aug  1 16:28:24 2006 :: Starting to transfer "/usr/common/homes/s/sakrejda/123".
            [15317] Tue Aug  1 16:28:24 2006 :: Finished transferring "/usr/common/homes/s/sakrejda/123".
         The first is msg_type = 1, the second is msg_type = 2
         """
        if self._hdr_host is None:
            self._hdr_host = self.getHeaderValue('host') is not None
        if self._hdr_host:
            host = self.getHeaderValue('host') or ''
        else:
            host = ''
        key = '%s#%d#%s' % (host, event['PID'], event['filename'])
        if self._match_events.has_key(key):
            event2 = self._match_events[key]
            if event['event'] == event2['event']:
                self._makeIntoError(event)
                self._addErrorEvent(key, event2)
            else:
                del self._match_events[key]
            result = (
             event,)
        elif msg_type == 2:
            self._makeIntoError(event)
            result = (event,)
        else:
            self._addErrorEvent(key, event)
            result = (event,)
        return result

    def _makeIntoError(self, event):
        """Make the given event into an error event.
        Changes event in-place.
        """
        event['status'] = -1
        e = event['event']
        last_dot = e.rfind('.')
        e_new = e[:last_dot] + '.error'
        event['event'] = e_new

    def _addErrorEvent(self, key, e):
        self._match_events[key] = e
        tmout = e['ts'] + self._err_timeout
        self._gen_err_ts = min(self._gen_err_ts, tmout)

    def _scanErrors(self, ts):
        """Remove and return all timed-out events
        """
        remove = []
        event_list = []
        new_err_ts = 100000000000
        for (key, event) in self._match_events.items():
            event_ts = event['ts']
            if event_ts < self._gen_err_ts:
                e = self._match_events[key]
                self._makeIntoError(e)
                event_list.append(e)
                remove.append(key)
            new_err_ts = min(new_err_ts, event_ts)

        for key in remove:
            del self._match_events[key]

        self._gen_err_ts = min(new_err_ts, self._gen_err_ts)
        return tuple(event_list)