# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/zif/gzipper/gzipper.py
# Compiled at: 2007-04-13 18:17:15
"""
WSGI middleware

Gzip-encodes the response.
"""
import time, struct, zlib, tempfile
from queues import TemporaryFileQueue, StringQueue

class GZStreamIter(object):
    __module__ = __name__

    def __init__(self, data, compressLevel=6, write=65536, read=65536, tempFileTrigger=1048576):
        self.writeBufferSize = write
        self.readBufferSize = read
        self.tempFileTrigger = tempFileTrigger
        self.inputIsNotIterator = False
        if isinstance(data, tuple) or isinstance(data, list):
            data = iter(data)
            self.inputIsNotIterator = True
        elif isinstance(data, basestring):
            data = iter([data])
            self.inputIsNotIterator = True
        self.data = data
        self.queue = StringQueue()
        self.usingTempFile = False
        self.allReceived = False
        self.initFile()
        self.crc = zlib.crc32('')
        self.size = 0
        self.compressor = zlib.compressobj(compressLevel, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
        self.compress = self.compressor.compress
        self.crc32 = zlib.crc32
        self.getData()

    def __len__(self):
        return self.size

    def getLength(self):
        return self.size

    def close(self):
        self.queue.__init__()

    def __iter__(self):
        return self

    def initFile(self):
        self.queue.write(b'\x1f\x8b\x08\x00')
        self.queue.write(struct.pack('<L', long(time.time())))
        self.queue.write(b'\x02\xff')

    def getData(self):
        while len(self.queue) < self.readBufferSize and not self.allReceived:
            self.getIter()

    def getIter(self):
        try:
            s = self.data.next()
            self.queue.write(self.compress(s))
            self.size += len(s)
            self.crc = self.crc32(s, self.crc)
            if self.tempFileTrigger:
                if self.size > self.tempFileTrigger and not self.usingTempFile:
                    tmp = TemporaryFileQueue()
                    tmp.write(self.queue.read(None))
                    self.queue.close()
                    self.queue = tmp
                    self.usingTempFile = True
        except (StopIteration, ValueError):
            self.endFile()
            self.allReceived = True
            if hasattr(self.data, 'close'):
                self.data.close()
            self.data = None

        return

    def endFile(self):
        self.queue.write(self.compressor.flush())
        self.queue.write(struct.pack('<LL', self.crc & 4294967295, self.size & 4294967295))

    def next(self):
        if self.usingTempFile and self.inputIsNotIterator:
            while not self.allReceived:
                self.getIter()

        queueLen = len(self.queue)
        if queueLen == 0 and self.allReceived:
            self.queue.close()
            raise StopIteration
        dataGetSize = min(queueLen, self.writeBufferSize)
        s = self.queue.read(dataGetSize)
        if s == '' and self.allReceived:
            s = self.queue.read(None)
        if not self.allReceived:
            self.getData()
        return s

    length = property(getLength)


class middleware(object):
    __module__ = __name__

    def __init__(self, application, compress_level=6, nocompress='', tempfile='1048576', exclude=''):
        self.application = application
        self.compress_level = int(compress_level)
        self.nocompress = nocompress.split()
        self.tempFile = int(tempfile)
        self.excludes = exclude.split()

    def __call__(self, environ, start_response):
        doNothing = False
        if 'gzip' not in environ.get('HTTP_ACCEPT_ENCODING', ''):
            doNothing = True
        myGet = environ.get('PATH_INFO')
        for filename in self.excludes:
            if filename in myGet:
                doNothing = True

        if doNothing:
            return self.application(environ, start_response)
        response = GzipResponse(start_response, self.compress_level, self.nocompress, tempFileTrigger=self.tempFile)
        app_iter = self.application(environ, response.initial_decisions)
        if response.doProcessing:
            app_iter = response.finish_response(app_iter)
        return app_iter


class GzipResponse(object):
    __module__ = __name__

    def __init__(self, start_response, compress_level, nocompress=[], tempFileTrigger=1048576):
        self.start_response = start_response
        self.doProcessing = False
        self.compress_level = compress_level
        self.nocompress = nocompress
        self.tempFileTrigger = tempFileTrigger

    def initial_decisions(self, status, headers, exc_info=None):
        ct = None
        ce = None
        for (name, value) in headers:
            name = name.lower()
            if name == 'content-type':
                ct = value
            elif name == 'content-encoding':
                ce = value

        self.doProcessing = False
        if ct:
            self.doProcessing = True
            for k in self.nocompress:
                if k in ct:
                    self.doProcessing = False and self.doProcessing

        if ce:
            self.doProcessing = False
        if self.doProcessing:
            d = None
            headers.append(('content-encoding', 'gzip'))
            headers = [ (name, value) for (name, value) in headers if name.lower() != 'content-length' ]
        return self.start_response(status, headers, exc_info)

    def finish_response(self, app_iter):
        if app_iter:
            try:
                output = GZStreamIter(app_iter, self.compress_level, tempFileTrigger=self.tempFileTrigger)
            finally:
                try:
                    app_iter.close()
                except AttributeError:
                    pass

                if hasattr(app_iter, '__len__') and len(app_iter) == 1:
                    s = ('').join([ x for x in output ])
                    return (s,)
                return output
        else:
            return app_iter


def filter_factory(global_conf, compress_level='6', nocompress='', tempfile='1048576', exclude=''):

    def filter(application):
        return middleware(application, compress_level, nocompress, tempfile, exclude)

    return filter