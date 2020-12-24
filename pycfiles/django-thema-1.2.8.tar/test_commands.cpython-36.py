# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/tests/test_commands.py
# Compiled at: 2018-03-07 08:23:44
# Size of source mod 2**32: 4662 bytes
from django.core.management import call_command, CommandError
from django.test import TestCase
from django.utils.six import StringIO
from mock import patch
from thema.models import ThemaCategory
from thema.tests.utils import ThemaTemporaryFilesMixin

def mock_get_parent(self, code):
    raise ThemaCategory.DoesNotExist


class TestPopulateThemaCategoryCmd(ThemaTemporaryFilesMixin, TestCase):

    def test_regular_case(self):
        self.assertEqual(ThemaCategory.objects.count(), 0)
        out = StringIO()
        call_command('populate_thema_categories', stdout=out)
        self.assertEqual(ThemaCategory.objects.count(), 6748)
        output = out.getvalue()
        self.assertIn('Amount of categories created: 6748', output)
        self.assertIn('Amount of categories updated: 0', output)
        self.assertIn("The ThemaCategory table is clean and updated, you don't have obsolete categories.", output)
        for thema_code, values in self.random_codes.items():
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).header, values['en'][0])
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).parent.code, values['parent'])

    def test_regular_case_with_obsolete_categories(self):
        self.assertEqual(ThemaCategory.objects.count(), 0)
        ThemaCategory.objects.create(code='WUHU!', header='header')
        ThemaCategory.objects.create(code='OBSOLETE')
        out = StringIO()
        call_command('populate_thema_categories', stdout=out)
        output = out.getvalue()
        self.assertIn('Amount of categories created: 6748', output)
        self.assertIn('Amount of categories updated: 0', output)
        self.assertIn('There are some obsolete categories in the database', output)
        self.assertIn('WUHU!', output)
        self.assertIn('OBSOLETE', output)
        self.assertEqual(ThemaCategory.objects.count(), 6750)
        for thema_code, values in self.random_codes.items():
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).header, values['en'][0])
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).parent.code, values['parent'])

    def test_regular_case_with_updates(self):
        self.assertEqual(ThemaCategory.objects.count(), 0)
        amv = ThemaCategory.objects.create(code='AMV')
        amvd = ThemaCategory.objects.create(code='AMVD')
        out = StringIO()
        call_command('populate_thema_categories', stdout=out)
        output = out.getvalue()
        self.assertIn('Amount of categories created: 6746', output)
        self.assertIn('Amount of categories updated: 2', output)
        self.assertEqual(ThemaCategory.objects.count(), 6748)
        for thema_code, values in self.random_codes.items():
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).header, values['en'][0])
            self.assertEqual(ThemaCategory.objects.get(code=thema_code).parent.code, values['parent'])

        amv.refresh_from_db()
        amvd.refresh_from_db()
        self.assertEqual(amv.header, 'Landscape art & architecture')
        self.assertEqual(amvd.header, 'City & town planning: architectural aspects')
        self.assertEqual(amvd.parent, amv)

    @patch('thema.management.commands.populate_thema_categories.Command._get_parent', mock_get_parent)
    def test_missing_parent(self):
        self.assertRaises(CommandError, call_command, 'populate_thema_categories')