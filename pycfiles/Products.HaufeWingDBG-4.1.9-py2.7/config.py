# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/HaufeWingDBG/config.py
# Compiled at: 2012-12-06 03:42:07
"""WingDBG constants"""
import os
from Globals import package_home
from AccessControl.Permissions import view_management_screens, delete_objects
from AccessControl import ModuleSecurityInfo
security = ModuleSecurityInfo('Products.HaufeWingDBG.config')
GLOBALS = globals()
security.declarePublic('PACKAGE_NAME', 'CONTROL_PANEL_ID', 'ICON_NAME')
PACKAGE_NAME = 'HaufeWingDBG'
CONTROL_PANEL_ID = 'WingDebugService'
ICON_NAME = CONTROL_PANEL_ID
PRODUCT_DIR = package_home(GLOBALS)
WWW_DIR = os.path.join(PRODUCT_DIR, 'www')
DOC_DIR = os.path.join(PRODUCT_DIR, 'documentation')
security.declarePublic('VIEW_PERMISSION', 'CHANGE_PERMISSION', 'USE_PERMISSION', 'DEL_PERMISSION')
VIEW_PERMISSION = view_management_screens
CHANGE_PERMISSION = 'Wing Debug Service: Change Settings'
USE_PERMISSION = 'Wing Debug Service: Control Debugger'
DEL_PERMISSION = delete_objects
security.declarePublic('PW_MODE_PROFILE_DIR', 'PW_MODE_CUSTOM_DIR', 'PW_MODE_CUSTOM_PW', 'PW_ENC_TYPE_NONE', 'PW_ENC_TYPE_ROTOR')
PW_MODE_PROFILE_DIR, PW_MODE_CUSTOM_DIR, PW_MODE_CUSTOM_PW = range(3)
PW_ENC_TYPE_NONE, PW_ENC_TYPE_ROTOR = range(2)