# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\QuillsEnabledRemoteBlogging\Extensions\Install.py
# Compiled at: 2008-04-09 20:30:16
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