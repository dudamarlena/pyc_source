# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/abstract_streaming_event.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.terminal.stream_variable import IStreamingEvent

class AbstractStreamingEvent(IStreamingEvent):
    """Abstract base class for IStreamingEvent implementations."""

    def __init__(self, filename, typ, length, bytesReceived):
        self._filename = filename
        self._type = typ
        self._contentLength = length
        self._bytesReceived = bytesReceived

    def getFileName(self):
        return self._filename

    def getMimeType(self):
        return self._type

    def getContentLength(self):
        return self._contentLength

    def getBytesReceived(self):
        return self._bytesReceived