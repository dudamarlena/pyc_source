# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_core.py
# Compiled at: 2016-12-31 09:35:50
# Size of source mod 2**32: 2141 bytes
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.test import SimpleTestCase
from internationalflavor.forms import SortedSelect

class SortedSelectTest(SimpleTestCase):

    def test_simple_sorted_select(self):
        f = SortedSelect(choices=[(1, _('Unknown Region')), (2, 'Abuh')])
        out = '<select name="test">\n        <option value="2">Abuh</option>\n        <option value="1" selected="selected">Unknown Region</option>\n        </select>'
        self.assertHTMLEqual(out, f.render('test', '1'))

    def test_sorted_select_with_optgroups(self):
        f = SortedSelect(choices=[('B', (('a', _('Unknown Region')), (2, 'Abuh'))), ('z', 'A'), ('x', 'C')])
        out = '<select name="test">\n          <optgroup label="B">\n          <option value="2">Abuh</option>\n          <option value="a" selected="selected">Unknown Region</option>\n          </optgroup>\n          <option value="z">A</option>\n          <option value="x">C</option>\n          </select>'
        self.assertHTMLEqual(out, f.render('test', 'a'))

    def test_sorting_of_unicode_strings(self):
        import locale
        current_locale = locale.getlocale(locale.LC_COLLATE)
        try:
            new_locale = locale.setlocale(locale.LC_COLLATE, '')
            if 'UTF-8' not in new_locale:
                self.skipTest('No proper sortable context found')
            if locale.strcoll('z', 'ą') < 0:
                self.skipTest('Sortable context does not sort properly (using BSD?)')
            f = SortedSelect(choices=[('0', 'a'), ('1', 'ą'), ('2', 'z')])
            out = '<select name="test">\n            <option value="0" selected="selected">a</option>\n            <option value="1">ą</option>\n            <option value="2">z</option>\n            </select>'
            self.assertHTMLEqual(out, f.render('test', '0'))
        finally:
            locale.setlocale(locale.LC_COLLATE, current_locale)