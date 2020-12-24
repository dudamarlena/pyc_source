# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/tests/test_utils.py
# Compiled at: 2018-12-02 07:23:05
# Size of source mod 2**32: 906 bytes
from django.test import TestCase
from rolepermissions.utils import camelToSnake, snake_to_title, camel_or_snake_to_title

class UtilTests(TestCase):

    def setUp(self):
        pass

    def test_camel_to_snake(self):
        self.assertEqual(camelToSnake('camelCaseString'), 'camel_case_string')
        self.assertEqual(camelToSnake('Snake_Camel_String'), 'snake__camel__string')

    def test_snake_to_title(self):
        self.assertEqual(snake_to_title('snake_case_string'), 'Snake Case String')
        self.assertEqual(snake_to_title('Even_if__itsFunky'), 'Even If  Itsfunky')

    def test_camel_or_snake_to_title(self):
        self.assertEqual(camel_or_snake_to_title('snake_case_string'), 'Snake Case String')
        self.assertEqual(camel_or_snake_to_title('camelCaseString'), 'Camel Case String')
        self.assertEqual(camel_or_snake_to_title('mix_itUp_WhyNot'), 'Mix It Up  Why Not')