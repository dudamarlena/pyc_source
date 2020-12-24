# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idgb/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_subscribers.py
# Compiled at: 2017-10-25 13:43:42
__doc__ = 'Tests for audio subscribers.'
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
import unittest

class AudioSubscribersTestCase(unittest.TestCase):
    """Test an Audio can hold only up to one file of each format."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.audio = api.content.create(self.portal, 'Audio', 'audio')
        api.content.create(self.audio, 'MPEG Audio File', 'foo')
        api.content.create(self.audio, 'OGG Audio File', 'bar')

    def test_object_added(self):
        from AccessControl import Unauthorized
        with self.assertRaises(Unauthorized):
            api.content.create(self.audio, 'MPEG Audio File', 'baz')
        with self.assertRaises(Unauthorized):
            api.content.create(self.audio, 'OGG Audio File', 'qux')

    def test_object_removed(self):
        api.content.delete(self.audio['foo'])
        api.content.create(self.audio, 'MPEG Audio File', 'baz')
        self.assertIn('baz', self.audio)
        api.content.delete(self.audio['bar'])
        api.content.create(self.audio, 'OGG Audio File', 'qux')
        self.assertIn('qux', self.audio)