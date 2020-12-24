# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_transformer.py
# Compiled at: 2018-10-17 12:54:29
# Size of source mod 2**32: 8244 bytes
from collective.lazysizes.interfaces import ILazySizesSettings
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.transform import LazySizesTransform
from collective.lazysizes.transform import PLACEHOLDER
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from testfixtures import log_capture
from zope.component import getUtility
import logging, lxml, unittest
HTML = '<html>\n  <body>\n    <div id="content">\n      <img src="{url}" class="{klass}" />\n    </div>\n  </body>\n</html>\n'
TWEET = '\n<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Nothing Twitter is doing is working <a href="https://t.co/s0FppnacwK">https://t.co/s0FppnacwK</a> <a href="https://t.co/GK9MRfQkYO">pic.twitter.com/GK9MRfQkYO</a></p>&mdash; The Verge (@verge) <a href="https://twitter.com/verge/status/725096763972001794">April 26, 2016</a></blockquote>\n<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>\n'
TWEET_MODIFIED = '\n<blockquote class="twitter-tweet" data-lang="en"></blockquote>\n<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>\n'
TWEET_NO_SCRIPT = '\n<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Nothing Twitter is doing is working <a href="https://t.co/s0FppnacwK">https://t.co/s0FppnacwK</a> <a href="https://t.co/GK9MRfQkYO">pic.twitter.com/GK9MRfQkYO</a></p>&mdash; The Verge (@verge) <a href="https://twitter.com/verge/status/725096763972001794">April 26, 2016</a></blockquote>\n'

class TransformerTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        request = self.layer['request']
        request.response.setHeader('Content-Type', 'text/html')
        self.transformer = LazySizesTransform(None, request)

    def test_transformer_anonymous_user(self):
        logout()
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertEqual(img.attrib['class'], 'lazyload')
        self.assertIn(img.attrib['data-src'], url)

    def test_transformer_authenticated_user_disabled(self):
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertIsNone(result)

    def test_transformer_authenticated_user_enabled(self):
        record = ILazySizesSettings.__identifier__ + '.lazyload_authenticated'
        api.portal.set_registry_record(record, True)
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertEqual(img.attrib['class'], 'lazyload')
        self.assertIn(img.attrib['data-src'], url)

    def test_lazyload_img(self):
        url = 'http://example.com/foo.png'
        img_tag = '<img src="{0}" />'.format(url)
        element = lxml.html.fromstring(img_tag)
        self.assertEqual(self.transformer._lazyload_img(element), url)
        self.assertIn('src', element.attrib)
        self.assertTrue(element.attrib['src'].startswith('data:image/png'))
        self.assertIn('data-src', element.attrib)
        self.assertEqual(element.attrib['data-src'], url)

    @log_capture(level=(logging.ERROR))
    def test_lazyload_img_no_src(self, l):
        element = lxml.html.fromstring('<img />')
        self.assertIsNone(self.transformer._lazyload_img(element))
        msg = '<img> tag without src attribute in: http://nohost'
        expected = ('collective.lazysizes', 'ERROR', msg)
        l.check(expected)

    def test_lazyload_iframe(self):
        url = 'http://example.com/foo/bar'
        iframe_tag = '<iframe src="{0}" />'.format(url)
        element = lxml.html.fromstring(iframe_tag)
        self.assertEqual(self.transformer._lazyload_iframe(element), url)
        self.assertNotIn('src', element.attrib)
        self.assertIn('data-src', element.attrib)
        self.assertEqual(element.attrib['data-src'], url)

    def test_lazyload_iframe_no_src(self):
        element = lxml.html.fromstring('<iframe />')
        self.assertIsNone(self.transformer._lazyload_iframe(element))

    def test_lazyload_tweet(self):
        url = 'https://twitter.com/verge/status/725096763972001794'
        html = lxml.html.fromstring(TWEET)
        element = html.getchildren()[0]
        self.assertEqual(self.transformer._lazyload_tweet(element), url)
        self.assertIn('data-twitter', element.attrib)
        self.assertEqual(len(html.getchildren()), 1)

    def test_lazyload_tweet_modified(self):
        html = lxml.html.fromstring(TWEET_MODIFIED)
        element = html.getchildren()[0]
        self.assertIsNone(self.transformer._lazyload_tweet(element))

    def test_lazyload_tweet_no_script(self):
        element = lxml.html.fromstring(TWEET_NO_SCRIPT)
        self.assertIsNone(self.transformer._lazyload_tweet(element))

    @staticmethod
    def set_css_class_blacklist(value):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILazySizesSettings)
        settings.css_class_blacklist = value

    def test_css_blacklisted_class(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()
        url = 'http://example.com/foo.png'
        klass = 'nolazyload'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], url)
        self.assertEqual(img.attrib['class'], klass)
        self.assertNotIn('data-src', img.attrib)

    def test_css_blacklisted_multiple_classes(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()
        url = 'http://example.com/foo.png'
        klass = 'nolazyload secondclass thirdclass'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], url)
        self.assertEqual(img.attrib['class'], klass)
        self.assertNotIn('data-src', img.attrib)

    def test_css_blacklisted_false_possitives(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()
        url = 'http://example.com/foo.png'
        klass = 'nolazyloadbutnot anothernolazyloadbutnot'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertIn(klass, img.attrib['class'])
        self.assertIn('lazyload', img.attrib['class'])
        self.assertEqual(img.attrib['data-src'], url)