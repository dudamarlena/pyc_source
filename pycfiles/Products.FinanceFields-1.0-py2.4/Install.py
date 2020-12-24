# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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