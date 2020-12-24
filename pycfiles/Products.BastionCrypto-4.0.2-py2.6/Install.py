# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/Extensions/Install.py
# Compiled at: 2012-03-06 02:26:51
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BastionCrypto.config import *

def install(portal):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.BastionCrypto:default', purge_old=False)
    out.write('registered skins and types and workflows')
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal, reinstall=False):
    out = StringIO()
    if not reinstall:
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.BastionCrypto:default')
    print >> out, 'Successfully uninstalled %s.' % PROJECTNAME
    return out.getvalue()