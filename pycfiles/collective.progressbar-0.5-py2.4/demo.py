# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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