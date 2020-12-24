# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/tests/test_geoforms.py
# Compiled at: 2018-07-11 18:15:30
from django.forms import ValidationError
from django.contrib.gis.gdal import HAS_GDAL
from django.contrib.gis.tests.utils import HAS_SPATIALREFSYS
from django.utils import unittest
if HAS_SPATIALREFSYS:
    from django.contrib.gis import forms
    from django.contrib.gis.geos import GEOSGeometry

@unittest.skipUnless(HAS_GDAL and HAS_SPATIALREFSYS, 'GeometryFieldTest needs gdal support and a spatial database')
class GeometryFieldTest(unittest.TestCase):

    def test00_init(self):
        """Testing GeometryField initialization with defaults."""
        fld = forms.GeometryField()
        for bad_default in ('blah', 3, 'FoO', None, 0):
            self.assertRaises(ValidationError, fld.clean, bad_default)

        return

    def test01_srid(self):
        """Testing GeometryField with a SRID set."""
        fld = forms.GeometryField(srid=4326)
        geom = fld.clean('POINT(5 23)')
        self.assertEqual(4326, geom.srid)
        fld = forms.GeometryField(srid=32140)
        tol = 1e-07
        xform_geom = GEOSGeometry('POINT (951640.547328465 4219369.26171664)', srid=32140)
        cleaned_geom = fld.clean('SRID=4326;POINT (-95.363151 29.763374)')
        self.assertTrue(xform_geom.equals_exact(cleaned_geom, tol))

    def test02_null(self):
        """Testing GeometryField's handling of null (None) geometries."""
        fld = forms.GeometryField()
        self.assertRaises(forms.ValidationError, fld.clean, None)
        fld = forms.GeometryField(required=False, null=False)
        self.assertRaises(forms.ValidationError, fld.clean, None)
        fld = forms.GeometryField(required=False)
        self.assertEqual(None, fld.clean(None))
        return

    def test03_geom_type(self):
        """Testing GeometryField's handling of different geometry types."""
        fld = forms.GeometryField()
        for wkt in ('POINT(5 23)', 'MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)))', 'LINESTRING(0 0, 1 1)'):
            self.assertEqual(GEOSGeometry(wkt), fld.clean(wkt))

        pnt_fld = forms.GeometryField(geom_type='POINT')
        self.assertEqual(GEOSGeometry('POINT(5 23)'), pnt_fld.clean('POINT(5 23)'))
        self.assertEqual(GEOSGeometry('LINESTRING(0 0, 1 1)'), pnt_fld.to_python('LINESTRING(0 0, 1 1)'))
        self.assertRaises(forms.ValidationError, pnt_fld.clean, 'LINESTRING(0 0, 1 1)')

    def test04_to_python(self):
        """
        Testing to_python returns a correct GEOSGeometry object or
        a ValidationError
        """
        fld = forms.GeometryField()
        for wkt in ('POINT(5 23)', 'MULTIPOLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)))', 'LINESTRING(0 0, 1 1)'):
            self.assertEqual(GEOSGeometry(wkt), fld.to_python(wkt))

        for wkt in ('POINT(5)', 'MULTI   POLYGON(((0 0, 0 1, 1 1, 1 0, 0 0)))', 'BLAH(0 0, 1 1)'):
            self.assertRaises(forms.ValidationError, fld.to_python, wkt)


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(GeometryFieldTest))
    return s


def run(verbosity=2):
    unittest.TextTestRunner(verbosity=verbosity).run(suite())


if __name__ == '__main__':
    run()