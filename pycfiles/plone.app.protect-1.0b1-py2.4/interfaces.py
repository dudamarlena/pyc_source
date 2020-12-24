# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/interfaces.py
# Compiled at: 2008-03-07 17:28:21
from zope.interface import Interface

class IAuthenticatorView(Interface):
    __module__ = __name__

    def authenticator():
        """Return an xhtml snippet which sets an authenticator.
        
        This must be included inside a <form> element.
        """
        pass

    def verify():
        """
        Verify if the request contains a valid authenticator.
        """
        pass