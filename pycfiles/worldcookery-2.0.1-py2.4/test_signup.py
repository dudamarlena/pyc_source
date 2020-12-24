# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/ftests/test_signup.py
# Compiled at: 2006-09-23 14:08:58
import unittest, transaction
from zope.app.testing.functional import FunctionalDocFileSuite, getRootFolder
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.securitypolicy.interfaces import IPrincipalRoleManager
from worldcookery.cookiecredentials import CookieCredentialsPlugin
from worldcookery.signup import SignupPrincipalFolder

def setUp(test):
    root = getRootFolder()
    sm = root.getSiteManager()
    pau = sm['pau'] = PluggableAuthentication()
    sm.registerUtility(pau, IAuthentication)
    cookies = pau['cookies'] = CookieCredentialsPlugin()
    cookies.loginpagename = 'wclogin.html'
    pau.credentialsPlugins = ('cookies', )
    signups = pau['signups'] = SignupPrincipalFolder('worldcookery.signup.')
    signups.signup_roles = ['worldcookery.Visitor', 'worldcookery.Member']
    pau.authenticatorPlugins = ('signups', )
    role_manager = IPrincipalRoleManager(root)
    role_manager.assignRoleToPrincipal('worldcookery.Visitor', 'zope.anybody')
    transaction.commit()


def test_suite():
    return FunctionalDocFileSuite('signup.txt', package='worldcookery.browser', setUp=setUp)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')