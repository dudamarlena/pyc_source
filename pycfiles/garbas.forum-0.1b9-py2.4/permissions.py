# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/permissions.py
# Compiled at: 2008-09-26 00:35:00
from Products.CMFCore.permissions import setDefaultRoles
SubmitNewPost = 'Forum: Submit New Post'

def initialize_permissions():
    setDefaultRoles(SubmitNewPost, ['Manager'])