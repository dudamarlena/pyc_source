# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/streaming_events.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.terminal.stream_variable import IStreamingEndEvent, IStreamingErrorEvent, IStreamingProgressEvent, IStreamingStartEvent
from muntjac.terminal.gwt.server.abstract_streaming_event import AbstractStreamingEvent

class StreamingEndEventImpl(AbstractStreamingEvent, IStreamingEndEvent):

    def __init__(self, filename, typ, totalBytes):
        super(StreamingEndEventImpl, self).__init__(filename, typ, totalBytes, totalBytes)


class StreamingErrorEventImpl(AbstractStreamingEvent, IStreamingErrorEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived, exception):
        super(StreamingErrorEventImpl, self).__init__(filename, typ, contentLength, bytesReceived)
        self._exception = exception

    def getException(self):
        return self._exception


class StreamingProgressEventImpl(AbstractStreamingEvent, IStreamingProgressEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived):
        super(StreamingProgressEventImpl, self).__init__(filename, typ, contentLength, bytesReceived)


class StreamingStartEventImpl(AbstractStreamingEvent, IStreamingStartEvent):

    def __init__(self, filename, typ, contentLength):
        super(StreamingStartEventImpl, self).__init__(filename, typ, contentLength, 0)
        self._disposed = None
        return

    def disposeStreamVariable(self):
        self._disposed = True

    def isDisposed(self):
        return self._disposed