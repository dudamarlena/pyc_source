# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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