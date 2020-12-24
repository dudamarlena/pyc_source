# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/core/config.py
# Compiled at: 2008-10-06 10:31:14
try:
    import Products.CMFPlone.migrations.v3_0
    HAS_PLONE3 = True
except ImportError:
    HAS_PLONE3 = False

import iccommunity.core
PACKAGE = iccommunity.core
PROJECTNAME = 'iccommunity.core'
PACKAGENAME = 'iccommunity.core'
DEPENDENCIES = []
from Products.CMFCore.permissions import SetOwnProperties
CONFIGLETS = ()
GLOBALS = globals()