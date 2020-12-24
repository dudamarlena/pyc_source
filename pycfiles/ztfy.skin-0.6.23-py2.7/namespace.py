# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/namespace.py
# Compiled at: 2013-02-12 17:38:05
__docformat__ = 'restructuredtext'
from ztfy.skin.interfaces import ICustomBackOfficeInfoTarget
from zope.component import queryAdapter
from zope.traversing import namespace
from ztfy.utils.traversing import getParent

class CustomBackOfficeInfoNamespace(namespace.view):
    """++back++ namespace traverser"""

    def traverse(self, name, ignored):
        target = getParent(self.context, ICustomBackOfficeInfoTarget)
        if target is not None:
            return queryAdapter(target, target.back_interface)
        else:
            return