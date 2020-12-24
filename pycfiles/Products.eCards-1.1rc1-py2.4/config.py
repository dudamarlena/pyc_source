# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/config.py
# Compiled at: 2008-11-11 20:26:20
PROJECTNAME = 'eCards'
GLOBALS = globals()
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
SKINS_DIR = 'skins'
ALLTYPES = ('eCard', 'eCardCollection')
ALLSKINS = ('ecards_images', 'ecards_templates', 'ecards_styles')
from Products.CMFCore import permissions as CMFCorePermissions
SendECard = 'eCards: Send eCard'
CMFCorePermissions.setDefaultRoles(SendECard, ['Manager', 'Anonymous'])