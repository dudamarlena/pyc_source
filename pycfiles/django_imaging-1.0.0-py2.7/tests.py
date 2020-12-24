# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imaging/tests.py
# Compiled at: 2012-06-08 08:51:22
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from imaging.models import DEFAULT_IMAGING_SETTINGS, Image
from django.core.urlresolvers import reverse
import os, stat, sys
try:
    IMAGING_SETTINGS = settings.IMAGING_SETTINGS
except:
    IMAGING_SETTINGS = DEFAULT_IMAGING_SETTINGS

PERMS = '777'

class TestImagingSetup(TestCase):

    def test_file_permissions(self):
        path = os.path.join(settings.MEDIA_ROOT, IMAGING_SETTINGS['image_dir'])
        filemode = stat.S_IMODE(os.stat(path).st_mode)
        self.assertEquals(filemode, int(PERMS, 8))


class TestAjax(TestCase):
    urls = 'imaging.urls'
    fixtures = ['users.json']

    def setUp(self):
        self.is_logged = self.client.login(username='admin', password='nimda')
        self.upload_path = os.path.join(settings.MEDIA_ROOT, IMAGING_SETTINGS['image_dir'])

    def test_image_upload(self):
        testfile_path = os.path.join(settings.STATICFILES_DIRS[0], 'imaging', 'imaging_testfile.jpg')
        testfile = open(testfile_path)
        data = {'name': 'Test Image: guilt', 
           'alt': 'Alt of guilt', 
           'title': 'Title of guilt', 
           'image': testfile}
        response = self.client.post(reverse('imaging_iframe_form'), data, follow=True)
        testfile.close()
        uploaded = Image.objects.all()[0]
        os.remove(uploaded.imaging_thumbnail.file.name)
        os.remove(uploaded.image.file.name)
        self.assertEquals(self.is_logged, True)
        self.assertEquals(response.status_code, 200)
        self.assertNotEqual(response.context['callback'], None)
        return