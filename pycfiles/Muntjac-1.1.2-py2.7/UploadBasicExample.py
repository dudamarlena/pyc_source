# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/upload/UploadBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from StringIO import StringIO
from muntjac.api import VerticalLayout, Label
from muntjac.ui.upload import Upload, IReceiver, IFinishedListener

class UploadBasicExample(VerticalLayout):

    def __init__(self):
        super(UploadBasicExample, self).__init__()
        self._result = Label()
        self._counter = LineBreakCounter()
        self._upload = Upload('Upload a file', self._counter)
        self.addComponent(self._upload)
        self.addComponent(self._result)
        self._upload.addListener(FinishedListener(self), IFinishedListener)


class FinishedListener(IFinishedListener):

    def __init__(self, c):
        self._c = c

    def uploadFinished(self, event):
        self._c._result.setValue('Uploaded file contained ' + self._c._counter.getLineBreakCount() + ' linebreaks')


class LineBreakCounter(IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._counter = None
        return

    def receiveUpload(self, filename, MIMEType):
        """return an OutputStream that simply counts line ends"""
        self._counter = 0
        self._fileName = filename
        self._mtype = MIMEType
        return OutputStream(self)

    def getFileName(self):
        return self._fileName

    def getMimeType(self):
        return self._mtype

    def getLineBreakCount(self):
        return self._counter


class OutputStream(StringIO):

    def __init__(self, lbc):
        super(OutputStream, self).__init__()
        self._lbc = lbc

    def write(self, b):
        if b == '\n':
            self._lbc._counter += 1