# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/Extensions/Install.py
# Compiled at: 2011-09-28 02:31:46
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple
from Products.Zpydoc.config import *

def install(portal):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    if getFSVersionTuple()[0] >= 3:
        setup_tool.runAllImportStepsFromProfile('profile-Zpydoc:default', purge_old=False)
    else:
        plone_base_profileid = 'profile-CMFPlone:plone'
        setup_tool.setImportContext(plone_base_profileid)
        setup_tool.setImportContext('profile-Zpydoc:default')
        setup_tool.runAllImportSteps(purge_old=False)
        setup_tool.setImportContext(plone_base_profileid)
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal, reinstall=False):
    out = StringIO()
    if not reinstall:
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Zpydoc:default')
    print >> out, 'Successfully uninstalled %s.' % PROJECTNAME
    return out.getvalue()