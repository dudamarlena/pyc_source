# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/tests/test_photogallery.py
# Compiled at: 2017-10-20 20:11:12
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.tests.test_image import zptlogo
from sc.photogallery.interfaces import IPhotoGallery
from sc.photogallery.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility
import unittest

class PhotoGalleryTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'test')
        self.gallery = api.content.create(self.folder, 'Photo Gallery', 'gallery')

    def test_adding(self):
        self.assertTrue(IPhotoGallery.providedBy(self.gallery))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        schema = fti.lookupSchema()
        self.assertEqual(IPhotoGallery, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Photo Gallery')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPhotoGallery.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        self.assertTrue(IExcludeFromNavigation.providedBy(self.gallery))

    def test_allowed_content_types(self):
        allowed_types = [ t.getId() for t in self.gallery.allowedContentTypes() ]
        expected = [
         'Image']
        self.assertListEqual(allowed_types, expected)

    def test_selectable_as_folder_default_page(self):
        self.folder.setDefaultPage('gallery')
        self.assertEqual(self.folder.getDefaultPage(), 'gallery')

    def test_no_image(self):
        self.assertIsNone(self.gallery.image())
        self.assertIsNone(self.gallery.tag())

    def test_image_caption(self):
        self.assertEqual(self.gallery.image_caption(), '')
        api.content.create(self.gallery, 'Image', 'foo', description='Foo')
        self.assertEqual(self.gallery.image_caption(), 'Foo')

    def test_image(self):
        from sc.photogallery.tests.api_hacks import set_image_field
        image = api.content.create(self.gallery, 'Image', 'foo')
        set_image_field(image, zptlogo, 'image/gif')
        try:
            data = self.gallery.image().image.data
        except AttributeError:
            data = self.gallery.image().data

        self.assertEqual(data, zptlogo)
        self.assertIn('height="16" width="16"', self.gallery.tag())