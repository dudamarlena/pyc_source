# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/downloader/tests.py
# Compiled at: 2010-04-27 13:28:02
"""Unit tests for emencia.django.downloader"""
import base64, shutil
from django.test import TestCase
from django.core.files import File
from django.core.urlresolvers import reverse
from django.core import mail
from emencia.django.downloader.models import Download

class DownloadsTest(TestCase):
    """
    Tests for emencia.django.downloader application
    """

    def tearDown(self):
        try:
            shutil.rmtree('tests/private')
        except OSError:
            pass

    def test_create_download(self):
        """
        create some downloads
        """
        data = {'file': File(open('tests/test.txt'), 'test.txt')}
        download1 = Download.objects.create(**data)
        data = {'file': File(open('tests/test.txt'), 'test.txt'), 'password': 'mysecret'}
        download2 = Download.objects.create(**data)
        self.assertNotEqual(download1.slug, download2.slug)
        data = {'file': File(open('tests/test.txt'), 'test.txt'), 'slug': 'my_slug_for_test_file'}
        download3 = Download.objects.create(**data)
        self.assertEqual(download3.slug, 'my_slug_for_test_file')

    def test_get_file(self):
        """
        test to get the files
        """
        data = {'file': File(open('tests/test.txt'), 'test.txt')}
        download1 = Download.objects.create(**data)
        data = {'file': File(open('tests/test.txt'), 'test.txt'), 'password': 'mysecret'}
        download2 = Download.objects.create(**data)
        response = self.client.get(reverse('get_file', args=[download1.slug]))
        self.assertContains(response, 'test\n')
        self.assertEquals(response['content-type'], 'text/plain')
        response = self.client.get(reverse('get_file', args=[download2.slug]))
        self.failUnlessEqual(response.status_code, 401)
        response = self.client.get(reverse('get_file', args=[download2.slug]), **{'HTTP_AUTHORIZATION': 'Basic %s' % base64.b64encode(':%s' % download2.password)})
        self.assertContains(response, 'test\n')
        self.assertEquals(response['content-type'], 'text/plain')

    def test_upload_view(self):
        """
        test the upload view
        """
        response = self.client.get(reverse('upload'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'downloader/upload.html')

    def test_create_download_by_view(self):
        """
        test the upload view
        """
        response = self.client.post(reverse('upload'))
        self.assertContains(response, 'This field is required.', 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'downloader/upload.html')
        self.assertFormError(response, 'form', 'file', 'This field is required.')
        file = open('tests/test.txt')
        data = {'file': file}
        response = self.client.post(reverse('upload'), data=data)
        file.close()
        self.assertEqual(response.status_code, 302)
        download = list(Download.objects.all())[(-1)]
        self.assertRedirects(response, reverse('upload_ok', args=[download.slug]), target_status_code=200)
        file = open('tests/test.txt')
        data = {'file': file, 'my_mail': 'lafaye@emencia.com', 
           'notify1': 'contact@emencia.com', 
           'notify2': 'contact2@emencia.com', 
           'notify3': 'contact3@emencia.com'}
        response = self.client.post(reverse('upload'), data=data)
        file.close()
        download = list(Download.objects.all())[(-1)]
        self.assertEquals(len(mail.outbox), 2)
        self.assertEquals(mail.outbox[0].subject, "Confirmation de notification d'envoi de fichier via testserver")
        self.assertEquals(mail.outbox[1].subject, "Notification d'envoi de fichier via testserver")
        self.assert_('lafaye@emencia.com' in mail.outbox[0].to)
        self.assert_('contact@emencia.com' in mail.outbox[1].to)
        self.assert_('contact2@emencia.com' in mail.outbox[1].to)
        self.assert_('contact3@emencia.com' in mail.outbox[1].to)
        url = 'http://testserver/%s' % download.slug
        self.assert_(url in mail.outbox[0].body)
        self.assert_(url in mail.outbox[1].body)