# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/__init__.py
# Compiled at: 2013-01-07 13:37:03
from utilities import Base
from browser import Browser
from operating_system import OperatingSystem

class UserAgent(Base):

    def __init__(self, userAgentString):
        self.userAgentString = userAgentString
        self.browser = Browser.parseUserAgentString(userAgentString)
        self.operatingSystem = OperatingSystem.UNKNOWN
        if browser is not Browser.BOT:
            self.operatingSystem = OperatingSystem.parseUserAgentString(userAgentString)