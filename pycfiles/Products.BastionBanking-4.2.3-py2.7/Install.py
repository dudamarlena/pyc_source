# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Extensions/Install.py
# Compiled at: 2015-07-18 19:38:10
from StringIO import StringIO
from Products.CMFPlone.utils import getFSVersionTuple
from Products.CMFCore.utils import getToolByName
from Products.BastionBanking.config import *

def install(portal):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.BastionBanking:default', purge_old=False)
    out.write('registered skins and types and workflows')
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.BastionBanking:default')
    return 'Successfully uninstalled %s' % PROJECTNAME