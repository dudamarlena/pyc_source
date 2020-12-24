# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/GoogleAnalytics.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.abstract_component import AbstractComponent

class GoogleAnalytics(AbstractComponent):
    CLIENT_WIDGET = None

    def __init__(self, trackerId, domainName=None):
        super(GoogleAnalytics, self).__init__()
        self._trackerId = trackerId
        self._pageId = None
        self._domainName = domainName
        return

    def getTrackerId(self):
        return self._trackerId

    def getDomainName(self):
        return self._domainName

    def trackPageview(self, pageId):
        self._pageId = pageId
        self.requestRepaint()

    def paintContent(self, target):
        super(GoogleAnalytics, self).paintContent(target)
        target.addAttribute('trackerid', self._trackerId)
        if self._pageId is not None:
            target.addAttribute('pageid', self._pageId)
        if self._domainName is not None:
            target.addAttribute('domain', self._domainName)
        return