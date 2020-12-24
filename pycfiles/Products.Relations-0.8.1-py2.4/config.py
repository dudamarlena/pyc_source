# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/config.py
# Compiled at: 2008-09-11 19:48:09
from Products.CMFCore.permissions import AddPortalContent, ManagePortal
from Products.Archetypes import config as ATconfig
ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'Relations'
SKINS_DIR = 'skins'
GLOBALS = globals()
DEPS = ('Archetypes', )
UID_CATALOG = ATconfig.UID_CATALOG
REFERENCE_CATALOG = ATconfig.REFERENCE_CATALOG
IMPORT_TRANSACTION_STEPPING = 15
RELATIONS_LIBRARY = 'relations_library'
RELATIONSHIP_LIBRARY = 'Relations.library'
RELATIONSHIP_RULESETTOREF = 'Relations.rulesettoref'
RELATIONSHIP_CONTENTREF = 'Relations.contentref'
INSTALL_TEST_TYPES = 0
ALLOW_MULTIPLE_REFS_PER_TRIPLE = 0
CONFIGLETS = ({'id': RELATIONS_LIBRARY, 'name': 'Relations: Library', 'action': 'string:${portal_url}/%s/' % RELATIONS_LIBRARY, 'category': 'Products', 'permission': ManagePortal, 'imageUrl': 'book_icon.gif', 'appId': 'Products.Relations'},)