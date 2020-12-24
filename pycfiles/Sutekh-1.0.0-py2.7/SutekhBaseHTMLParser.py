# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/SutekhBaseHTMLParser.py
# Compiled at: 2019-12-11 16:37:52
"""Common base classes for the different HTML Parsers"""
import HTMLParser
from logging import Logger

class StateError(Exception):
    """Error case in the state"""
    pass


class HTMLStateError(StateError):
    """Exception with more info for HTML State transition errors"""

    def __init__(self, sInfo, sData, sTag):
        super(HTMLStateError, self).__init__()
        self._sInfo = sInfo
        self._sData = sData
        self._sTag = sTag

    def __str__(self):
        return 'HTML Parser State Error : %s\nsData : %s\nTag : %s' % (
         self._sInfo, self._sData, self._sTag)


class BaseState(object):
    """Base class for parser states"""

    def __init__(self):
        super(BaseState, self).__init__()
        self._sData = ''

    def transition(self, sTag, dAttr):
        """Transition from one state to another"""
        raise NotImplementedError

    def data(self, sData):
        """Add data to the state"""
        self._sData += sData


class LogState(BaseState):
    """Base class for the State transitions with a log handler"""

    def __init__(self, oLogger):
        super(LogState, self).__init__()
        self._oLogger = oLogger


class LogStateWithInfo(LogState):
    """Base class for states which contain information of interest"""

    def __init__(self, dInfo, oLogger):
        super(LogStateWithInfo, self).__init__(oLogger)
        self._dInfo = dInfo


class HolderState(BaseState):
    """Base class for parser states"""

    def __init__(self, oHolder):
        super(HolderState, self).__init__()
        self._oHolder = oHolder


class SutekhBaseHTMLParser(HTMLParser.HTMLParser, object):
    """Base Parser for the Sutekh HTML parsers"""

    def __init__(self):
        """Create an SutekhBaseHTMLParser."""
        self._oState = BaseState()
        super(SutekhBaseHTMLParser, self).__init__()

    def reset(self):
        """Reset the parser"""
        super(SutekhBaseHTMLParser, self).reset()
        self._oState = BaseState()

    def handle_starttag(self, sTag, aAttr):
        self._oState = self._oState.transition(sTag.lower(), dict(aAttr))

    def handle_endtag(self, sTag):
        self._oState = self._oState.transition('/' + sTag.lower(), {})

    def handle_data(self, sData):
        self._oState.data(sData)

    def handle_charref(self, sName):
        pass

    def handle_entityref(self, sName):
        pass

    def parse(self, fOpenFile):
        """Wrapper around feed to provide a consistent interface with
           other parsers."""
        for sLine in fOpenFile:
            self.feed(sLine)


class LoggingHTMLParser(SutekhBaseHTMLParser):
    """HTML Parser that sets up appropriate logging logic."""
    sLogName = 'Base html parser'

    def __init__(self, oLogHandler):
        self._oLogger = Logger(self.sLogName)
        if oLogHandler is not None:
            self._oLogger.addHandler(oLogHandler)
        super(LoggingHTMLParser, self).__init__()
        return