# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/interfaces.py
# Compiled at: 2013-02-09 19:59:16
from zope.interface import Interface

class IAuthCheck(Interface):
    """
    This interface is for verifying authentication information with your
    backing store of choice. In the short term this will be limited to
    usernames and passwords, but may grow to support other authentication
    methods.
    """

    def checkauth(self, username, password):
        """
        Validate a given username and password against some kind of store,
        usually a relational database. Return the users user_id if credentials
        are valid, otherwise False or None.
        """
        pass