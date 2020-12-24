# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/tests.py
# Compiled at: 2018-10-30 10:25:25
# Size of source mod 2**32: 2130 bytes
import os, shutil
from django.test import TestCase
from django import forms
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from redactor.widgets import RedactorEditor

class TestForm(forms.Form):
    text = forms.CharField(widget=(RedactorEditor()))


class AdminFormTestCase(TestCase):

    def test_in_form(self):
        form = TestForm()
        rendered_html = form.as_p()
        self.assertIn('$("#id_text").redactor', rendered_html)

    def test_custom_upload_parameters(self):
        widget = RedactorEditor()
        rendered = widget.render('text', 'text', attrs={'id': 'test_id'})
        self.assertIn('"fileUpload": "/upload/file/"', rendered)
        widget = RedactorEditor(redactor_options={'fileUpload': '/another_url/'})
        rendered = widget.render('text', 'text', attrs={'id': 'test_id'})
        self.assertIn('"fileUpload": "/another_url/"', rendered)

    def test_upload_view(self):
        password = 'test'
        user = User.objects.create_superuser('test', 'test@gmail.com', password)
        self.client.login(username=(user.username), password=password)
        content = 'file_content'.encode('utf-8')
        video_file = SimpleUploadedFile('file.mp4',
          content, content_type='video/mp4')
        response = self.client.post(reverse('redactor_upload_file', kwargs={'upload_to': 'file'}), {'file1': video_file})
        self.assertEqual(response.status_code, 403)
        video_file = SimpleUploadedFile('file.mp4',
          content, content_type='video/mp4')
        try:
            response = self.client.post(reverse('redactor_upload_file', kwargs={'upload_to': 'file'}), {'file': video_file})
        finally:
            shutil.rmtree(os.path.realpath('./file'))

        self.assertEqual(response.status_code, 200)