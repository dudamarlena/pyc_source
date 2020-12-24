# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/nlganglia.py
# Compiled at: 2009-12-08 17:43:30
"""
Ganglia / NetLogger interface module

Dan Gunter, dkgunter@lbl.gov
"""
__rcsid__ = '$Id: nlganglia.py 23923 2009-09-18 22:42:26Z ksb $'
import re, socket, time, nlapi
from netlogger.nllog import DoesLogging, get_logger

def get_log():
    return get_logger('nlganglia')


class Gmetad(DoesLogging):
    """Class representing a gmetad server, with convenient defaults for
    reading off the local host.
     
    To read locally: g = Gmetad() ; xmlstring = g.read()
    To read from remote: g = Gmetad('remote.host'); xstr = g.read()
    """

    def __init__(self, host='localhost', port=8161, default_timeout=0.5):
        """Initialize with location of server and
        a default value for a timeout (in seconds) to wait
        for some data to be returned when we connect.
        """
        DoesLogging.__init__(self)
        self.host, self.port, self.tmout = host, port, default_timeout

    def read(self, timeout=None):
        """Connect to gmetad and return its output as a string.
        """
        self.log.debug('read.start')
        sock = socket.socket()
        sock.connect((self.host, self.port))
        timeout = (timeout, self.tmout)[(timeout is None)]
        sock.settimeout(timeout)
        data = []
        while 1:
            buf = sock.recv(65536)
            if buf == '':
                break
            data.append(buf)

        self.log.debug('read.end', status=0, num=len(data))
        return ('').join(data)


attrs_re = re.compile('([A-Z]+)="([^"]*)"')

def parse(buf):
    """Parse XML returned by gmetad into BP-formatted log lines
    and for each return a pair (metric-name, log-line). 
    Explicitly returning the metric name makes filtering on metric
    very easy.
    """
    get_log().debug('parse.start')
    ts = time.time()
    log = nlapi.Log()
    log.setLevel(nlapi.Level.INFO)
    results = []
    log_meta = {}
    state = 'hdr'
    for line in buf.split('\n'):
        line = line.strip()
        if state == 'hdr':
            if line.startswith('<GANGLIA_XML'):
                state = 'body'
        elif state == 'body':
            if line.startswith('<METRIC'):
                attrs = {}
                for (k, v) in attrs_re.findall(line):
                    attrs[k.lower()] = v

                metric = attrs['name']
                event = 'ganglia.metric.%s' % metric
                del attrs['name']
                if attrs['units'] == '':
                    attrs['units'] = 'none'
                log_str = log.write(event=event, ts=ts, **attrs)
                results.append((metric, log_str))
            elif line.startswith('</'):
                if line.startswith('</GANGLIA_XML'):
                    state = 'done'
            else:
                attrs = attrs_re.findall(line)
                pfx = line[1:line.find(' ')].lower()
                for (k, v) in attrs:
                    log_meta['%s.%s' % (pfx, k.lower())] = v

                log.setMeta(None, **log_meta)

    get_log().debug('parse.end', status=0, num=len(results))
    return results