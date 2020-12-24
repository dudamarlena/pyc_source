# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/Extensions/Install.py
# Compiled at: 2011-01-11 16:22:56
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.BastionZenoss.config import *

def install(portal):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-BastionZenoss:default', purge_old=False)
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def uninstall(portal, reinstall=False):
    out = StringIO()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-BastionZenoss:default')
    setup_tool.runAllImportSteps()
    try:
        setup_tool.setImportContext('profile-CMFPlone:plone')
    except:
        pass

    return 'Ran all uninstall steps.'


if __name__ == '__main__':
    print 'brilliant - it compiles ...'