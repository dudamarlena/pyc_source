# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/permissions.py
# Compiled at: 2008-12-16 18:21:21
import config
from Products.CMFCore.permissions import setDefaultRoles
from AccessControl import ModuleSecurityInfo
security = ModuleSecurityInfo(config.PROJECTNAME)
security.declarePublic('SynchronizeContent')
SynchronizeContent = '%s: Synchronize Content' % config.PROJECTNAME
setDefaultRoles(SynchronizeContent, 'Manager')