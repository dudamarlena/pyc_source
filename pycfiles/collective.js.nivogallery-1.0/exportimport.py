# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/js/multizoom/exportimport.py
# Compiled at: 2015-12-02 03:46:28
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple

def install(context):
    site = context.getSite()
    if not context.readDataFile('collective.js.multizoom.txt'):
        return
    setup = getToolByName(site, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        setup.runAllImportStepsFromProfile('profile-collective.js.multizoom:plone4')
    else:
        setup.runAllImportStepsFromProfile('profile-collective.js.multizoom:plone5')