# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/layout/authpersonalbar/tests/_testing.py
# Compiled at: 2011-04-07 05:20:40
import doctest
from zope.configuration import xmlconfig
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing.layers import FunctionalTesting, IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

class CollectiveLayoutAuthpersonalbarLayer(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.layout.authpersonalbar
        xmlconfig.file('configure.zcml', collective.layout.authpersonalbar, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.layout.authpersonalbar:default')


COLLECTIVELAYOUTAUTHPERSONALBAR_FIXTURE = CollectiveLayoutAuthpersonalbarLayer()
COLLECTIVELAYOUTAUTHPERSONALBAR_INTEGRATION_TESTING = IntegrationTesting(bases=(
 COLLECTIVELAYOUTAUTHPERSONALBAR_FIXTURE,), name='CollectiveLayoutAuthpersonalbarLayer:Integration')
COLLECTIVELAYOUTAUTHPERSONALBAR_FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 COLLECTIVELAYOUTAUTHPERSONALBAR_FIXTURE,), name='CollectiveLayoutAuthpersonalbarLayer:Functional')
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE