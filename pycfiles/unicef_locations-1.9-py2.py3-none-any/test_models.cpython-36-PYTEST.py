# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/tests/test_models.py
# Compiled at: 2018-07-11 11:07:05
# Size of source mod 2**32: 1452 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.test import SimpleTestCase
from etools.applications.locations.tests.factories import CartoDBTableFactory, GatewayTypeFactory, LocationFactory

class TestStrUnicode(SimpleTestCase):
    __doc__ = 'Ensure calling str() on model instances returns the right text.'

    def test_gateway_type(self):
        gateway_type = GatewayTypeFactory.build(name='xyz')
        self.assertEqual(str(gateway_type), 'xyz')
        gateway_type = GatewayTypeFactory.build(name='Rädda Barnen')
        self.assertEqual(str(gateway_type), 'Rädda Barnen')

    def test_location(self):
        gateway_type = GatewayTypeFactory.build(name='xyz')
        location = LocationFactory.build(gateway=gateway_type, name='Rädda Barnen', p_code='abc')
        self.assertEqual(str(location), 'Rädda Barnen (xyz PCode: abc)')
        gateway_type = GatewayTypeFactory.build(name='xyz')
        location = LocationFactory.build(gateway=gateway_type, name='Rädda Barnen', p_code='abc')
        self.assertEqual(str(location), 'Rädda Barnen (xyz PCode: abc)')

    def test_carto_db_table(self):
        carto_db_table = CartoDBTableFactory.build(table_name='Rädda Barnen')
        self.assertEqual(str(carto_db_table), 'Rädda Barnen')
        carto_db_table = CartoDBTableFactory.build(table_name='xyz')
        self.assertEqual(str(carto_db_table), 'xyz')