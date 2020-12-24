# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/reportinghttp.py
# Compiled at: 2014-06-18 08:36:36
"""HTTPHandler that supports a callback method for progress reports.
"""
import urllib2, httplib, logging
__all__ = [
 'urlopen']
logging.basicConfig()
LOG = logging.getLogger(__name__)
progress_callback = None

class ReportingSocket(object):
    """Wrapper around a socket. Gives progress report through a
    callback function.
    """
    min_chunksize = 10240

    def __init__(self, socket):
        self.socket = socket

    def sendall(self, bits):
        """Sends all data, calling the callback function for every
        sent chunk.
        """
        global progress_callback
        LOG.debug('SENDING: %s...' % bits[0:30])
        total = len(bits)
        sent = 0
        chunksize = max(self.min_chunksize, total // 100)
        while len(bits) > 0:
            send = bits[0:chunksize]
            self.socket.sendall(send)
            sent += len(send)
            if progress_callback:
                progress = float(sent) / total * 100
                progress_callback(progress, sent == total)
            bits = bits[chunksize:]

    def makefile(self, mode, bufsize):
        """Returns a file-like object for the socket."""
        return self.socket.makefile(mode, bufsize)

    def close(self):
        """Closes the socket."""
        return self.socket.close()


class ProgressHTTPConnection(httplib.HTTPConnection):
    """HTTPConnection that gives regular progress reports during
    sending of data.
    """

    def connect(self):
        """Connects to a HTTP server."""
        httplib.HTTPConnection.connect(self)
        self.sock = ReportingSocket(self.sock)


class ProgressHTTPHandler(urllib2.HTTPHandler):
    """HTTPHandler that gives regular progress reports during sending
    of data.
    """

    def http_open(self, req):
        return self.do_open(ProgressHTTPConnection, req)


def set_callback(method):
    """Sets the callback function to use for progress reports."""
    global progress_callback
    if not hasattr(method, '__call__'):
        raise ValueError('Callback method must be callable')
    progress_callback = method


def urlopen(url_or_request, callback, body=None):
    """Opens an URL using the ProgressHTTPHandler."""
    set_callback(callback)
    opener = urllib2.build_opener(ProgressHTTPHandler)
    return opener.open(url_or_request, body)


if __name__ == '__main__':

    def upload(progress, finished):
        """Upload progress demo"""
        LOG.info('%3.0f - %s' % (progress, finished))


    conn = urlopen('http://www.flickr.com/', 'x' * 10245, upload)
    data = conn.read()
    LOG.info('Read data')
    print data[:100].split('\n')[0]