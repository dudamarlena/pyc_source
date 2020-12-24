# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_countries.py
# Compiled at: 2015-09-03 13:29:32
# Size of source mod 2**32: 1134 bytes
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from internationalflavor.countries import CountryFormField

class CountriesTestCase(SimpleTestCase):

    def test_form_field(self):
        field = CountryFormField(countries=['NL', 'BE', 'FR'])
        self.assertEqual(set([f[0] for f in field.choices]), set(['BE', 'FR', 'NL']))

    def test_form_field_render(self):
        field = CountryFormField(countries=['NL', 'CF'])
        out = '<select name="countries">\n            <option value="CF">Central African Republic</option>\n            <option value="NL" selected="selected">Netherlands</option>\n            </select>'
        self.assertHTMLEqual(field.widget.render('countries', 'NL'), out)
        with translation.override('de'):
            out = '<select name="countries">\n                <option value="NL" selected="selected">Niederlande</option>\n                <option value="CF">Zentralafrikanische Republik</option>\n                </select>'
            self.assertHTMLEqual(field.widget.render('countries', 'NL'), out)