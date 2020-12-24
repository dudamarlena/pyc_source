# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cities_tiny/tests.py
# Compiled at: 2012-03-14 13:44:03
import unittest
from django.core import management
from cities_tiny.models import Country, AdminDivision, City

class RefreshCommandTestCase(unittest.TestCase):

    def test_command(self):
        management.call_command('citiestinyrefresh', verbosity=2, force_import_all=True, force_all=False, force_import=[], force=[])
        self.assertEqual(Country.objects.count() > 0, True)
        self.assertEqual(AdminDivision.objects.count() > 0, True)
        self.assertEqual(City.objects.count() > 0, True)