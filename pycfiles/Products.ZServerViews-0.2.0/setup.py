# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/browser/setup.py
# Compiled at: 2015-07-18 19:40:58
from Acquisition import aq_base, aq_inner
from Products.Five.browser import BrowserView
from Products.ZScheduler.ZScheduler import ZScheduler

class ZSchedulerTool(BrowserView):
    """
    Creates a Zenoss installation
    """

    def createTool(self):
        """
        creates zport, DMD in install root
        """
        context = aq_inner(self.context)
        context._setObject('ZSchedulerTool', ZScheduler())
        self.request.set('manage_tabs_message', 'created ZSchedulerTool')
        self.request.RESPONSE.redirect('/manage_main')