# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_upgrades.py
# Compiled at: 2018-10-17 12:54:29
# Size of source mod 2**32: 7472 bytes
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.testing import INTEGRATION_TESTING
from plone import api
import unittest

class BaseUpgradeTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING
    profile_id = 'collective.lazysizes:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        assert version == self.from_

    def get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        if steps:
            return steps[0]

    def do_upgrade(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)


class To2TestCase(BaseUpgradeTestCase):
    from_ = '1'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    def test_add_new_field_to_configlet(self):
        title = 'Add new field to configlet'
        step = self.get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from collective.lazysizes.interfaces import ILazySizesSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        del registry.records[record]
        with self.assertRaises(KeyError):
            registry.forInterface(ILazySizesSettings)
        self.do_upgrade(step)
        settings = registry.forInterface(ILazySizesSettings)
        self.assertTrue(hasattr(settings, 'css_class_blacklist'))
        self.assertEqual(settings.css_class_blacklist, set([]))


class To3TestCase(BaseUpgradeTestCase):
    from_ = '2'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)


class To4TestCase(BaseUpgradeTestCase):
    from_ = '3'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)


class To5TestCase(BaseUpgradeTestCase):
    from_ = '4'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_use_amd_version(self):
        title = 'Use AMD version of Lazysizes'
        step = self.get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from collective.lazysizes.upgrades.v5 import NEW_JS
        from collective.lazysizes.upgrades.v5 import OLD_JS
        portal_js = api.portal.get_tool('portal_javascripts')
        portal_js.registerResource(OLD_JS)
        self.assertIn(OLD_JS, portal_js.getResourceIds())
        self.do_upgrade(step)
        self.assertNotIn(OLD_JS, portal_js.getResourceIds())
        self.assertIn(NEW_JS, portal_js.getResourceIds())


class To6TestCase(BaseUpgradeTestCase):
    from_ = '5'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)


class To7TestCase(BaseUpgradeTestCase):
    from_ = '6'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_remove_respimg_polyfill(self):
        title = 'Remove respimg polyfill plugin'
        step = self.get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from collective.lazysizes.upgrades.v7 import JS
        portal_js = api.portal.get_tool('portal_javascripts')
        portal_js.registerResource(JS)
        self.assertIn(JS, portal_js.getResourceIds())
        self.do_upgrade(step)
        self.assertNotIn(JS, portal_js.getResourceIds())


class To8TestCase(BaseUpgradeTestCase):
    from_ = '7'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)

    def test_add_new_field_to_configlet(self):
        title = 'Add lazyload_authenticated field to configlet'
        step = self.get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        from collective.lazysizes.interfaces import ILazySizesSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        record = ILazySizesSettings.__identifier__ + '.lazyload_authenticated'
        del registry.records[record]
        with self.assertRaises(KeyError):
            registry.forInterface(ILazySizesSettings)
        self.do_upgrade(step)
        settings = registry.forInterface(ILazySizesSettings)
        self.assertTrue(hasattr(settings, 'lazyload_authenticated'))
        self.assertEqual(settings.lazyload_authenticated, False)


class To9TestCase(BaseUpgradeTestCase):
    from_ = '8'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 1)


class To10TestCase(BaseUpgradeTestCase):
    from_ = '9'

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Plone 4.3')
    def test_deprecate_resource_registries_plone_4(self):
        title = 'Deprecate resource registries'
        step = self.get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        RESOURCES = set([
         '++resource++collective.lazysizes/ls.twitter.min.js',
         '++resource++collective.lazysizes/lazysizes-umd.min.js'])
        jsregistry = api.portal.get_tool('portal_javascripts')
        for id_ in RESOURCES:
            jsregistry.registerResource(id_)

        self.assertTrue(set(jsregistry.getResourceIds()) & RESOURCES)
        self.do_upgrade(step)
        self.assertFalse(set(jsregistry.getResourceIds()) & RESOURCES)