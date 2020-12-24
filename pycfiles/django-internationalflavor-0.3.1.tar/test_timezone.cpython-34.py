# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_timezone.py
# Compiled at: 2017-01-03 12:24:05
# Size of source mod 2**32: 5529 bytes
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from django.utils.encoding import force_text
from internationalflavor.timezone.data import get_metazone_name, CURRENT_METAZONES
from internationalflavor.timezone.forms import TimezoneFormField, MetazoneFormField

class TimezoneTestCase(SimpleTestCase):

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


class MetazoneTestCase(SimpleTestCase):

    def test_get_metazone_name(self):
        self.assertEqual(get_metazone_name('Europe_Central', 'name'), 'Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', 'name_cities'), 'Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name('Europe_Central', 'offset_name'), 'GMT+01:00 Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', 'offset_name_cities'), 'GMT+01:00 Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name('Europe_Central', '%(tzname)s'), 'Central European Time')
        self.assertEqual(get_metazone_name('Europe_Central', '%(cities)s'), 'Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...')
        self.assertEqual(get_metazone_name('Europe_Central', '%(gmt_offset)s'), 'GMT+01:00')
        self.assertEqual(get_metazone_name('Europe_Central', '%(offset)s'), '+01:00')
        with translation.override('bg'):
            self.assertEqual(get_metazone_name('Europe_Central', '%(gmt_offset)s'), 'Гринуич+01:00')

    def test_form_field(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'])
        self.assertEqual(set([force_text(f[0]) for f in field.choices]), set(['Europe_Central', 'GMT', 'Dushanbe']))

    def test_form_field_render_name(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'], display_format='name')
        out = '<select name="zones">\n            <option value="Europe_Central">Central European Time</option>\n            <option value="Dushanbe" selected="selected">Dushanbe Time</option>\n            <option value="GMT">Greenwich Mean Time</option>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))
        with translation.override('de'):
            out = '<select name="zones">\n            <option value="Dushanbe" selected="selected">Duschanbe Zeit</option>\n            <option value="Europe_Central">Mitteleuropäische Zeit</option>\n            <option value="GMT">Mittlere Greenwich-Zeit</option>\n            </select>'
            self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))

    def test_form_field_render_name_cities(self):
        field = MetazoneFormField(metazones=['Europe_Central', 'GMT', 'Dushanbe'], display_format='name_cities')
        out = '<select name="zones">\n            <option value="Europe_Central">Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)</option>\n            <option value="Dushanbe" selected="selected">Dushanbe Time (Dushanbe)</option>\n            <option value="GMT">Greenwich Mean Time (Abidjan, Accra, Bamako, Banjul, Conakry, ...)</option>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render('zones', 'Dushanbe'))