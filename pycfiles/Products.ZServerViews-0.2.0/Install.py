# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/Extensions/Install.py
# Compiled at: 2015-07-18 19:40:58
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.ZScheduler.config import *

def install(portal):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.ZScheduler:default', purge_old=False)
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal, reinstall=False):
    out = StringIO()
    if not reinstall:
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.ZScheduler:default')
    print >> out, 'Successfully uninstalled %s.' % PROJECTNAME
    return out.getvalue()