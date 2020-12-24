# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.network/plonesocial/network/testing.py
# Compiled at: 2013-09-11 10:08:01
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig

class PlonesocialNetwork(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plonesocial.network
        xmlconfig.file('configure.zcml', plonesocial.network, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonesocial.network:default')


PLONESOCIAL_NETWORK_FIXTURE = PlonesocialNetwork()
PLONESOCIAL_NETWORK_INTEGRATION_TESTING = IntegrationTesting(bases=(PLONESOCIAL_NETWORK_FIXTURE,), name='PlonesocialNetwork:Integration')