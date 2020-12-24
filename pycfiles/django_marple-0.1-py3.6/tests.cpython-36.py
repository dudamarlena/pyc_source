# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/tests.py
# Compiled at: 2018-06-30 09:17:16
# Size of source mod 2**32: 2614 bytes
import os
from django.test import TestCase
from django.core.management import call_command
from marple.management.commands.marple_update import Command
from marple.marple import Marple

class MarpleTestCase(TestCase):

    def setUp(self):
        self.m = Marple()

    def test_get_files(self):
        """
        tests/sass/
        ├── ignoreme
        │\xa0\xa0 └── _ignoreme.scss
        ├── ignorethis.css
        ├── _nocomments.scss
        ├── root.scss
        └── subdir
            ├── _all_comments.scss
            └── _malformed_comments.scss
        """
        files = self.m.get_files()
        p = 'tests/sass'
        self.assertNotIn(p + '/ignorethis.css', files)
        self.assertNotIn(p + '/ignoreme/_ignoreme.scss', files)
        self.assertEqual(len(files), 4)

    def test_guess_type_variable(self):
        x = self.m.guess_type('$l: 42;')
        self.assertEqual(x, 'variable')
        x = self.m.guess_type('  $l:42;')
        self.assertEqual(x, 'variable')
        x = self.m.guess_type('  $ l:42;')
        self.assertEqual(x, None)

    def test_guess_type_color(self):
        x = self.m.guess_type('$c: #123;')
        self.assertEqual(x, 'color')
        x = self.m.guess_type('$c: #123456;')
        self.assertEqual(x, 'color')
        x = self.m.guess_type('$c: # 123;')
        self.assertEqual(x, None)
        x = self.m.guess_type('$c: #1234;')
        self.assertEqual(x, None)
        x = self.m.guess_type('$c: #12345;')
        self.assertEqual(x, None)
        x = self.m.guess_type('$c: rgb(10, 10, 10);')
        self.assertEqual(x, 'color')
        x = self.m.guess_type('$c: rgba(10, 10, 10 .5);')
        self.assertEqual(x, None)
        x = self.m.guess_type('$c: rgba(10, 10, 10, .5);')
        self.assertEqual(x, 'color')

    def test_guess_type_mixin(self):
        x = self.m.guess_type('@mixin m{')
        self.assertEqual(x, 'mixin')
        x = self.m.guess_type('   @mixin m {')
        self.assertEqual(x, 'mixin')
        x = self.m.guess_type('@mixin m($a, $b, $c) {')
        self.assertEqual(x, 'mixin')
        x = self.m.guess_type('@ mixin m($a, $b, $c) {')
        self.assertEqual(x, None)

    def test_get_comments(self):
        files = self.m.get_files()
        content = ''
        for file in files:
            with open(file, 'r') as (f):
                content += f.read()

        comments = self.m.get_comments(content)
        self.assertEqual(len(comments), 5)
        self.assertFalse(all(['/// description: this should not be in get_comments' in x for x in comments]))