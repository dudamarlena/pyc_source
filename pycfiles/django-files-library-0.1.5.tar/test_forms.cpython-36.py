# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/tests/test_forms.py
# Compiled at: 2018-02-10 08:54:43
# Size of source mod 2**32: 800 bytes
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django_files_library.forms import FileForm

class LibraryFormsTestCase(TestCase):

    def test_FileForm_valid(self):
        mock_file = SimpleUploadedFile('best_file_eva.txt', b'these are the file contents!')
        form = FileForm(data={'name':'test',  'description':'test desc',  'uploaded_file':mock_file}, files={'uploaded_file': mock_file})
        self.assertTrue(form.is_valid())

    def test_FileForm_invalid(self):
        form = FileForm(data={'name':'test', 
         'description':'test desc',  'first_name':'user',  'uploaded_file':None})
        self.assertFalse(form.is_valid())