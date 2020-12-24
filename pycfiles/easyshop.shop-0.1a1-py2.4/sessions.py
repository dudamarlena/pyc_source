# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/utilities/sessions.py
# Compiled at: 2008-09-03 11:15:25
from DateTime import DateTime
from zope.interface import implements
from easyshop.core.interfaces import ISessionManagement

class SessionManagement:
    """
    """
    __module__ = __name__
    implements(ISessionManagement)

    def getSID(self, request):
        """
        """
        sid = request.cookies.get('easyshop-sid', None)
        if sid is None:
            try:
                sid = request.SESSION.getId()
                expires = (DateTime() + 10).toZone('GMT').rfc822()
                request.RESPONSE.setCookie('easyshop-sid', sid, expires=expires, path='/')
            except AttributeError:
                sid = 'DUMMY_SESSION'

        return sid