# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/HTTPHelpers.py
# Compiled at: 2008-10-19 12:19:52
"""Helper classes and components for HTTP"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown

class HTTPMakePostRequest(component):
    """    HTTPMakePostRequest is used to turn messages into HTTP POST requests
    for SimpleHTTPClient.
    """

    def __init__(self, uploadurl):
        super(HTTPMakePostRequest, self).__init__()
        self.uploadurl = uploadurl

    def main(self):
        while 1:
            yield 1
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                msg = {'url': self.uploadurl, 'postbody': msg}
                self.send(msg, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()


__kamaelia_components__ = (HTTPMakePostRequest,)
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    postscript = raw_input('Post Script URL: ')
    pipeline(ConsoleReader(eol=''), HTTPMakePostRequest(postscript), SimpleHTTPClient()).run()