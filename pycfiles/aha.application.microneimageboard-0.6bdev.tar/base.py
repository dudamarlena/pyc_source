# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/auth/base.py
# Compiled at: 2011-03-22 20:00:44
__doc__ = ' appengine.py - A module to provide base class of authentication plugin.\n\n$Id: appengine.py 638 2010-08-10 04:05:57Z ats $\n'
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'

class BaseAuth(object):
    """
    A base class of authentication plugin for aha framework.
    The authentication class for aha consists of 4 methods.
    If you want to write your own authentication plugin class,
    you have to override all these methods.
    They are called automatically via @authenticate decorator.

    = auth(self, ins, *param, **kws)
    
    The method to perform authentication. It checls status,
    redirect to login URL in case authentication is required.

    = auth_redirect(self, ins, *param, **kws)
    
    A method to redirect to such as login form.
    Typically this method is called from auth() method.

    = get_user(self, ins, *param, **kws)
    
    A method to obtain user object after authentication.

    = logout(self, ins, *param, **kws)
    
    A method to perform logout, clearing login information etc.

    """

    def auth(self, ins, *param, **kws):
        """
        A method to perform authentication, or
        to check if the authentication has been performed.
        It returns true on success, false on failure.
        
        :param ins: The controller instance.
        :param param: parameter to the authentication function.
        :param kws: keyword argument to the authentication function.
        """
        raise NotImplementedError('You must override auth() method')

    def auth_redirect(self, ins, *param, **kws):
        """
        A method to perform redirection
        when the authentication fails, user doesn't have privileges, etc.

        :param ins: The controller instance.
        :param param: parameter to the authentication function.
        :param kws: keyword argument to the authentication function.
        """
        raise NotImplementedError('You must override auth_redirect() method')

    def get_user(self, ins, *param, **kws):
        """
        A method to return current login user.
        It returns user dict if the user is logging in,
            None if doesn't.
        A returned dictionary should have following data::

           {'type':'type of the authentication'
            'nickname':'a nickname',
            'email':'an email',
            'userid':'a userid',
            'realname':'a realname',
            }

        :param ins: The controller instance.
        :param param: parameter to the authentication function.
        :param kws: keyword argument to the authentication function.
        """
        raise NotImplementedError('You must override do_auth() method')

    def logout(self, ins, *param, **kws):
        """
        A method to perform logout action.
        Typically it's called from authenticate decorator.

        :param ins: The controller instance.
        :param param: parameter to the authentication function.
        :param kws: keyword argument to the authentication function.

        """
        raise NotImplementedError('You must override logout() method')


def main():
    pass