# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_core.py
# Compiled at: 2016-12-31 09:35:50
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.test import SimpleTestCase
from internationalflavor.forms import SortedSelect

class SortedSelectTest(SimpleTestCase):

    def test_simple_sorted_select(self):
        f = SortedSelect(choices=[(1, _(b'Unknown Region')), (2, 'Abuh')])
        out = b'<select name="test">\n        <option value="2">Abuh</option>\n        <option value="1" selected="selected">Unknown Region</option>\n        </select>'
        self.assertHTMLEqual(out, f.render(b'test', b'1'))

    def test_sorted_select_with_optgroups(self):
        f = SortedSelect(choices=[(b'B', ((b'a', _(b'Unknown Region')), (2, 'Abuh'))), ('z', 'A'), ('x', 'C')])
        out = b'<select name="test">\n          <optgroup label="B">\n          <option value="2">Abuh</option>\n          <option value="a" selected="selected">Unknown Region</option>\n          </optgroup>\n          <option value="z">A</option>\n          <option value="x">C</option>\n          </select>'
        self.assertHTMLEqual(out, f.render(b'test', b'a'))

    def test_sorting_of_unicode_strings(self):
        import locale
        current_locale = locale.getlocale(locale.LC_COLLATE)
        try:
            new_locale = locale.setlocale(locale.LC_COLLATE, b'')
            if b'UTF-8' not in new_locale:
                self.skipTest(b'No proper sortable context found')
            if locale.strcoll(b'z', b'ą') < 0:
                self.skipTest(b'Sortable context does not sort properly (using BSD?)')
            f = SortedSelect(choices=[('0', 'a'), ('1', 'ą'), ('2', 'z')])
            out = b'<select name="test">\n            <option value="0" selected="selected">a</option>\n            <option value="1">ą</option>\n            <option value="2">z</option>\n            </select>'
            self.assertHTMLEqual(out, f.render(b'test', b'0'))
        finally:
            locale.setlocale(locale.LC_COLLATE, current_locale)