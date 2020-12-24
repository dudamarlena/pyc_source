# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/file_handling/test_configure_geometry.py
# Compiled at: 2019-10-03 13:30:51
import unittest
from total_scattering.file_handling.load import configure_geometry, add_required_shape_keys

class TestConfigureGeometry(unittest.TestCase):
    cylinder = {'Shape': 'Cylinder', 
       'Height': 1.8, 
       'Radius': 0.3, 
       'Center': [
                0.0, 0.0, 0.0]}
    hollow_cylinder = {'Shape': 'HollowCylinder', 
       'Height': 1.8, 
       'InnerRadius': 0.3, 
       'OuterRadius': 0.4, 
       'Center': [
                0.0, 0.0, 0.0]}
    flat_plate = {'Shape': 'FlatPlate', 
       'Width': 0.3, 
       'Height': 0.3, 
       'Thick': 0.01, 
       'Center': [
                0.0, 0.0, 0.0], 
       'Angle': 90.0}

    def setUp(self):
        pass

    def test_util_add_required_shape_keys(self):
        geo = self.cylinder.copy()
        geo.pop('Radius')
        newGeo = add_required_shape_keys(geo, 'Cylinder')
        self.assertEqual(newGeo.keys(), self.cylinder.keys())

    def test_cylinder_basic(self):
        newGeo = configure_geometry(self.cylinder.copy())
        self.assertEqual(newGeo, self.cylinder)

    def test_cylinder_shape_name(self):
        geo = self.cylinder.copy()
        geo['Shape'] = 'cylinder'
        newGeo = configure_geometry(geo)
        self.assertEqual(newGeo, self.cylinder)

    def test_cylinder_on_radius2(self):
        geo = self.cylinder.copy()
        geo['Radius2'] = 5.555
        newGeo = configure_geometry(geo)
        self.assertEqual(newGeo, self.cylinder)

    def test_hollow_cylinder_basic(self):
        newGeo = configure_geometry(self.hollow_cylinder.copy())
        self.assertEqual(newGeo, self.hollow_cylinder)

    def test_hollow_cylinder_shape_name(self):
        geo = self.hollow_cylinder.copy()
        geo['Shape'] = 'Hollow Cylinder'
        newGeo = configure_geometry(geo)
        self.assertEqual(newGeo, self.hollow_cylinder)

    def test_hollow_cylinder_on_radius_and_radius2(self):
        geo = {'Shape': 'HollowCylinder', 'Radius2': 0.3, 
           'Radius': 0.4, 
           'Height': 1.8, 
           'Center': [
                    0.0, 0.0, 0.0]}
        newGeo = configure_geometry(geo)
        self.assertEqual(newGeo, self.hollow_cylinder)

    def test_flat_plate_basic(self):
        newGeo = configure_geometry(self.flat_plate.copy())
        self.assertEqual(newGeo, self.flat_plate)

    def test_flat_plate_shape_name(self):
        geo = self.flat_plate.copy()
        geo['Shape'] = 'Flat Plate'
        newGeo = configure_geometry(geo)
        self.assertEqual(newGeo, self.flat_plate)


if __name__ == '__main__':
    unittest.main()