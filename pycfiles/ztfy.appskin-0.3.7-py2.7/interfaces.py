# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/appskin/viewlets/usernav/interfaces.py
# Compiled at: 2013-04-23 02:36:24
from zope.viewlet.interfaces import IViewletManager, IViewlet

class IUserNavigationViewletManager(IViewletManager):
    """User navigation viewlet manager interface"""
    pass


class IUserNavigationMenu(IViewlet):
    """User navigation menu"""
    pass