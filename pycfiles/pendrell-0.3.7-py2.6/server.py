# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/server.py
# Compiled at: 2010-09-03 02:22:19
import os, math
from base64 import b64encode
from binascii import a2b_hex
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from pendrell import log
CHUNK_SIZE = 16384

class JunkSite(Site):

    def __init__(self, chunkSize=CHUNK_SIZE):
        Site.__init__(self, JunkRoot(chunkSize))


class JunkRoot(Resource):
    isLeaf = False

    def __init__(self, chunkSize=CHUNK_SIZE):
        Resource.__init__(self)
        self._chunkSize = chunkSize

    def getChild(self, name, request):
        log.debug('%r getting child %s for %r' % (self, name, request))
        try:
            (sizeDesc, suffix) = name.split('.')
            size = int(sizeDesc)
        except (TypeError, ValueError):
            child = Resource.getChild(self, name, request)
        else:
            suffix = suffix.upper()
            if suffix == 'B':
                child = Junk(size, self._chunkSize)
            elif suffix == 'KB':
                child = Junk(size * 1024, self._chunkSize)
            elif suffix == 'MB':
                child = Junk(size * 1024 * 1024, self._chunkSize)
            else:
                child = Resource.getChild(self, name, request)

        return child


class Junk(Resource):
    isLeaf = True

    def __init__(self, size, chunkSize=CHUNK_SIZE):
        Resource.__init__(self)
        self.size = size
        self.chunkSize = int(chunkSize or self.chunkSize)

    def render_GET(self, request):
        log.debug('%r rendering %d bytes for %r' % (self, self.size, request))
        request.setHeader('Content-length', self.size)
        self._writeJunk(request)
        return NOT_DONE_YET

    @inlineCallbacks
    def _writeJunk(self, request):
        writtenSize = 0
        while writtenSize != self.size:
            if writtenSize + self.chunkSize > self.size:
                writeSize = self.size - writtenSize
            else:
                writeSize = self.chunkSize
            log.debug('%r writing %d bytes for %r' % (self, writeSize, request))
            yield self._writeJunkChunk(request, writeSize)
            writtenSize += writeSize

        assert writtenSize == self.size
        log.debug('%r wrote %d bytes for %r' % (self, writtenSize, request))
        request.finish()

    def _writeJunkChunk(self, request, chunkSize):

        def randString(n):
            base = int(math.ceil(0.75 * n))
            junk = os.urandom(base)
            return b64encode(junk, '-_')[:n]

        chunk = randString(chunkSize)
        assert len(chunk) == chunkSize

        def _write(data, d):
            request.write(data)
            d.callback(True)

        d = Deferred()
        reactor.callLater(0, _write, chunk, d)
        return d