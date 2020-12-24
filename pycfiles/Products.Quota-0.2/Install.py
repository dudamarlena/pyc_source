# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\Extensions\Install.py
# Compiled at: 2008-06-04 06:25:00
from StringIO import StringIO
import transaction
from Products.CMFCore.utils import getToolByName
from Products.MetaWeblogPASPlugin import config

def install(self):
    """Install QuillsRemoteBlogging
    """
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    print >> out, 'Installing dependency %s:' % config.PROJECTNAME
    quickinstaller.installProduct(config.PROJECTNAME)
    transaction.savepoint()
    print >> out, 'Successfully installed %s.' % config.PROJECTNAME
    return out.getvalue()