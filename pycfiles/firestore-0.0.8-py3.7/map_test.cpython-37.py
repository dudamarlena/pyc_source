# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/datatypes/map_test.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 2195 bytes
from unittest import TestCase
from pytest import mark
from firestore import Collection, Document, Integer, Map, String
from firestore.datatypes.map import MapSchema
from firestore.errors import ValidationError

class Mapping(MapSchema):
    name = String(required=True, default='Tiza')
    age = Integer(minimum=4)


class AltMapping(MapSchema):
    name = String(required=True)


class MapDocument(Collection):
    map = Map()


class MapDocumentMapping(Document):
    map = Map(Mapping)


class MapTest(TestCase):

    def setUp(self):
        self.md = MapDocument()
        self.mdm = MapDocumentMapping()

    def tearDown(self):
        pass

    def test_map_schema_validation(self):
        """Tests that the map schema object correctly transforms
        to a python dict in the document instance and vis a vis"""
        with self.assertRaises(ValidationError):
            self.mdm.map = {'name':'Peter', 
             'age':2}

    def test_map_schema_value_error(self):
        with self.assertRaises(ValueError):
            self.mdm.map = {'name':'Peter', 
             'age':'two'}

    def test_document_presave_with_map(self):
        mapping = Mapping()
        self.mdm.map = mapping
        self.assertEqual(self.mdm.map.name, 'Tiza')

    def test_mapschema_assignment_validation(self):
        """
        Test that validations in mapschema are invoked if
        a MapSchema object is used for assignment as opposed
        to a dict loaded into a mapschema
        """
        mapping = AltMapping()
        with self.assertRaises(ValidationError):
            self.mdm.map = mapping

    def test_map_schema_assignment(self):
        mapping = Mapping()
        mapping.name = 'Tiza'
        self.mdm.map = mapping
        self.assertEqual(self.mdm.map.name, 'Tiza')

    def test_map_in_document_instance(self):
        """Test when we create a map it get's loaded into the parent doc instance"""
        _map = {'name':'peter', 
         'age':5}
        self.md.map = _map
        self.assertEqual(self.md._data.get('map'), _map)