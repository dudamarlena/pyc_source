# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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