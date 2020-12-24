# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/dns.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import os, re, socket, threading, time

class DNSQuery(object):
    """
    Used for making fake DNS resolution responses based on received
    raw request

    Reference(s):
        http://code.activestate.com/recipes/491264-mini-fake-dns-server/
        https://code.google.com/p/marlon-tools/source/browse/tools/dnsproxy/dnsproxy.py
    """

    def __init__(self, raw):
        self._raw = raw
        self._query = ''
        type_ = ord(raw[2]) >> 3 & 15
        if type_ == 0:
            i = 12
            j = ord(raw[i])
            while j != 0:
                self._query += raw[i + 1:i + j + 1] + '.'
                i = i + j + 1
                j = ord(raw[i])

    def response(self, resolution):
        """
        Crafts raw DNS resolution response packet
        """
        retVal = ''
        if self._query:
            retVal += self._raw[:2]
            retVal += b'\x85\x80'
            retVal += self._raw[4:6] + self._raw[4:6] + '\x00\x00\x00\x00'
            retVal += self._raw[12:12 + self._raw[12:].find('\x00') + 5]
            retVal += b'\xc0\x0c'
            retVal += '\x00\x01'
            retVal += '\x00\x01'
            retVal += '\x00\x00\x00 '
            retVal += '\x00\x04'
            retVal += ('').join(chr(int(_)) for _ in resolution.split('.'))
        return retVal


class DNSServer(object):

    def __init__(self):
        self._requests = []
        self._lock = threading.Lock()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('', 53))
        self._running = False

    def pop(self, prefix=None, suffix=None):
        """
        Returns received DNS resolution request (if any) that has given
        prefix/suffix combination (e.g. prefix.<query result>.suffix.domain)
        """
        retVal = None
        with self._lock:
            for _ in self._requests:
                if prefix is None and suffix is None or re.search('%s\\..+\\.%s' % (prefix, suffix), _, re.I):
                    retVal = _
                    self._requests.remove(_)
                    break

        return retVal

    def run(self):
        """
        Runs a DNSServer instance as a daemon thread (killed by program exit)
        """

        def _():
            try:
                try:
                    self._running = True
                    while True:
                        data, addr = self._socket.recvfrom(1024)
                        _ = DNSQuery(data)
                        self._socket.sendto(_.response('127.0.0.1'), addr)
                        with self._lock:
                            self._requests.append(_._query)

                except KeyboardInterrupt:
                    raise

            finally:
                self._running = False

        thread = threading.Thread(target=_)
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    server = None
    try:
        try:
            server = DNSServer()
            server.run()
            while server._running:
                while True:
                    _ = server.pop()
                    if _ is None:
                        break
                    else:
                        print '[i] %s' % _

                time.sleep(1)

        except socket.error as ex:
            if 'Permission' in str(ex):
                print '[x] Please run with sudo/Administrator privileges'
            else:
                raise
        except KeyboardInterrupt:
            os._exit(0)

    finally:
        if server:
            server._running = False