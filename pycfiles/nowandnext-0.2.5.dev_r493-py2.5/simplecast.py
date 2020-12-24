# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/simplecast.py
# Compiled at: 2009-05-11 19:02:40
import urllib, logging, socket, exceptions
log = logging.getLogger(__name__)

class simplecast(object):
    """
    Represents a connection to a simplecast server
    """

    def __init__(self, host, port):
        assert type(host) == str
        assert type(port) == int
        self.host = host
        self.port = port

    def ping(self, query):
        assert type(query) == dict
        params = urllib.urlencode(query)
        url = 'http://%s:%s/?%s' % (self.host, self.port, params)
        log.info('Pinging: %s' % url)
        try:
            urlstream = urllib.urlopen(url)
            response = urlstream.read().strip()
            log.info('Got response: %s' % response)
            return response
        except exceptions.IOError, se:
            log.exception(se)
            log.critical('Could not ping URL: %s' % url)
            return

        return