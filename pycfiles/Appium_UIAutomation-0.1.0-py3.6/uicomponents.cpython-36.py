# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/automation/mobile/uicomponents.py
# Compiled at: 2017-04-06 05:40:13
# Size of source mod 2**32: 1825 bytes
from enum import Enum
from collections import namedtuple

class UIComponents:
    Component = namedtuple('Component', ['iOS', 'Android'])
    LABEL = Component(iOS='//XCUIElementTypeStaticText[{}]', Android='//android.widget.TextView[{}]')
    BUTTON = Component(iOS='//XCUIElementTypeButton[{}]', Android='//android.widget.Button[{}]')
    TEXTFIELD = Component(iOS='//XCUIElementTypeTextField[{}]', Android='//android.widget.EditText[{}]')
    PWDFIELD = Component(iOS='//XCUIElementTypeSecureTextField[{}]', Android='//android.widget.EditText[{}]')
    LIST = Component(iOS='//XCUIElementTypeTable/*[{}]', Android='//android.widget.ListView/*[{}]')
    SWITCH = Component(iOS='//XCUIElementTypeSwitch[{}]', Android='TBD')
    SLIDER = Component(iOS='//XCUIElementTypeSlider[{}]', Android='TBD')
    ALERT = Component(iOS='//XCUIElementTypeAlert', Android="(//android.widget.LinearLayout | //android.widget.FrameLayout)[contains(@resource-id, 'id/parentPanel')]")