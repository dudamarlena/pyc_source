# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/details/error/error.py
# Compiled at: 2010-08-27 06:32:04
from zope.component import getUtility
from zope.publisher.browser import BrowserView
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.error.interfaces import IErrorReportingUtility
from zope.error.interfaces import ILocalErrorReportingUtility

class EditErrorLog(object):

    def updateProperties(self, keep_entries, copy_to_zlog=None, ignored_exceptions=None):
        errorLog = self.context
        if copy_to_zlog is None:
            copy_to_zlog = 0
        errorLog.setProperties(keep_entries, copy_to_zlog, ignored_exceptions)
        return self.request.response.redirect('@@getControlDetailsConfigure')