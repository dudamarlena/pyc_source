# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/IcecastClient.py
# Compiled at: 2008-10-19 12:19:52
"""======================================
Icecast/SHOUTcast MP3 streaming client
======================================

This component uses HTTP to stream MP3 audio from a SHOUTcast/Icecast
server.

IcecastClient fetches the combined audio and metadata stream from the
HTTP server hosting the stream. IcecastDemux separates the audio data
from the metadata in stream and IcecastStreamWriter writes the audio
data to disk (discarding metadata).

Example Usage
-------------

Receive an Icecast/SHOUTcast stream, demultiplex it, and write it to a file::

    pipeline(
        IcecastClient("http://64.236.34.97:80/stream/1049"),
        IcecastDemux(),
        IcecastStreamWriter("stream.mp3"),
    ).run()

    
    
How does it work?
-----------------
The SHOUTcast/Icecast protocol is virtually identical to HTTP. As such,
IcecastClient subclasses SingleShotHTTPClient modifying the request
slightly to ask for stream metadata(e.g. track name) to be included
(by adding the icy-metadata header).
It is otherwise identical to its parent class.
"""
import string, time
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from Kamaelia.Protocol.HTTP.HTTPParser import *
from Kamaelia.Protocol.HTTP.HTTPClient import *
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.BaseIPC import IPC

def intval(mystring):
    try:
        retval = int(mystring)
    except ValueError:
        retval = None
    except TypeError:
        retval = None

    return retval


class IceIPCHeader(IPC):
    """Icecast header - content type: %(contenttype)s"""
    Parameters = [
     'contenttype']


class IceIPCMetadata(IPC):
    """Icecast stream metadata"""
    Parameters = [
     'metadata']


class IceIPCDataChunk(IPC):
    """An audio/video stream data chunk (typically MP3)"""
    Parameters = [
     'data']


class IceIPCDisconnected(IPC):
    """Icecast stream disconnected"""
    Parameters = []


class IcecastDemux(component):
    """Splits a raw Icecast stream into A/V data and metadata"""

    def dictizeMetadata(self, metadata):
        """Convert metadata that was embedded in the stream into a dictionary."""
        lines = metadata.split(';')
        metadict = {}
        for line in lines:
            splitline = line.split('=', 1)
            if len(splitline) > 1:
                key = splitline[0]
                val = splitline[1]
                if key[:1] == '\n':
                    key = key[1:]
                if val[0:1] == "'" and val[-1:] == "'":
                    val = val[1:-1]
                metadict[key] = val

        return metadict

    def main(self):
        metadatamode = False
        readbuffer = ''
        while 1:
            yield 1
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                if isinstance(msg, ParsedHTTPHeader):
                    metadatainterval = intval(msg.header['headers'].get('icy-metaint', 0))
                    if metadatainterval == None:
                        metadatainterval = 0
                    bytesUntilMetadata = metadatainterval
                    self.send(IceIPCHeader(contenttype=msg.header['headers'].get('content-type')), 'outbox')
                    print 'Metadata interval is ' + str(metadatainterval)
                elif isinstance(msg, ParsedHTTPBodyChunk):
                    readbuffer += msg.bodychunk
                elif isinstance(msg, ParsedHTTPEnd):
                    self.send(IceIPCDisconnected(), 'outbox')

            while len(readbuffer) > 0:
                if metadatainterval == 0:
                    self.send(IceIPCDataChunk(data=readbuffer), 'outbox')
                    readbuffer = ''
                else:
                    chunkdata = readbuffer[0:bytesUntilMetadata]
                    if len(chunkdata) > 0:
                        self.send(IceIPCDataChunk(data=chunkdata), 'outbox')
                    readbuffer = readbuffer[bytesUntilMetadata:]
                    bytesUntilMetadata -= len(chunkdata)
                    if len(readbuffer) > 0:
                        metadatalength = ord(readbuffer[0]) * 16
                        if len(readbuffer) >= metadatalength + 1:
                            metadictionary = self.dictizeMetadata(readbuffer[1:metadatalength + 1])
                            self.send(IceIPCMetadata(metadata=metadictionary), 'outbox')
                            bytesUntilMetadata = metadatainterval
                            readbuffer = readbuffer[metadatalength + 1:]
                        else:
                            break

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()

        return


class IcecastClient(SingleShotHTTPClient):
    """    IcecastClient(starturl) -> Icecast/SHOUTcast MP3 streaming component

    Arguments:
    - starturl    -- the URL of the stream
    """

    def formRequest(self, url):
        """Overrides the standard HTTP request with an Icecast/SHOUTcast variant
        which includes the icy-metadata header required to get metadata with the
        stream"""
        self.send('IcecastClient.formRequest()', 'debug')
        splituri = splitUri(url)
        host = splituri['uri-server']
        if splituri.has_key('uri-port'):
            host += ':' + splituri['uri-port']
        splituri['request'] = 'GET ' + splituri['raw-uri'] + ' HTTP/1.1\r\n'
        splituri['request'] += 'Host: ' + host + '\r\n'
        splituri['request'] += 'User-agent: Kamaelia Icecast Client 0.3 (RJL)\r\n'
        splituri['request'] += 'Connection: Keep-Alive\r\n'
        splituri['request'] += 'icy-metadata: 1\r\n'
        splituri['request'] += '\r\n'
        return splituri

    def main(self):
        while 1:
            self.requestqueue.append(HTTPRequest(self.formRequest(self.starturl), 0))
            while self.mainBody():
                yield 1


def IcecastStreamRemoveMetadata():

    def extraDataChunks(msg):
        if isinstance(msg, IceIPCDataChunk):
            return msg.data
        else:
            return
        return

    return PureTransformer(extraDataChunks)


class IcecastStreamWriter(component):
    Inboxes = {'inbox': 'Icecast stream', 
       'control': 'UNUSED'}
    Outboxes = {'outbox': 'UNUSED', 
       'signal': 'UNUSED'}

    def __init__(self, filename):
        super(IcecastStreamWriter, self).__init__()
        self.filename = filename

    def main(self):
        f = open(self.filename, 'wb')
        while 1:
            yield 1
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                if isinstance(msg, IceIPCDataChunk):
                    f.write(msg.data)

            self.pause()


__kamaelia_components__ = (IcecastDemux, IcecastClient, IcecastStreamWriter)
__kamaelia_prefabs__ = (IcecastStreamRemoveMetadata,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    streamurl = raw_input('Stream URL: ')
    pipeline(IcecastClient(streamurl), IcecastDemux(), IcecastStreamWriter('stream.mp3')).run()