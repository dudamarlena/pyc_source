# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/tauruscustomsettings.py
# Compiled at: 2019-08-19 15:09:30
"""
This module contains some Taurus-wide default configurations.

The idea is that the final user may edit the values here to customize certain
aspects of Taurus.
"""
T_FORM_CUSTOM_WIDGET_MAP = {'SimuMotor': ('sardana.taurus.qt.qtgui.extra_pool.PoolMotorTV', (), {}), 'Motor': (
           'sardana.taurus.qt.qtgui.extra_pool.PoolMotorTV', (), {}), 
   'PseudoMotor': (
                 'sardana.taurus.qt.qtgui.extra_pool.PoolMotorTV', (), {}), 
   'PseudoCounter': (
                   'sardana.taurus.qt.qtgui.extra_pool.PoolChannelTV', (), {}), 
   'CTExpChannel': (
                  'sardana.taurus.qt.qtgui.extra_pool.PoolChannelTV', (), {}), 
   'ZeroDExpChannel': (
                     'sardana.taurus.qt.qtgui.extra_pool.PoolChannelTV', (), {}), 
   'OneDExpChannel': (
                    'sardana.taurus.qt.qtgui.extra_pool.PoolChannelTV', (), {}), 
   'TwoDExpChannel': (
                    'sardana.taurus.qt.qtgui.extra_pool.PoolChannelTV', (), {}), 
   'IORegister': (
                'sardana.taurus.qt.qtgui.extra_pool.PoolIORegisterTV', (), {})}
T_FORM_COMPACT = False
STRICT_MODEL_NAMES = False
LIGHTWEIGHT_IMPORTS = False
DEFAULT_SCHEME = 'tango'
FILTER_OLD_TANGO_EVENTS = True
EXTRA_SCHEME_MODULES = []
TANGO_SERIALIZATION_MODE = 'TangoSerial'
PLY_OPTIMIZE = 1
NAMESPACE = 'taurus'
DEFAULT_QT_API = 'pyqt'
QT_AUTO_INIT_LOG = True
QT_AUTO_REMOVE_INPUTHOOK = True
QT_AVOID_ABORT_ON_EXCEPTION = True
QT_THEME_DIR = ''
QT_THEME_NAME = 'Tango'
QT_THEME_FORCE_ON_LINUX = True
QT_DESIGNER_PATH = None
ORGANIZATION_LOGO = 'logos:taurus.png'
_MAX_DEPRECATIONS_LOGGED = 1