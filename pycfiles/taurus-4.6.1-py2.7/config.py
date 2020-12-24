# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/taurusgui/conf/tgconf_macrogui/config.py
# Compiled at: 2019-08-19 15:09:30
"""
configuration file for an example of how to construct a GUI based on TaurusGUI

This configuration file determines the default, permanent, pre-defined
contents of the GUI. While the user may add/remove more elements at run
time and those customizations will also be stored, this file defines what a
user will find when launching the GUI for the first time.
"""
from taurus.qt.qtgui.taurusgui.utils import PanelDescription, ExternalApp, Qt_Qt
GUI_NAME = 'MacroGUI'
ORGANIZATION = 'Taurus'
pymca = ExternalApp(['pymca'])
MACROSERVER_NAME = ''
DOOR_NAME = ''
MACROEDITORS_PATH = ''
CONSOLE = [
 'tango']