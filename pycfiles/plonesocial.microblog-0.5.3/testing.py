# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/testing.py
# Compiled at: 2013-04-12 05:54:49
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig

class PlonesocialMicroblog(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plonesocial.microblog
        xmlconfig.file('configure.zcml', plonesocial.microblog, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonesocial.microblog:default')


PLONESOCIAL_MICROBLOG_FIXTURE = PlonesocialMicroblog()
PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING = IntegrationTesting(bases=(PLONESOCIAL_MICROBLOG_FIXTURE,), name='PlonesocialMicroblog:Integration')