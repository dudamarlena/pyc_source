# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/dev/python/piep/test/test_env.py
# Compiled at: 2019-01-10 05:59:14
# Size of source mod 2**32: 697 bytes
from .test_helper import run, temp_cwd
from unittest import TestCase
import subprocess

class TestModuleImporting(TestCase):

    def test_modules_are_not_importable_from_cwd_by_default(self):
        with temp_cwd():
            with open('mymod.py', 'w') as (f):
                f.write('def up(s): return s.upper()')
            self.assertRaises(ImportError, lambda : run('-m', 'mymod', 'mymod.up(p)', ['a']))

    def test_modules_can_be_imported_from_cwd(self):
        with temp_cwd():
            with open('mymod.py', 'w') as (f):
                f.write('def up(s): return s.upper()')
            self.assertEqual(run('-p', '.', '-m', 'mymod', 'mymod.up(p)', ['a']), ['A'])