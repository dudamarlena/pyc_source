# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/Handlers/UploadTorrents.py
# Compiled at: 2008-10-19 12:19:52
"""========================
Upload Torrents
========================
A session-based HTTP request handler for HTTPServer.
UploadTorrents saves .torrent files that are uploaded to it as POST
data and stores the number of .torrent files save to a file "meta.txt".
"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
import Kamaelia.Protocol.HTTP.ErrorPages
Sessions = {}

def UploadTorrentsWrapper(request):
    """Returns an UploadTorrents component, manages that components lifetime and access."""
    sessionid = request['uri-suffix']
    if Sessions.has_key(sessionid):
        session = Sessions[sessionid]
        if session['busy']:
            return ErrorPages.websiteErrorPage(500, 'Session handler busy')
        else:
            return session['handler']
    else:
        session = {'busy': True, 'handler': UploadTorrents(sessionid)}
        Sessions[sessionid] = session
        return session['handler']


class UploadTorrents(component):

    def __init__(self, sessionid):
        super(UploadTorrents, self).__init__()
        self.sessionid = sessionid

    def main(self):
        counter = 0
        while 1:
            counter += 1
            torrentfile = fopen(str(counter) + '.torrent')
            metafile = fopen('meta.txt')
            metafile.write(str(counter))
            metafile.close()
            resource = {'statuscode': '200', 
               'data': '<html><body>%d</body></html>' % counter, 
               'incomplete': False, 
               'content-type': 'text/html'}
            receivingpost = False
            while receivingpost:
                while self.dataReady('inbox'):
                    msg = self.recv('inbox')
                    torrentfile.write(msg)

                while self.dataReady('control'):
                    msg = self.recv('control')
                    if isinstance(msg, producerFinished):
                        receivingpost = False

                if receivingpost:
                    yield 1
                    self.pause()

            torrentfile.close()
            self.send(resource, 'outbox')
            self.send(producerFinished(self), 'signal')
            Sessions[self.sessionid]['busy'] = False
            self.pause()
            yield 1


__kamaelia_components__ = (UploadTorrents,)