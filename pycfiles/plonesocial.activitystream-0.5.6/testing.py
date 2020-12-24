# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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