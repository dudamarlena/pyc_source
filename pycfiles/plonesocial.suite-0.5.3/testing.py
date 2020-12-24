# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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