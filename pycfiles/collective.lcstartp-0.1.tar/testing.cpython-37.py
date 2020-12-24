# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/testing.py
# Compiled at: 2019-03-12 21:32:21
# Size of source mod 2**32: 2048 bytes
__doc__ = 'Setup testing fixture.\n\nFor Plone 5 we need to install plone.app.contenttypes.\n'
from collective.lazysizes.config import PROJECTNAME
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
import pkg_resources
try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    import plone.app.contenttypes.testing as PLONE_FIXTURE
IS_BBB = api.env.plone_version().startswith('4.3')

class QIBBB:
    """QIBBB"""

    def uninstall(self):
        if IS_BBB:
            qi = self.portal['portal_quickinstaller']
            with api.env.adopt_roles(['Manager']):
                qi.uninstallProducts([PROJECTNAME])
        else:
            from Products.CMFPlone.utils import get_installer
            qi = get_installer(self.portal, self.request)
            with api.env.adopt_roles(['Manager']):
                qi.uninstall_product(PROJECTNAME)
        return qi


class Fixture(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lazysizes
        self.loadZCML(package=(collective.lazysizes))

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.lazysizes:default')
        portal.portal_workflow.setDefaultChain('one_state_workflow')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,),
  name='collective.lazysizes:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,),
  name='collective.lazysizes:Functional')
ROBOT_TESTING = FunctionalTesting(bases=(
 FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
  name='collective.lazysizes:Robot')