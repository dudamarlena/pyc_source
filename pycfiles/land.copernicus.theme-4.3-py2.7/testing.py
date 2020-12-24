# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/theme/testing.py
# Compiled at: 2018-04-23 08:38:48
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE

class Fixture(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import land.copernicus.theme
        self.loadZCML(package=land.copernicus.theme)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'land.copernicus.theme:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='land.copernicus.theme:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE, ZSERVER_FIXTURE), name='land.copernicus.theme:Functional')