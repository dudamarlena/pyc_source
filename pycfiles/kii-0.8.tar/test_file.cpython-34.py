# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/file/tests/test_file.py
# Compiled at: 2015-01-18 14:56:47
# Size of source mod 2**32: 660 bytes
from __future__ import unicode_literals
from django.core.files.uploadedfile import SimpleUploadedFile
from kii.stream.tests.base import StreamTestCase
from .. import models

class TestFile(StreamTestCase):

    def test_file_accepts_uploaded_file(self):
        item = models.File(root=self.streams[0], title='Hello !')
        item.file_obj = SimpleUploadedFile('hello.txt', b'hello world!')
        item.save()

    def test_file_store_mimetype(self):
        item = models.File(root=self.streams[0], title='Hello !')
        item.file_obj = SimpleUploadedFile('hello.png', b'')
        item.save()
        self.assertEqual(item.mimetype, 'image/png')