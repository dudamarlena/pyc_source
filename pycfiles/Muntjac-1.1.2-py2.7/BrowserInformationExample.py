# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/BrowserInformationExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label

class BrowserInformationExample(VerticalLayout):

    def __init__(self):
        super(BrowserInformationExample, self).__init__()
        self._populated = False

    def attach(self):
        if self._populated:
            return
        context = self.getApplication().getContext()
        webBrowser = context.getBrowser()
        browserText = self.getBrowserAndVersion(webBrowser)
        browserText = browserText + ' in ' + self.getOperatingSystem(webBrowser)
        ipAddresslabel = Label('Hello user from <b>' + webBrowser.getAddress() + '</b>.', Label.CONTENT_XHTML)
        browser = Label('You are running <b>' + browserText + '</b>.', Label.CONTENT_XHTML)
        screenSize = Label('Your screen resolution is <b>' + str(webBrowser.getScreenWidth()) + 'x' + str(webBrowser.getScreenHeight()) + '</b>.', Label.CONTENT_XHTML)
        locale = Label('Your browser is set to primarily use the <b>' + str(webBrowser.getLocale()) + '</b> locale.', Label.CONTENT_XHTML)
        self.addComponent(ipAddresslabel)
        self.addComponent(browser)
        self.addComponent(screenSize)
        self.addComponent(locale)
        self._populated = True

    def getTimeZoneInfoString(self, webBrowser):
        tzOffset = webBrowser.getTimezoneOffset()
        infoStr = 'Your browser indicates GMT%s%d' % (
         '-' if tzOffset < 0 else '+', abs(self.tzoToHours(tzOffset)))
        if webBrowser.isDSTInEffect():
            infoStr += ' and DST %d' % self.tzoToHours(webBrowser.getDSTSavings())
        return infoStr + ', which could mean:'

    @classmethod
    def tzoToHours(cls, ms):
        return ms / 1000 / 60 / 60

    def getOperatingSystem(self, webBrowser):
        if webBrowser.isWindows():
            return 'Windows'
        else:
            if webBrowser.isMacOSX():
                return 'Mac OSX'
            if webBrowser.isLinux():
                return 'Linux'
            return 'an unknown operating system'

    def getBrowserAndVersion(self, webBrowser):
        if webBrowser.isChrome():
            return 'Chrome ' + str(webBrowser.getBrowserMajorVersion()) + '.' + str(webBrowser.getBrowserMinorVersion())
        else:
            if webBrowser.isOpera():
                return 'Opera ' + str(webBrowser.getBrowserMajorVersion()) + '.' + str(webBrowser.getBrowserMinorVersion())
            if webBrowser.isFirefox():
                return 'Firefox ' + str(webBrowser.getBrowserMajorVersion()) + '.' + str(webBrowser.getBrowserMinorVersion())
            if webBrowser.isSafari():
                return 'Safari ' + str(webBrowser.getBrowserMajorVersion()) + '.' + str(webBrowser.getBrowserMinorVersion())
            if webBrowser.isIE():
                return 'Internet Explorer ' + str(webBrowser.getBrowserMajorVersion())
            return 'an unknown browser'