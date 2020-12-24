# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/red5/protectedvod/permissions.py
# Compiled at: 2009-08-19 12:31:49
from AccessControl import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
security = ModuleSecurityInfo('unimr.red5.protectedvod.permissions')
security.declarePublic('DownloadRed5Stream')
DownloadRed5Stream = 'Download Red5Stream'
setDefaultRoles(DownloadRed5Stream, ('Owner', 'Manager'))