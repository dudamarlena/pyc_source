# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/cookiecredentials/tests.py
# Compiled at: 2007-09-20 06:47:27
import os.path, unittest, transaction
from zope.app.testing.functional import FunctionalDocFileSuite, getRootFolder
from zope.app.testing.functional import ZCMLLayer
from zope.app.security.interfaces import IAuthentication
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.principalfolder import InternalPrincipal
from zope.app.securitypolicy.interfaces import IPrincipalRoleManager
from wc.cookiecredentials.plugin import CookieCredentialsPlugin
ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer')

def setUp(test):
    root = getRootFolder()
    sm = root.getSiteManager()
    pau = sm['pau'] = PluggableAuthentication()
    sm.registerUtility(pau, IAuthentication)
    cookies = pau['cookies'] = CookieCredentialsPlugin()
    pau.credentialsPlugins = ('cookies', )
    principals = pau['principals'] = PrincipalFolder('wc.test.')
    principals['admin'] = InternalPrincipal('admin', 'secret', 'Administrator')
    pau.authenticatorPlugins = ('principals', )
    role_manager = IPrincipalRoleManager(root)
    role_manager.assignRoleToPrincipal('zope.Manager', 'wc.test.admin')
    transaction.commit()


def test_suite():
    suite = FunctionalDocFileSuite('README.txt', package='wc.cookiecredentials', setUp=setUp)
    suite.layer = FunctionalLayer
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')