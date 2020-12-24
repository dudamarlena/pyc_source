# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_timezone.py
# Compiled at: 2015-09-03 13:29:32
# Size of source mod 2**32: 2287 bytes
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from django.utils.encoding import force_text
from internationalflavor.timezone.forms import TimezoneFormField

class CountriesTestCase(SimpleTestCase):

    def test_form_field(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT'])
        self.assertEqual(set([force_text(f[0]) for f in field.choices]), set(['Europe', 'Americas', 'World']))
        self.assertEqual(set([force_text(g[0]) for f in field.choices for g in f[1]]), set(['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT']))

    def test_form_field_render(self):
        field = TimezoneFormField(timezones=['Europe/Amsterdam', 'Europe/Berlin', 'America/New_York', 'Etc/GMT', 'Indian/Christmas'])
        out = '<select name="zones">\n            <optgroup label="Americas">\n            <option value="America/New_York">New York</option>\n            </optgroup>\n            <optgroup label="Europe">\n            <option value="Europe/Amsterdam">Amsterdam</option>\n            <option value="Europe/Berlin" selected="selected">Berlin</option>\n            </optgroup>\n            <optgroup label="World">\n            <option value="Indian/Christmas">Christmas</option>\n            <option value="Etc/GMT">GMT</option>\n            </optgroup>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render('zones', 'Europe/Berlin'))
        with translation.override('de'):
            out = '<select name="zones">\n                <optgroup label="Amerika">\n                <option value="America/New_York">New York</option>\n                </optgroup>\n                <optgroup label="Europa">\n                <option value="Europe/Amsterdam">Amsterdam</option>\n                <option value="Europe/Berlin" selected="selected">Berlin</option>\n                </optgroup>\n                <optgroup label="Welt">\n                <option value="Etc/GMT">GMT</option>\n                <option value="Indian/Christmas">Weihnachtsinsel</option>\n                </optgroup>\n                </select>'
            self.assertHTMLEqual(out, field.widget.render('zones', 'Europe/Berlin'))