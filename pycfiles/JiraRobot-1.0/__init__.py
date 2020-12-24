# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: JiraRobot\__init__.py
# Compiled at: 2014-07-21 04:59:31
from JiraRobot import JiraRobot
from version import VERSION
_version_ = VERSION

class JiraRobot(JiraRobot):
    """
    Robot-AppEyes is a visual verfication library for Robot Framework that leverages
    the Eyes-Selenium and Selenium2 libraries.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'