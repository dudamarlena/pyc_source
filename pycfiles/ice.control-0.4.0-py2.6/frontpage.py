# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/skin/frontpage/frontpage.py
# Compiled at: 2010-08-27 06:32:04
from zope.security import checkPermission
from zope.authentication.interfaces import IUnauthenticatedPrincipal

class Pagelet:

    def update(self):
        self.unauth = IUnauthenticatedPrincipal.providedBy(self.request.principal)
        self.is_allow = checkPermission('ice.control.View', self.context)