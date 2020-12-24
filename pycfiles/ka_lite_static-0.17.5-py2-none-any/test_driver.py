# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/gdal/tests/test_driver.py
# Compiled at: 2018-07-11 18:15:30
import unittest
from django.contrib.gis.gdal import Driver, OGRException
valid_drivers = ('ESRI Shapefile', 'MapInfo File', 'TIGER', 'S57', 'DGN', 'Memory',
                 'CSV', 'GML', 'KML')
invalid_drivers = ('Foo baz', 'clucka', 'ESRI Shp')
aliases = {'eSrI': 'ESRI Shapefile', 'TigER/linE': 'TIGER', 
   'SHAPE': 'ESRI Shapefile', 
   'sHp': 'ESRI Shapefile'}

class DriverTest(unittest.TestCase):

    def test01_valid_driver(self):
        """Testing valid OGR Data Source Drivers."""
        for d in valid_drivers:
            dr = Driver(d)
            self.assertEqual(d, str(dr))

    def test02_invalid_driver(self):
        """Testing invalid OGR Data Source Drivers."""
        for i in invalid_drivers:
            self.assertRaises(OGRException, Driver, i)

    def test03_aliases(self):
        """Testing driver aliases."""
        for alias, full_name in aliases.items():
            dr = Driver(alias)
            self.assertEqual(full_name, str(dr))


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(DriverTest))
    return s


def run(verbosity=2):
    unittest.TextTestRunner(verbosity=verbosity).run(suite())