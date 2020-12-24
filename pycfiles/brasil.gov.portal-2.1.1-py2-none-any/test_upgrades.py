# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_upgrades.py
# Compiled at: 2018-11-23 14:32:39
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import queryUtility
import unittest

class UpgradeBaseTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING
    profile_id = 'brasil.gov.portal:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [ s for s in upgrades[0] if s['title'] == title ]
        if steps:
            return steps[0]
        else:
            return

    def _do_upgrade(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)


class to10900TestCase(UpgradeBaseTestCase):
    from_ = '*'
    to_ = '10900'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 7)

    def test_remove_styles(self):
        title = 'Move styles to brasil.gov.temas package'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from brasil.gov.portal.upgrades.v10900 import STYLES
        css_tool = api.portal.get_tool('portal_css')
        for css in STYLES:
            css_tool.registerResource(id=css)
            self.assertIn(css, css_tool.getResourceIds())

        self._do_upgrade(step)
        for css in STYLES:
            self.assertNotIn(css, css_tool.getResourceIds())

    def test_show_global_sections(self):
        title = 'Show back global_sections viewlet'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        storage = queryUtility(IViewletSettingsStorage)
        manager = 'plone.portalheader'
        skinname = 'Plone Default'
        hidden = ('plone.global_sections', )
        storage.setHidden(manager, skinname, hidden)
        self._do_upgrade(step)
        hidden = storage.getHidden(manager, skinname)
        self.assertEqual(hidden, ())

    def test_remove_nitf_customizations(self):
        title = 'Remove collective.nitf customizations'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        custom_view = 'nitf_custom_view'
        types_tool = api.portal.get_tool('portal_types')
        nitf = types_tool['collective.nitf.content']
        nitf.view_methods += tuple(custom_view)
        nitf.default_view_fallback = False
        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(self.portal, 'collective.nitf.content', 'n1')
            self.n2 = api.content.create(self.portal, 'collective.nitf.content', 'n2')
        self.n1.setLayout(custom_view)
        self.n2.setLayout(custom_view)
        self.assertEqual(self.n1.getLayout(), custom_view)
        self.assertEqual(self.n2.getLayout(), custom_view)
        self._do_upgrade(step)
        self.assertNotIn(custom_view, nitf.view_methods)
        self.assertTrue(nitf.default_view_fallback)
        self.assertEqual(self.n1.getLayout(), 'view')
        self.assertEqual(self.n2.getLayout(), 'view')

    def test_search_for_embedder(self):
        title = 'Remove sc.embedder from types_not_searched'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        settings = api.portal.get_tool('portal_properties').site_properties
        settings.types_not_searched += ('sc.embedder', )
        self.assertIn('sc.embedder', settings.types_not_searched)
        self._do_upgrade(step)
        self.assertNotIn('sc.embedder', settings.types_not_searched)

    def test_infographic_content_type(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        types = api.portal.get_tool('portal_types')
        del types['Infographic']
        self.assertNotIn('Infographic', types)
        self.setup.upgradeProfile('brasil.gov.portal:default')
        self.assertIn('Infographic', types)
        with api.env.adopt_roles(['Manager']):
            api.content.create(self.portal, 'Infographic', 'foo')
            api.content.delete(self.portal['foo'])

    def test_portal_services_settings_configlet(self):
        configlet = 'portal-services-settings'
        portal_controlpanel = api.portal.get_tool('portal_controlpanel')
        actions = portal_controlpanel.listActions()
        idx = [ actions.index(i) for i in actions if i.getId() == configlet ]
        portal_controlpanel.deleteActions(idx)
        self.assertNotIn(configlet, [ c.getId() for c in portal_controlpanel.listActions() ])
        self.setup.upgradeProfile('brasil.gov.portal:default')
        self.assertIn(configlet, [ c.getId() for c in portal_controlpanel.listActions() ])

    def test_update_galeria_image_sizes(self):
        title = 'Update galeria image sizes.'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        settings = api.portal.get_tool('portal_properties').imaging_properties
        allowed_sizes = set(settings.allowed_sizes)
        allowed_sizes |= frozenset([
         'galeria_de_foto_thumb 87:49', 'galeria_de_foto_view 748:513'])
        allowed_sizes -= frozenset(['galeria_de_foto_view 1150:650'])
        settings.allowed_sizes = tuple(allowed_sizes)
        self.assertIn('galeria_de_foto_thumb 87:49', settings.allowed_sizes)
        self.assertIn('galeria_de_foto_view 748:513', settings.allowed_sizes)
        self.assertNotIn('galeria_de_foto_view 1150:650', settings.allowed_sizes)
        self._do_upgrade(step)
        self.assertNotIn('galeria_de_foto_thumb 87:49', settings.allowed_sizes)
        self.assertNotIn('galeria_de_foto_view 748:513', settings.allowed_sizes)
        self.assertIn('galeria_de_foto_view 1150:650', settings.allowed_sizes)

    def test_install_keyword_manager(self):
        title = 'Install Products.PloneKeywordManager'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        addon = 'PloneKeywordManager'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts([addon])
        self.assertFalse(qi.isProductInstalled(addon))
        self._do_upgrade(step)
        self.assertTrue(qi.isProductInstalled(addon))


class to10901TestCase(UpgradeBaseTestCase):
    from_ = '10900'
    to_ = '10901'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 7)

    def test_remove_root_portlets(self):
        title = 'Remove portlet assigments at portal root'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        self._do_upgrade(step)

    def test_fix_column_widths(self):
        title = 'Fix column widths on cover objects'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        self._do_upgrade(step)

    def test_import_various(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        self._do_upgrade(step)

    @unittest.expectedFailure
    def test_update_infographic_workflow(self):
        title = 'Remove workflow from Infographic content type'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        wftool = api.portal.get_tool('portal_workflow')
        wftool.setChainForPortalTypes(['Infographic'], '(Default)')
        self.assertEqual(wftool.getChainForPortalType('Infographic'), wftool.getDefaultChain())
        self._do_upgrade(step)
        self.assertEqual(wftool.getChainForPortalType('Infographic'), ())

    def test_add_content_central_menu(self):
        title = 'Add Content Central menu option to Folder content type'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        view = 'centrais-de-conteudo'
        folder_fti = api.portal.get_tool('portal_types')['Folder']
        view_methods = list(folder_fti.view_methods)
        view_methods.remove(view)
        folder_fti.view_methods = tuple(view_methods)
        self.assertNotIn(view, folder_fti.view_methods)
        self._do_upgrade(step)
        self.assertIn(view, folder_fti.view_methods)

    def test_add_results_filter_menu(self):
        title = 'Add Results Filter menu option to Collection content type'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        view = 'filtro-de-resultados'
        collection_fti = api.portal.get_tool('portal_types')['Collection']
        view_methods = list(collection_fti.view_methods)
        view_methods.remove(view)
        collection_fti.view_methods = tuple(view_methods)
        self.assertNotIn(view, collection_fti.view_methods)
        self._do_upgrade(step)
        self.assertIn(view, collection_fti.view_methods)


class to10902TestCase(UpgradeBaseTestCase):
    from_ = '10901'
    to_ = '10902'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)

    def test_update_image_scales(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        NEW_SCALES = set([
         'Imagem-3C 273:273',
         'Imagem-4C 370:370',
         'Imagem-5C 468:468',
         'Imagem-6C 565:565',
         'Imagem-7C 663:663',
         'Imagem-8C 760:760',
         'Imagem-Full: 1150:1150'])
        settings = api.portal.get_tool('portal_properties').imaging_properties
        allowed_sizes = set(settings.allowed_sizes) - NEW_SCALES
        settings.allowed_sizes = tuple(allowed_sizes)
        self.assertFalse(set(settings.allowed_sizes) & NEW_SCALES)
        self._do_upgrade(step)
        for scale in NEW_SCALES:
            self.assertIn(scale, settings.allowed_sizes)


class to10903TestCase(UpgradeBaseTestCase):
    from_ = '10902'
    to_ = '10903'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    def test_install_dropdownmenu(self):
        title = 'Install webcouturier.dropdownmenu'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        addon = 'webcouturier.dropdownmenu'
        qi = api.portal.get_tool('portal_quickinstaller')
        qi.uninstallProducts([addon])
        self.assertFalse(qi.isProductInstalled(addon))
        self._do_upgrade(step)
        self.assertTrue(qi.isProductInstalled(addon))

    def test_dropdownmenu_properties(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        dropdown = api.portal.get_tool('portal_properties').dropdown_properties
        dropdown.dropdown_depth = 3
        self._do_upgrade(step)
        self.assertEqual(dropdown.dropdown_depth, 1)

    def test_navigation_properties(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        navtree = api.portal.get_tool('portal_properties').navtree_properties
        navtree.metaTypesNotToList = ()
        self._do_upgrade(step)
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory
        types = getUtility(IVocabularyFactory, 'plone.app.vocabularies.PortalTypes')(None)
        types = set(t.value for t in types)
        exclude = set(navtree.metaTypesNotToList)
        expected = {
         'Document',
         'Folder',
         'FormFolder'}
        self.assertSetEqual(types - exclude, expected)
        return


class to10904TestCase(UpgradeBaseTestCase):
    from_ = '10903'
    to_ = '10904'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 3)

    def test_import_various(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        name = 'collective.cover.controlpanel.ICoverSettings.styles'
        styles = api.portal.get_registry_record(name)
        value = 'Com Etiqueta|tile-etiqueta'
        styles -= {value}
        api.portal.set_registry_record(name=name, value=styles)
        self.assertNotIn(value, api.portal.get_registry_record(name))
        self._do_upgrade(step)
        self.assertIn(value, api.portal.get_registry_record(name))

    def test_deprecate_resource_registries(self):
        title = 'Deprecate resource registries'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from brasil.gov.portal.upgrades.v10904 import SCRIPTS
        js_tool = api.portal.get_tool('portal_javascripts')
        for js in SCRIPTS:
            js_tool.registerResource(id=js)
            self.assertIn(js, js_tool.getResourceIds())

        self._do_upgrade(step)
        for js in SCRIPTS:
            self.assertNotIn(js, js_tool.getResourceIds())

    def test_uninstall_doormat(self):
        title = 'Uninstall Products.Doormat'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        addon = 'Doormat'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.installProduct(addon)
        self.assertTrue(qi.isProductInstalled(addon))
        self._do_upgrade(step)
        self.assertFalse(qi.isProductInstalled(addon))


class to10905TestCase(UpgradeBaseTestCase):
    from_ = '10904'
    to_ = '10905'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)

    def test_import_various(self):
        title = 'Import various'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        site_actions = api.portal.get_tool('portal_actions').site_actions
        site_actions['accessibility'].visible = True
        site_actions['mapadosite'].visible = True
        del site_actions['vlibras']
        self.assertNotIn('vlibras', site_actions)
        self._do_upgrade(step)
        self.assertFalse(site_actions['accessibility'].visible)
        self.assertFalse(site_actions['mapadosite'].visible)
        self.assertIn('vlibras', site_actions)


class to10906TestCase(UpgradeBaseTestCase):
    from_ = '10905'
    to_ = '10906'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)

    def test_fix_nitf_default_view(self):
        title = 'Fix wrong value on News Article factory'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        custom_view = 'nitf_custom_view'
        types_tool = api.portal.get_tool('portal_types')
        nitf = types_tool['collective.nitf.content']
        nitf.default_view = custom_view
        self.assertEqual(nitf.default_view, custom_view)
        self._do_upgrade(step)
        self.assertEqual(nitf.default_view, 'view')