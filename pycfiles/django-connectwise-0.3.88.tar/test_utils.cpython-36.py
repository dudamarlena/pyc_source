# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/tests/test_utils.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 2168 bytes
from django.test import TestCase
from . import mocks
from django.core.files.base import ContentFile
from djconnectwise.utils import get_hash, get_filename_extension, generate_thumbnail, generate_filename

class TestUtils(TestCase):

    def test_get_hash_returns_hash(self):
        self.assertEqual(get_hash('hello, world'.encode('utf-8')), 'b7e23ec29af22b0b4e41da31e868d57226121c84')

    def test_get_filename_extension_returns_extension(self):
        self.assertEqual(get_filename_extension('avatar.jpg'), 'jpg')
        self.assertEqual(get_filename_extension('avatar.one.jpg'), 'jpg')
        self.assertEqual(get_filename_extension('avatar me.jpg'), 'jpg')

    def test_get_filename_extension_returns_none_when_invalid(self):
        self.assertEqual(get_filename_extension('avatar'), None)
        self.assertEqual(get_filename_extension(''), None)


class TestThumbnailGeneration(TestCase):
    thumbnail_size = {'avatar':(80, 80), 
     'micro_avatar':(20, 20)}
    filename = 'AnonymousMember.png'
    extension = 'png'
    avatar = mocks.get_member_avatar()

    def test_generate_filename(self):
        expected_filename = 'AnonymousMember.png80x80.png'
        processed_filename = generate_filename(self.thumbnail_size['avatar'], self.filename, self.extension)
        self.assertEqual(expected_filename, processed_filename)

    def test_generate_avatar_thumbnail(self):
        expected_filename = 'AnonymousMember.png20x20.png'
        file, avatar = generate_thumbnail(self.avatar, self.thumbnail_size['micro_avatar'], self.extension, self.filename)
        self.assertEqual(expected_filename, avatar)
        self.assertIsInstance(file, ContentFile)