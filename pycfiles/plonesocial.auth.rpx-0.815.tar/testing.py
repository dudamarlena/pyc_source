# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/testing.py
# Compiled at: 2013-07-05 10:36:06
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig

class PlonesocialActivitystream(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plonesocial.activitystream
        xmlconfig.file('configure.zcml', plonesocial.activitystream, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonesocial.activitystream:default')


PLONESOCIAL_ACTIVITYSTREAM_FIXTURE = PlonesocialActivitystream()
PLONESOCIAL_ACTIVITYSTREAM_INTEGRATION_TESTING = IntegrationTesting(bases=(PLONESOCIAL_ACTIVITYSTREAM_FIXTURE,), name='PlonesocialActivitystream:Integration')