# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/plonetheme/unam/testing.py
# Compiled at: 2013-04-03 17:48:41
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig

class Theming(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plonetheme.unam
        xmlconfig.file('configure.zcml', plonetheme.unam, context=configurationContext)

    def setUpPloneSite(self, portal):
        pass


THEMING_FIXTURE = Theming()
THEMING_INTEGRATION_TESTING = IntegrationTesting(bases=(
 THEMING_FIXTURE,), name='Theming:Integration')
THEMING_FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 THEMING_FIXTURE,), name='Theming:Functional')