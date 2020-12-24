# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/bootstrap/blog/skin/viewlets/header/login.py
# Compiled at: 2013-03-05 17:26:14
__docformat__ = 'restructuredtext'
import copy
from zope.publisher.interfaces.browser import IBrowserSkinType
from ztfy.skin.interfaces import IDefaultView
from zope.component import queryUtility, queryMultiAdapter
from zope.publisher.browser import applySkin
from ztfy.skin.viewlet import ViewletBase

class LoginViewlet(ViewletBase):

    @property
    def manage_url(self):
        skin = queryUtility(IBrowserSkinType, 'ZTFY.BO')
        if skin is not None:
            fake = copy.copy(self.request)
            applySkin(fake, skin)
        else:
            fake = self.request
        adapter = queryMultiAdapter((self.context, fake, self.__parent__), IDefaultView)
        if adapter is not None:
            return adapter.getAbsoluteURL()
        else:
            return