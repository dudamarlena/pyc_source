# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unit_tests/test_GenericFile.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 2058 bytes
from __future__ import absolute_import
from builtins import str
from unittest import TestCase
from os import path, remove
from blowdrycss.filehandler import GenericFile
from blowdrycss.utilities import unittest_file_path
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class TestGenericFile(TestCase):

    def test_write_valid(self):
        sample_markdown = '# Sample Title\nThis is a paragraph.\n'
        expected_string = sample_markdown
        generic_directory = unittest_file_path('test_generic')
        file_name = 'blowdry'
        extensions = ['.md', '.rst', '.html', '.txt']
        for extension in extensions:
            generic_file = GenericFile(file_directory=generic_directory, file_name=file_name, extension=extension)
            if path.isfile(generic_file.file_path):
                remove(generic_file.file_path)
            generic_file.write(text=(str(sample_markdown)))
            with open(generic_file.file_path, 'r') as (generic_file):
                file_string = generic_file.read()
            self.assertEqual(file_string, expected_string)

    def test_write_invalid_input(self):
        invalid_inputs = [1239487.234, ['nth', 'rcghtn'], {2, 1, '&^'}, 546]
        generic_directory = unittest_file_path('test_generic')
        file_name = 'blowdry'
        extension = '.md'
        for invalid_text in invalid_inputs:
            generic_file = GenericFile(file_directory=generic_directory, file_name=file_name, extension=extension)
            self.assertRaises(TypeError, generic_file.write, invalid_text)

    def test_invalid_initialization(self):
        generic_directory = unittest_file_path('test_generic')
        file_name = 'blowdry'
        extension = '.md'
        self.assertRaises(ValueError, GenericFile, '', file_name, extension)
        self.assertRaises(ValueError, GenericFile, generic_directory, '', extension)
        self.assertRaises(ValueError, GenericFile, generic_directory, file_name, '')