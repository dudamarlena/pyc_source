# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/progressbar/demo/demo.py
# Compiled at: 2009-09-18 14:53:55
import time
from Products.Five import BrowserView
from zope.event import notify
from collective.progressbar.events import InitialiseProgressBar
from collective.progressbar.events import ProgressBar
from collective.progressbar.events import UpdateProgressEvent
from collective.progressbar.events import ProgressState

class DemoProgressBar(BrowserView):
    """ Demo progress bar
    """
    __module__ = __name__

    def __call__(self):
        bar = ProgressBar(self.context, self.request, 'Demo Progress Bar', 'Demo in progress ...')
        notify(InitialiseProgressBar(bar))
        for index in range(101):
            progress = ProgressState(self.request, index)
            notify(UpdateProgressEvent(progress))
            time.sleep(1)