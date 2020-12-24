# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/upload/ImmediateUploadExample.py
# Compiled at: 2013-04-04 15:36:38
import time
from StringIO import StringIO
from muntjac.api import VerticalLayout, Label, ProgressIndicator, HorizontalLayout, Upload, Alignment, Button
from muntjac.ui import button, upload

class ImmediateUploadExample(VerticalLayout):

    def __init__(self):
        super(ImmediateUploadExample, self).__init__()
        self.setSpacing(True)
        self._status = Label('Please select a file to upload')
        self._pi = ProgressIndicator()
        self._receiver = MyReceiver()
        self._progressLayout = HorizontalLayout()
        self._upload = Upload(None, self._receiver)
        self._receiver.setSlow(True)
        self.addComponent(self._status)
        self.addComponent(self._upload)
        self.addComponent(self._progressLayout)
        self._upload.setImmediate(True)
        self._upload.setButtonCaption('Select file')
        self._progressLayout.setSpacing(True)
        self._progressLayout.setVisible(False)
        self._progressLayout.addComponent(self._pi)
        self._progressLayout.setComponentAlignment(self._pi, Alignment.MIDDLE_LEFT)
        cancelProcessing = Button('Cancel')
        cancelProcessing.addListener(CancelListener(self), button.IClickListener)
        cancelProcessing.setStyleName('small')
        self._progressLayout.addComponent(cancelProcessing)
        self._upload.addListener(StartedListener(self), upload.IStartedListener)
        self._upload.addListener(ProgressListener(self), upload.IProgressListener)
        self._upload.addListener(SucceededListener(self), upload.ISucceededListener)
        self._upload.addListener(FailedListener(self), upload.IFailedListener)
        self._upload.addListener(FinishedListener(self), upload.IFinishedListener)
        return


class CancelListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._upload.interruptUpload()


class StartedListener(upload.IStartedListener):

    def __init__(self, c):
        self._c = c

    def uploadStarted(self, event):
        self._c._upload.setVisible(False)
        self._c._progressLayout.setVisible(True)
        self._c._pi.setValue(0.0)
        self._c._pi.setPollingInterval(500)
        self._c._status.setValue('Uploading file "' + event.getFilename() + '"')


class ProgressListener(upload.IProgressListener):

    def __init__(self, c):
        self._c = c

    def updateProgress(self, readBytes, contentLength):
        self._c._pi.setValue(float(readBytes / contentLength))


class SucceededListener(upload.ISucceededListener):

    def __init__(self, c):
        self._c = c

    def uploadSucceeded(self, event):
        self._c._status.setValue('Uploading file "' + event.getFilename() + '" succeeded')


class FailedListener(upload.IFailedListener):

    def __init__(self, c):
        self._c = c

    def uploadFailed(self, event):
        self._c._status.setValue('Uploading interrupted')


class FinishedListener(upload.IFinishedListener):

    def __init__(self, c):
        self._c = c

    def uploadFinished(self, event):
        self._c._progressLayout.setVisible(False)
        self._c._upload.setVisible(True)
        self._c._upload.setCaption('Select another file')


class MyReceiver(upload.IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._sleep = None
        self._total = 0
        return

    def receiveUpload(self, filename, mimetype):
        self._fileName = filename
        self._mtype = mimetype
        return UploadStream(self)

    def getFileName(self):
        return self._fileName

    def getMimeType(self):
        return self._mtype

    def setSlow(self, value):
        self._sleep = value


class UploadStream(StringIO):

    def __init__(self, r):
        super(UploadStream, self).__init__()
        self._r = r

    def write(self, b):
        self._r._total += 1
        if self._r._sleep and self._r._total % 10000 == 0:
            time.sleep(100)