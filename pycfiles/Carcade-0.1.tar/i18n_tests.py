# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aromanovich/carcade_dist/tests/i18n_tests.py
# Compiled at: 2013-02-27 01:42:17
import unittest, tempfile, polib
from carcade.environments import create_jinja2_env
from carcade.i18n import extract_translations

class TranslationsExtractionTest(unittest.TestCase):

    def test(self):
        jinja2_env = create_jinja2_env(layouts_dir='tests/fixtures/layouts')
        with tempfile.NamedTemporaryFile() as (pot_file):
            extract_translations(jinja2_env, pot_file.name)
            po_entries = polib.pofile(pot_file.name)
            self.assertEqual(str(po_entries[0]), '#: test.html:1\nmsgid "Static"\nmsgstr "Static"\n')
            self.assertEqual(str(po_entries[1]), '#: test.html:1 test.html:3\nmsgid "sites"\nmsgstr "sites"\n')