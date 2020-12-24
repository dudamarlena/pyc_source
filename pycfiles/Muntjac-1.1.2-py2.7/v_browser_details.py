# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/client/v_browser_details.py
# Compiled at: 2013-04-04 15:36:36
"""Defines a class that parses the user agent string from the browser and
provides information about the browser."""
import re

class VBrowserDetails(object):
    """Class that parses the user agent string from the browser and provides
    information about the browser. Used internally by L{BrowserInfo} and
    L{WebBrowser}. Should not be used directly.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, userAgent):
        """Create an instance based on the given user agent.

        @param userAgent:
                   User agent as provided by the browser.
        """
        self._isGecko = False
        self._isWebKit = False
        self._isPresto = False
        self._isSafari = False
        self._isChrome = False
        self._isFirefox = False
        self._isOpera = False
        self._isIE = False
        self._isWindows = False
        self._isMacOSX = False
        self._isLinux = False
        self._browserEngineVersion = -1
        self._browserMajorVersion = -1
        self._browserMinorVersion = -1
        userAgent = userAgent.lower()
        self._isGecko = userAgent.find('gecko') != -1 and userAgent.find('webkit') == -1
        self._isWebKit = userAgent.find('applewebkit') != -1
        self._isPresto = userAgent.find(' presto/') != -1
        self._isChrome = userAgent.find(' chrome/') != -1
        self._isSafari = not self._isChrome and userAgent.find('safari') != -1
        self._isOpera = userAgent.find('opera') != -1
        self._isIE = userAgent.find('msie') != -1 and not self._isOpera and userAgent.find('webtv') == -1
        self._isFirefox = userAgent.find(' firefox/') != -1
        try:
            if self._isGecko:
                rvPos = userAgent.find('rv:')
                if rvPos >= 0:
                    tmp = userAgent[rvPos + 3:]
                    tmp = re.sub('(\\.[0-9]+).+', '\\1', tmp, count=1)
                    self._browserEngineVersion = float(tmp)
            elif self._isWebKit:
                tmp = userAgent[userAgent.find('webkit/') + 7:]
                tmp = re.sub('([0-9]+)[^0-9].+', '\\1', tmp, count=1)
                self._browserEngineVersion = float(tmp)
        except Exception:
            print 'Browser engine version parsing failed for: ' + userAgent

        try:
            if self._isIE:
                ieVersionString = userAgent[userAgent.find('msie ') + 5:]
                ieVersionString = self.safeSubstring(ieVersionString, 0, ieVersionString.find(';'))
                self.parseVersionString(ieVersionString)
            elif self._isFirefox:
                i = userAgent.find(' firefox/') + 9
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isChrome:
                i = userAgent.find(' chrome/') + 8
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isSafari:
                i = userAgent.find(' version/') + 9
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
            elif self._isOpera:
                i = userAgent.find(' version/')
                if i != -1:
                    i += 9
                else:
                    i = userAgent.find('opera/') + 6
                ver = self.safeSubstring(userAgent, i, i + 5)
                self.parseVersionString(ver)
        except Exception:
            print 'Browser version parsing failed for: ' + userAgent

        if 'windows ' in userAgent:
            self._isWindows = True
        elif 'linux' in userAgent:
            self._isLinux = True
        elif 'macintosh' in userAgent or 'mac osx' in userAgent or 'mac os x' in userAgent:
            self._isMacOSX = True

    def parseVersionString(self, versionString):
        idx = versionString.find('.')
        if idx < 0:
            idx = len(versionString)
        ver = self.safeSubstring(versionString, 0, idx)
        self._browserMajorVersion = int(ver)
        idx2 = versionString.find('.', idx + 1)
        if idx2 < 0:
            idx2 = len(versionString)
        try:
            ver = self.safeSubstring(versionString, idx + 1, idx2)
            self._browserMinorVersion = int(re.sub('[^0-9].*', '', ver))
        except ValueError:
            pass

    def safeSubstring(self, string, beginIndex, endIndex):
        if beginIndex < 0:
            beginIndex = 0
        if endIndex < 0 or endIndex > len(string):
            endIndex = len(string)
        return string[beginIndex:endIndex]

    def isFirefox(self):
        """Tests if the browser is Firefox.

        @return: true if it is Firefox, false otherwise
        """
        return self._isFirefox

    def isGecko(self):
        """Tests if the browser is using the Gecko engine

        @return: true if it is Gecko, false otherwise
        """
        return self._isGecko

    def isWebKit(self):
        """Tests if the browser is using the WebKit engine

        @return: true if it is WebKit, false otherwise
        """
        return self._isWebKit

    def isPresto(self):
        """Tests if the browser is using the Presto engine

        @return: true if it is Presto, false otherwise
        """
        return self._isPresto

    def isSafari(self):
        """Tests if the browser is Safari.

        @return: true if it is Safari, false otherwise
        """
        return self._isSafari

    def isChrome(self):
        """Tests if the browser is Chrome.

        @return: true if it is Chrome, false otherwise
        """
        return self._isChrome

    def isOpera(self):
        """Tests if the browser is Opera.

        @return: true if it is Opera, false otherwise
        """
        return self._isOpera

    def isIE(self):
        """Tests if the browser is Internet Explorer.

        @return: true if it is Internet Explorer, false otherwise
        """
        return self._isIE

    def getBrowserEngineVersion(self):
        """Returns the version of the browser engine. For WebKit this is
        an integer e.g., 532.0. For gecko it is a float e.g., 1.8 or 1.9.

        @return: The version of the browser engine
        """
        return self._browserEngineVersion

    def getBrowserMajorVersion(self):
        """Returns the browser major version e.g., 3 for Firefox 3.5, 4 for
        Chrome 4, 8 for Internet Explorer 8.

        Note that Internet Explorer 8 and newer will return the document
        mode so IE8 rendering as IE7 will return 7.

        @return: The major version of the browser.
        """
        return self._browserMajorVersion

    def getBrowserMinorVersion(self):
        """Returns the browser minor version e.g., 5 for Firefox 3.5.

        @see: #getBrowserMajorVersion()

        @return: The minor version of the browser, or -1 if not known/parsed.
        """
        return self._browserMinorVersion

    def setIEMode(self, documentMode):
        """Sets the version for IE based on the documentMode. This is used
        to return the correct the correct IE version when the version from
        the user agent string and the value of the documentMode property do
        not match.

        @param documentMode:
                   The current document mode
        """
        self._browserMajorVersion = documentMode
        self._browserMinorVersion = 0

    def isWindows(self):
        """Tests if the browser is run on Windows.

        @return: true if run on Windows, false otherwise
        """
        return self._isWindows

    def isMacOSX(self):
        """Tests if the browser is run on Mac OSX.

        @return: true if run on Mac OSX, false otherwise
        """
        return self._isMacOSX

    def isLinux(self):
        """Tests if the browser is run on Linux.

        @return: true if run on Linux, false otherwise
        """
        return self._isLinux