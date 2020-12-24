# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/FinanceFields/Extensions/Install.py
# Compiled at: 2010-03-10 14:21:00
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.FinanceFields.config import PROJECTNAME, GLOBALS
from StringIO import StringIO

def install(self):
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    classes = listTypes(PROJECTNAME)
    installTypes(self, out, classes, PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.setImportContext('profile-FinanceFields:default')
    result = setup_tool.runImportStep('propertiestool')
    out.write('Steps run: %s \n' % (', ').join(result['steps']))
    out.write('Successfully installed %s.' % PROJECTNAME)
    return out.getvalue()