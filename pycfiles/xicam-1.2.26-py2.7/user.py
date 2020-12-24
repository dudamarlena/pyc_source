# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\user.py
# Compiled at: 2018-08-27 17:21:06
from requests import Session

class User(object):
    """
    class for user credentials and sending and posting requests

    Attributes
    ----------
    session : requests.Session
    username : str
    logged_in : bool
        Boolean standing for login state. True if logged in
    """

    def __init__(self):
        super(User, self).__init__()
        self.session = Session()
        self.logged_in = False
        self.username = None
        return

    def __del__(self):
        try:
            self.session.close()
        except TypeError:
            pass

    def login(self, username):
        """
        Sets the attributes according to login
        """
        self.username = username
        self.logged_in = True
        return self

    def logout(self):
        """
        When logging out
        """
        self.logged_in = False

    def check_login(self):
        """
        Raise an error if user is not logged in
        """
        if self.logged_in is False:
            raise AUTHError('%s is not logged in.' % self.username)

    def post(self, url, **kwargs):
        """
        Wrap session post
        """
        response = self.session.post(url, **kwargs)
        return response

    def get(self, url, **kwargs):
        """
         Wrap session get
         """
        response = self.session.get(url, **kwargs)
        return response

    @staticmethod
    def check_response(response):
        """
        Check for errors in a REST call
        """
        if response.ok:
            return response.json()
        response.raise_for_status()


class AUTHError(Exception):
    """Error when users not logged in"""
    pass