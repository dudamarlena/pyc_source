# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/testing.py
# Compiled at: 2018-10-18 17:35:14
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
import os, shutil, tempfile
autoform = (
 'plone.autoform', {'loadZCML': True})
tinymce = ('Products.TinyMCE', {'loadZCML': True})
products = list(PLONE_FIXTURE.products)
products.insert(products.index(tinymce), autoform)
PLONE_FIXTURE.products = tuple(products)

class Fixture(PloneSandboxLayer):
    defaultBases = (
     PLONE_FIXTURE,)

    def setUp(self):
        """Copy all files used in tests to the temporary directory."""
        super(Fixture, self).setUp()
        tempdir = tempfile.gettempdir()
        path = os.path.join(os.path.dirname(__file__), 'tests', 'files')
        for i in os.listdir(path):
            shutil.copy(os.path.join(path, i), tempdir)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.Doormat')
        z2.installProduct(app, 'Products.PloneFormGen')
        import brasil.gov.portal
        self.loadZCML(package=brasil.gov.portal)
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'brasil.gov.portal:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(
 FIXTURE,), name='brasil.gov.portal:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(
 FIXTURE,), name='brasil.gov.portal:Functional')

class InitContentFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(InitContentFixture, self).setUpPloneSite(portal)
        portal.title = 'Portal Brasil'
        portal.description = 'Secretaria de Comunicação Social'
        wf = portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')
        types = ('Document', 'Folder', 'Link', 'Topic', 'News Item')
        wf.setChainForPortalTypes(types, '(Default)')


INITCONTENT_FIXTURE = InitContentFixture()
INITCONTENT_TESTING = IntegrationTesting(bases=(
 INITCONTENT_FIXTURE,), name='brasil.gov.portal:InitContent')

class AcceptanceFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(AcceptanceFixture, self).setUpPloneSite(portal)
        portal.title = 'Portal Brasil'
        portal.description = 'Secretaria de Comunicação Social'


ACCEPTANCE_FIXTURE = AcceptanceFixture()
ACCEPTANCE_TESTING = FunctionalTesting(bases=(
 AUTOLOGIN_LIBRARY_FIXTURE,
 ACCEPTANCE_FIXTURE,
 z2.ZSERVER_FIXTURE), name='brasil.gov.portal:Acceptance')