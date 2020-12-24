# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/Extensions/Install.py
# Compiled at: 2010-12-06 09:11:59
from Products.CMFCore.utils import getToolByName

def uninstall(portal):
    catalog_tool = getToolByName(portal, 'portal_catalog')
    catalog_tool._delObject('bigram_lexicon')
    index_ids = ('Title', 'Description', 'SearchableText')
    for idx_id in index_ids:
        catalog_tool.delIndex(idx_id)

    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.BigramSplitter:remove')
    return 'Ran all uninstall steps.'