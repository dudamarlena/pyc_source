# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagesitemaps/tests.py
# Compiled at: 2012-05-03 12:06:32
"""
Test Google Image Sitemaps
"""
from django.test import TestCase
from django.utils.importlib import import_module
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.conf import settings
from imagesitemaps import ImageSitemap

class TestSitemapObject(object):
    pass


TEST_IMAGE_TAGS = ('loc', 'title', 'caption', 'license')
TEST_VALUES = (
 ('/html-5/thumb.jpg', 'HTML5', 'HTML 5', 'http://creativecommons.org/licenses/by-nd/3.0/legalcode'),
 ('/cars/honda-5d/thumb.jpg', 'Honda 5D', '5 doors Honda', 'http://creativecommons.org/licenses/by-nd/3.0/legalcode'),
 ('/my-apple/thumb.jpg', 'Golden apple', 'Completely golden', 'http://creativecommons.org/licenses/by-nd/3.0/legalcode'))

def get_test_objects():
    for val in TEST_VALUES:
        obj = TestSitemapObject()
        setattr(obj, 'location', val[0])
        val = val[1:]
        for i, tag in enumerate(TEST_IMAGE_TAGS):
            setattr(obj, tag, val[i])

        yield obj


class TestImageSitemap(ImageSitemap):

    def items(self):
        return [ i for i in get_test_objects() ]

    def location(self, obj):
        return obj.location

    def image_title(self, img):
        return img.title

    def image_caption(self, img):
        return img.caption


image_sitemaps = {'': TestImageSitemap}

class ImageSitemapTest(TestCase):

    def setUp(self):
        self.urlconf = import_module(settings.ROOT_URLCONF)
        self.original_urlpatterns = self.urlconf.urlpatterns[:]
        self.urlconf.urlpatterns += patterns('', url('^image_sitemap.xml$', 'imagesitemaps.views.sitemap', {'sitemaps': image_sitemaps}, name='test_image_sitemap'))
        self.sitemap_view = reverse('test_image_sitemap')
        self.test_objects = [ i for i in get_test_objects() ]

    def get_document(self):
        from xml.dom.minidom import parseString
        response = self.client.get(self.sitemap_view)
        return parseString(response.content)

    def test_valid_xml(self):
        """
        Test if the sitemap is a valid XML document.
        """
        self.get_document()

    def test_valid_sitemap_dom(self):
        doc = self.get_document()
        self.assertEqual(doc.documentElement.nodeName, 'urlset')
        urlset = doc.documentElement
        self.assertTrue(urlset.hasAttribute('xmlns:image'))
        self.assertTrue(urlset.hasAttribute('xmlns'))
        urls = urlset.getElementsByTagName('url')
        self.assertEqual(len(urls), len(self.test_objects))
        for url in urls:
            locs = url.getElementsByTagName('loc')
            self.assertTrue(len(locs), 1)
            images = url.getElementsByTagName('image:image')
            self.assertTrue(len(images), 1)
            image = images[0]

    def tearDown(self):
        self.urlconf.urlpatterns = self.original_urlpatterns