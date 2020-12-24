# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/tests/test_spatialrefsys.py
# Compiled at: 2018-07-11 18:15:30
from django.db import connection
from django.contrib.gis.gdal import HAS_GDAL
from django.contrib.gis.tests.utils import no_mysql, oracle, postgis, spatialite, HAS_SPATIALREFSYS, SpatialRefSys
from django.utils import unittest
test_srs = (
 {'srid': 4326, 'auth_name': (
                'EPSG', True), 
    'auth_srid': 4326, 
    'srtext': 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84"', 
    'proj4': [
            '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ',
            '+proj=longlat +datum=WGS84 +no_defs '], 
    'spheroid': 'WGS 84', 
    'name': 'WGS 84', 'geographic': True, 
    'projected': False, 'spatialite': True, 'ellipsoid': (6378137.0, 6356752.3, 298.257223563), 
    'eprec': (1, 1, 9)},
 {'srid': 32140, 'auth_name': (
                'EPSG', False), 
    'auth_srid': 32140, 
    'srtext': 'PROJCS["NAD83 / Texas South Central",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980"', 
    'proj4': [
            '+proj=lcc +lat_1=30.28333333333333 +lat_2=28.38333333333333 +lat_0=27.83333333333333 +lon_0=-99 +x_0=600000 +y_0=4000000 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ',
            '+proj=lcc +lat_1=30.28333333333333 +lat_2=28.38333333333333 +lat_0=27.83333333333333 +lon_0=-99 +x_0=600000 +y_0=4000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs '], 
    'spheroid': 'GRS 1980', 
    'name': 'NAD83 / Texas South Central', 'geographic': False, 
    'projected': True, 'spatialite': False, 'ellipsoid': (6378137.0, 6356752.31414, 298.257222101), 
    'eprec': (1, 5, 10)})

@unittest.skipUnless(HAS_GDAL and HAS_SPATIALREFSYS, 'SpatialRefSysTest needs gdal support and a spatial database')
class SpatialRefSysTest(unittest.TestCase):

    @no_mysql
    def test01_retrieve(self):
        """Testing retrieval of SpatialRefSys model objects."""
        for sd in test_srs:
            srs = SpatialRefSys.objects.get(srid=sd['srid'])
            self.assertEqual(sd['srid'], srs.srid)
            auth_name, oracle_flag = sd['auth_name']
            if postgis or oracle and oracle_flag:
                self.assertEqual(True, srs.auth_name.startswith(auth_name))
            self.assertEqual(sd['auth_srid'], srs.auth_srid)
            if postgis:
                self.assertTrue(srs.wkt.startswith(sd['srtext']))
                self.assertTrue(srs.proj4text in sd['proj4'])

    @no_mysql
    def test02_osr(self):
        """Testing getting OSR objects from SpatialRefSys model objects."""
        for sd in test_srs:
            sr = SpatialRefSys.objects.get(srid=sd['srid'])
            self.assertEqual(True, sr.spheroid.startswith(sd['spheroid']))
            self.assertEqual(sd['geographic'], sr.geographic)
            self.assertEqual(sd['projected'], sr.projected)
            if not (spatialite and not sd['spatialite']):
                self.assertEqual(True, sr.name.startswith(sd['name']))
            if postgis or spatialite:
                srs = sr.srs
                self.assertTrue(srs.proj4 in sd['proj4'])
                if not spatialite:
                    self.assertTrue(srs.wkt.startswith(sd['srtext']))

    @no_mysql
    def test03_ellipsoid(self):
        """Testing the ellipsoid property."""
        for sd in test_srs:
            ellps1 = sd['ellipsoid']
            prec = sd['eprec']
            srs = SpatialRefSys.objects.get(srid=sd['srid'])
            ellps2 = srs.ellipsoid
            for i in range(3):
                param1 = ellps1[i]
                param2 = ellps2[i]
                self.assertAlmostEqual(ellps1[i], ellps2[i], prec[i])


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(SpatialRefSysTest))
    return s


def run(verbosity=2):
    unittest.TextTestRunner(verbosity=verbosity).run(suite())