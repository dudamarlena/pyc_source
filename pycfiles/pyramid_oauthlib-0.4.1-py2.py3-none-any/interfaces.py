# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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