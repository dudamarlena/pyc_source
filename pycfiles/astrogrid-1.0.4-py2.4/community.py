# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/community.py
# Compiled at: 2007-06-03 06:30:23
"""
Module to login/logout and get user information.

"""
__id__ = '$Id: community.py 111 2007-06-03 10:30:23Z eddie $'
__docformat__ = 'restructuredtext en'
from astrogrid import acr
from watcherrors import watcherrors, needslogin

class Community:
    """
    Community related tasks.

    Example:

       >>> from astrogrid import Community
       >>> c = Community()
       >>> c.isLoggedIn()
       False
       >>> c.login('me', 'mypass', 'mycommunity')
       >>> c.isLoggedIn()
       True
       >>> c.logout()
       
    """
    __module__ = __name__

    @watcherrors
    def __init__(self):
        self.community = acr.astrogrid.community

    @watcherrors
    def isLoggedIn(self):
        """
        Check if logged in.

        :returns: True or False
        """
        return self.community.isLoggedIn()

    @watcherrors
    def guiLogin(self):
        """Ask for credentials using the Workbench GUI"""
        self.community.guiLogin()

    @watcherrors
    def login(self, username, password, community):
        """
        Login with username and password. If not defined then use the ones 
        defined in the configuration file.

        :Parameters:
          username : str
            User name
          password : str
            Password
          community : str
            Community
        """
        return self.community.login(username, password, community) == 'OK'

    @watcherrors
    def logout(self):
        """Log out"""
        return self.community.logout() == 'OK'

    @watcherrors
    @needslogin
    def getUserInfo(self):
        """Returns user information"""
        return self.community.getUserInformation()