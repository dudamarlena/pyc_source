# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_photos/test_forms.py
# Compiled at: 2013-07-03 05:00:55
from django.contrib.sites.models import Site
from ella.photos.admin import FormatForm
from nose import tools
from test_ella.cases import RedisTestCase as TestCase
from test_ella.test_photos.fixtures import create_photo_formats

class TestFormatForm(TestCase):

    def setUp(self):
        super(TestFormatForm, self).setUp()
        create_photo_formats(self)
        self.other_site = Site.objects.create(name='other', domain='other.com')
        self.data = dict(name='basic', max_width=20, max_height=20, flexible_height=False, stretch=False, nocrop=False, resample_quality=85, sites=[])

    def test_same_name_formats_allowed_if_in_different_sites(self):
        self.data['sites'] = [
         self.other_site.pk]
        form = FormatForm(self.data)
        tools.assert_true(form.is_valid())

    def test_same_name_not_allowed_on_same_site(self):
        self.data['sites'] = [
         self.other_site.pk, Site.objects.get_current().pk]
        form = FormatForm(self.data)
        tools.assert_false(form.is_valid())