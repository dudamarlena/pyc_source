# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_countries.py
# Compiled at: 2016-12-31 10:36:50
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from internationalflavor.countries import CountryField
from internationalflavor.countries import CountryFormField

class CountriesFormTestCase(SimpleTestCase):

    def test_form_field(self):
        field = CountryFormField(countries=[b'NL', b'BE', b'FR'])
        self.assertEqual(set([ f[0] for f in field.choices ]), set([b'BE', b'FR', b'NL']))

    def test_form_field_render(self):
        field = CountryFormField(countries=[b'NL', b'CF'])
        out = b'<select name="countries">\n            <option value="CF">Central African Republic</option>\n            <option value="NL" selected="selected">Netherlands</option>\n            </select>'
        self.assertHTMLEqual(field.widget.render(b'countries', b'NL'), out)
        with translation.override(b'de'):
            out = b'<select name="countries">\n                <option value="NL" selected="selected">Niederlande</option>\n                <option value="CF">Zentralafrikanische Republik</option>\n                </select>'
            self.assertHTMLEqual(field.widget.render(b'countries', b'NL'), out)

    def test_model_field_deconstruct_default(self):
        test_inst = CountryField()
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = CountryField(*args, **kwargs)
        for attr in ('countries', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))

    def test_model_field_deconstruct_different(self):
        test_inst = CountryField(countries=[b'NL', b'BE'], exclude=[b'BE'])
        name, path, args, kwargs = test_inst.deconstruct()
        new_inst = CountryField(*args, **kwargs)
        for attr in ('countries', 'exclude', 'choices'):
            self.assertEqual(getattr(test_inst, attr), getattr(new_inst, attr))