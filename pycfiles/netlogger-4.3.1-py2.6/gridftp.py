# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/gridftp.py
# Compiled at: 2010-10-15 14:38:49
"""
Parse GridFTP (server) transfer logs.

Input format:

DATE=20070215110703.2102 HOST=pdsfgrid1.nersc.gov PROG=globus-gridftp-server NL.EVNT=FTP_INFO START=20070215110702.763298 USER=rosheck FILE=//tmp/YY5raYFdo5.local_out_moved BUFFER=0 BLOCK=262144 NBYTES=55 VOLUME=/ STREAMS=1 STRIPES=1 DEST=[129.79.4.64] TYPE=RETR CODE=226
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: gridftp.py 26609 2010-10-15 18:38:47Z dang $'
import calendar, socket, sys
from logging import DEBUG
from netlogger.parsers.base import BaseParser, parseDate
from netlogger import util

class Parser(BaseParser):
    """Parse GridFTP (server) transfer logs.

    Parameters:
        - one_event {yes,no,yes*}: If 'yes', produce a single event 
           for the transfer; if False, produce a start/end event pair.
        - hostnames {yes,no,no*}: If 'yes' look up things that look like
          IP addresses to attempt to find the fully qualified 
          domain name, for both the HOST and DEST attributes.
          Lookups are cached, so changes to system tables may not be
          reflected until the next invocation.
    """

    def __init__(self, f, one_event=True, hostnames='no', ignore_prefix='no', **kw):
        """Constructor.
        """
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._one = util.as_bool(one_event)
        self._ignore_prefix = util.as_bool(ignore_prefix)
        self._ints = dict.fromkeys(('buffer', 'block', 'nbytes', 'streams', 'stripes',
                                    'code'))
        if util.as_bool(hostnames):
            self._hostnames, self._failedhostnames = {}, {}
        else:
            self._hostnames = None
        if self._dbg:
            self._count = 0
        return

    def process(self, line):
        if self._dbg:
            self._count += 1
            self.log.debug('process.start', count=self._count)
        if self._ignore_prefix:
            ts_pos = line.find('DATE=')
            if ts_pos < 0:
                raise ValueError("No 'DATE=' found")
            if ts_pos > 0:
                line = line[ts_pos:]
        elif not line.startswith('DATE='):
            raise ValueError("Does not start with 'DATE='")
        d = {}
        dates = ''
        for nvp in line.split():
            try:
                (name, value) = nvp.split('=', 1)
            except:
                self.log.warn('process.split.error', field=nvp)
                continue
            else:
                nm = name.lower()
                if nm in ('start', 'date'):
                    if value[0] == '0':
                        value = '20' + value[2:]
                    dates += value
                    bpdate = value[:4] + '-' + value[4:6] + '-' + value[6:8] + 'T' + value[8:10] + ':' + value[10:12] + ':' + value[12:14] + '.'
                    frac = value[15:]
                    frac = '0' * (6 - len(frac)) + frac
                    bpdate += frac + 'Z'
                    d[nm] = parseDate(bpdate)
                    if nm == 'date' and self._one:
                        end_str = bpdate
                elif nm == 'nl.evnt':
                    d['event'] = value
                elif self._ints.has_key(nm):
                    d[nm] = int(value)
                elif nm == 'dest':
                    dest = value[1:-1]
                    if self._hostnames is not None:
                        dest = self._lookup_host(dest)
                    d[nm] = dest
                elif nm == 'host':
                    if self._hostnames is not None:
                        value = self._lookup_host(value)
                    d[nm] = value
                else:
                    d[nm] = value

        if self._dbg:
            self.log.trace('process.values', v=d)
        try:
            start, end = d['start'], d['date']
            d['dur'] = end - start
        except KeyError, err:
            self.log.exc('process.end', err, reason='missing values')
            return ()
        else:
            del d['start']
            del d['date']
            if self._one:
                d['ts'] = start
                d['end'] = end_str
                result = (d,)
            else:
                d1 = d
                d2 = d.copy()
                d1['ts'] = start
                d1['event'] = d1['event'] + '.start'
                d2['ts'] = end
                d2['event'] = d2['event'] + '.end'
                result = (d1, d2)
            if self._dbg:
                self.log.debug('process.end', size=len(result), status=0, count=self._count)

        return result

    def _lookup_host(self, addr):
        if self._hostnames.has_key(addr):
            hostname = self._hostnames[addr]
        else:
            if self._failedhostnames.has_key(addr):
                hostname = addr
            else:
                dhost = None
                try:
                    dhost = socket.getfqdn(socket.gethostbyaddr(addr)[0])
                    hostname = self._hostnames[addr] = dhost
                except socket.error:
                    hostname = addr
                    self._failedhostnames[addr] = True

            return hostname