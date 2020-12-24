# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/browser_type.py
# Compiled at: 2012-12-17 16:58:03
from utilities import Enum, EnumValue

class BrowserType(Enum):

    def __init__(self, name):
        self.name = name

    WEB_BROWSER = EnumValue('Browser')
    MOBILE_BROWSER = EnumValue('Browser (mobile)')
    TEXT_BROWSER = EnumValue('Browser (text only)')
    EMAIL_CLIENT = EnumValue('Email Client')
    ROBOT = EnumValue('Robot')
    TOOL = EnumValue('Downloading tool')
    UNKNOWN = EnumValue('unknown')