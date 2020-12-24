# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/user/browser/namespace.py
# Compiled at: 2013-04-19 10:05:32
from ztfy.sendit.user.interfaces import ISenditApplicationUsers
from zope.traversing import namespace

class SenditApplicationUsersNamespace(namespace.view):
    """++users++ namespace traverser"""

    def traverse(self, name, ignored):
        return ISenditApplicationUsers(self.context)