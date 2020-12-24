# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_timezone.py
# Compiled at: 2017-01-03 12:24:05
from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.utils import translation
from django.utils.encoding import force_text
from internationalflavor.timezone.data import get_metazone_name, CURRENT_METAZONES
from internationalflavor.timezone.forms import TimezoneFormField, MetazoneFormField

class TimezoneTestCase(SimpleTestCase):

    def test_form_field(self):
        field = TimezoneFormField(timezones=[b'Europe/Amsterdam', b'Europe/Berlin', b'America/New_York', b'Etc/GMT'])
        self.assertEqual(set([ force_text(f[0]) for f in field.choices ]), set([b'Europe', b'Americas', b'World']))
        self.assertEqual(set([ force_text(g[0]) for f in field.choices for g in f[1] ]), set([b'Europe/Amsterdam', b'Europe/Berlin', b'America/New_York', b'Etc/GMT']))

    def test_form_field_render(self):
        field = TimezoneFormField(timezones=[b'Europe/Amsterdam', b'Europe/Berlin', b'America/New_York', b'Etc/GMT', b'Indian/Christmas'])
        out = b'<select name="zones">\n            <optgroup label="Americas">\n            <option value="America/New_York">New York</option>\n            </optgroup>\n            <optgroup label="Europe">\n            <option value="Europe/Amsterdam">Amsterdam</option>\n            <option value="Europe/Berlin" selected="selected">Berlin</option>\n            </optgroup>\n            <optgroup label="World">\n            <option value="Indian/Christmas">Christmas</option>\n            <option value="Etc/GMT">GMT</option>\n            </optgroup>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render(b'zones', b'Europe/Berlin'))
        with translation.override(b'de'):
            out = b'<select name="zones">\n                <optgroup label="Amerika">\n                <option value="America/New_York">New York</option>\n                </optgroup>\n                <optgroup label="Europa">\n                <option value="Europe/Amsterdam">Amsterdam</option>\n                <option value="Europe/Berlin" selected="selected">Berlin</option>\n                </optgroup>\n                <optgroup label="Welt">\n                <option value="Etc/GMT">GMT</option>\n                <option value="Indian/Christmas">Weihnachtsinsel</option>\n                </optgroup>\n                </select>'
            self.assertHTMLEqual(out, field.widget.render(b'zones', b'Europe/Berlin'))


class MetazoneTestCase(SimpleTestCase):

    def test_get_metazone_name(self):
        self.assertEqual(get_metazone_name(b'Europe_Central', b'name'), b'Central European Time')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'name_cities'), b'Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'offset_name'), b'GMT+01:00 Central European Time')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'offset_name_cities'), b'GMT+01:00 Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'%(tzname)s'), b'Central European Time')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'%(cities)s'), b'Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'%(gmt_offset)s'), b'GMT+01:00')
        self.assertEqual(get_metazone_name(b'Europe_Central', b'%(offset)s'), b'+01:00')
        with translation.override(b'bg'):
            self.assertEqual(get_metazone_name(b'Europe_Central', b'%(gmt_offset)s'), b'Гринуич+01:00')

    def test_form_field(self):
        field = MetazoneFormField(metazones=[b'Europe_Central', b'GMT', b'Dushanbe'])
        self.assertEqual(set([ force_text(f[0]) for f in field.choices ]), set([b'Europe_Central', b'GMT', b'Dushanbe']))

    def test_form_field_render_name(self):
        field = MetazoneFormField(metazones=[b'Europe_Central', b'GMT', b'Dushanbe'], display_format=b'name')
        out = b'<select name="zones">\n            <option value="Europe_Central">Central European Time</option>\n            <option value="Dushanbe" selected="selected">Dushanbe Time</option>\n            <option value="GMT">Greenwich Mean Time</option>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render(b'zones', b'Dushanbe'))
        with translation.override(b'de'):
            out = b'<select name="zones">\n            <option value="Dushanbe" selected="selected">Duschanbe Zeit</option>\n            <option value="Europe_Central">Mitteleuropäische Zeit</option>\n            <option value="GMT">Mittlere Greenwich-Zeit</option>\n            </select>'
            self.assertHTMLEqual(out, field.widget.render(b'zones', b'Dushanbe'))

    def test_form_field_render_name_cities(self):
        field = MetazoneFormField(metazones=[b'Europe_Central', b'GMT', b'Dushanbe'], display_format=b'name_cities')
        out = b'<select name="zones">\n            <option value="Europe_Central">Central European Time (Amsterdam, Andorra, Belgrade, Berlin, Bratislava, ...)</option>\n            <option value="Dushanbe" selected="selected">Dushanbe Time (Dushanbe)</option>\n            <option value="GMT">Greenwich Mean Time (Abidjan, Accra, Bamako, Banjul, Conakry, ...)</option>\n            </select>'
        self.assertHTMLEqual(out, field.widget.render(b'zones', b'Dushanbe'))