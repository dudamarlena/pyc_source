# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/upload_listeners.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.component.abstract_listener_methods_test import AbstractListenerMethodsTest
from muntjac.ui.upload import Upload, IProgressListener, SucceededEvent, ISucceededListener, StartedEvent, IStartedListener, FailedEvent, IFailedListener, FinishedEvent, IFinishedListener
from muntjac.terminal.stream_variable import IStreamingProgressEvent

class UploadListeners(AbstractListenerMethodsTest):

    def testProgressListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, IStreamingProgressEvent, IProgressListener)

    def testSucceededListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, SucceededEvent, ISucceededListener)

    def testStartedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, StartedEvent, IStartedListener)

    def testFailedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FailedEvent, IFailedListener)

    def testFinishedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FinishedEvent, IFinishedListener)