# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/beyondskins/pyconbrasil2008/Extensions/Install.py
# Compiled at: 2008-07-25 10:39:38
from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    originalContext = setup_tool.getImportContextID()
    setup_tool.setImportContext('profile-beyondskins.pyconbrasil2008:default')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext(originalContext)
    return 'Ran all import steps.'