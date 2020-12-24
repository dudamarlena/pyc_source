# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Debugger\DebugWriter.py
# Compiled at: 2006-02-13 22:04:25
from Ft.Xml import EMPTY_NAMESPACE

class DebugWriter:
    __module__ = __name__

    def __init__(self):
        self.reset()

    def reset(self):
        self.calls = []

    def getMediaType(self):
        return ''

    def getResult(self):
        return ''

    def getCurrent(self):
        rt = self.calls
        self.reset()
        return rt

    def __makeCall(self, name, args):
        self.calls.append((name, args))

    def __startCall(self, name, args):
        self.calls.append(('Start: ' + name, args))

    def __endCall(self, name):
        self.calls.append(('End: ' + name, {}))

    def startDocument(self):
        self.__startCall('document', ())
        return

    def endDocument(self):
        self.__endCall('document')
        return

    def text(self, text, escapeOutput=1):
        self.__makeCall('text', {'text': text})
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        self.__makeCall('attribute', {'name': name, 'value': value, 'namespace': namespace})
        return

    def processingInstruction(self, target, data):
        self.__makeCall('processingInstruction', {'target': target, 'data': data})
        return

    def comment(self, body):
        self.__makeCall('comment', {'body': body})
        return

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        self.__startCall('element', {'name': name, 'namespace': namespace})
        return

    def endElement(self, name):
        self.__endCall('element')
        return