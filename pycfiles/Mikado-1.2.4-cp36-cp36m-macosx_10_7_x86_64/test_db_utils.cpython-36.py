# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/venturil/workspace/mikado/Mikado/tests/test_db_utils.py
# Compiled at: 2018-05-23 17:14:36
# Size of source mod 2**32: 5692 bytes
"""
TestCase to test the DButils module
"""
import os, unittest, Mikado.utilities.dbutils, Mikado.configuration.configurator, Mikado.serializers, sqlalchemy, sqlalchemy.orm.session, sqlalchemy.engine.base, sqlite3, Mikado.serializers.junction, Mikado.serializers.blast_serializer, Mikado.serializers.orf, shutil, pkg_resources
__author__ = 'Luca Venturini'

class TestDbConnect(unittest.TestCase):

    def setUp(self):
        self.json = Mikado.configuration.configurator.to_json(os.path.join(os.path.dirname(__file__), 'configuration.yaml'))
        self.json['db_settings']['db'] = pkg_resources.resource_filename('Mikado.tests', 'mikado.db')

    def test_connector(self):
        connector = Mikado.utilities.dbutils.create_connector(self.json)
        self.assertIsInstance(connector, sqlite3.Connection)

    def test_engine(self):
        engine = Mikado.utilities.dbutils.connect(self.json)
        self.assertIsInstance(engine, sqlalchemy.engine.base.Engine)
        table_names = ['chrom', 'hit', 'orf', 'external',
         'external_sources', 'hsp', 'junctions', 'query', 'target']
        self.assertEqual(sorted(list(engine.table_names())), sorted(table_names))

    def test_content(self):
        engine = Mikado.utilities.dbutils.connect(self.json)
        sessionmaker = sqlalchemy.orm.sessionmaker(bind=engine)
        session = sessionmaker()
        self.assertEqual(session.query(Mikado.serializers.junction.Junction).count(), 371, self.json['db_settings'])
        self.assertEqual(session.query(Mikado.serializers.orf.Orf).count(), 80)
        self.assertEqual(session.query(Mikado.serializers.blast_serializer.Target).count(), 38909)
        self.assertEqual(session.query(Mikado.serializers.blast_serializer.Query).count(), 93)
        self.assertEqual(session.query(Mikado.serializers.blast_serializer.Hit).count(), 344)
        self.assertEqual(session.query(Mikado.serializers.blast_serializer.Hsp).count(), 410)
        first_query = session.query(Mikado.serializers.blast_serializer.Query).limit(1).one()
        astup = first_query.as_tuple()
        self.assertTrue(astup._fields, ('query_id', 'query_name', 'query_length'))
        self.assertIsInstance(astup.query_id, int)
        self.assertIsInstance(astup.query_length, int)
        self.assertIsInstance(astup.query_name, str)
        first_target = session.query(Mikado.serializers.blast_serializer.Target).limit(1).one()
        astup = first_target.as_tuple()
        self.assertTrue(astup._fields, ('target_id', 'target_name', 'target_length'))
        self.assertIsInstance(astup.target_id, int)
        self.assertIsInstance(astup.target_length, int)
        self.assertIsInstance(astup.target_name, str)

    def test_query_init(self):
        _ = Mikado.serializers.blast_serializer.Query('foo', 1000)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Query(100, 1000)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Query('foo', 0)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Query('foo', -10)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Query('foo', 1000.0)

    def test_target_init(self):
        _ = Mikado.serializers.blast_serializer.Target('foo', 1000)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Target(100, 1000)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Target('foo', 0)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Target('foo', -10)
        with self.assertRaises(TypeError):
            _ = Mikado.serializers.blast_serializer.Target('foo', 1000.0)

    def test_wrong_db(self):
        self.json['db_settings']['dbtype'] = 'sqlite_foo'
        with self.assertRaises(ValueError):
            _ = Mikado.utilities.dbutils.create_connector(self.json)

    @unittest.skipUnless(os.path.exists('/dev/shm'), '/dev/shm is not available on this system.')
    def test_connect_to_shm(self):
        self.json['pick']['run_options']['shm'] = True
        shutil.copy(self.json['db_settings']['db'], '/dev/shm/')
        self.json['pick']['run_options']['shm_db'] = os.path.join('/dev/shm/', self.json['db_settings']['db'])
        connector = Mikado.utilities.dbutils.connect(self.json)
        self.assertEqual(str(connector.url), 'sqlite://')
        engine = Mikado.utilities.dbutils.connect(self.json)
        sessionmaker = sqlalchemy.orm.sessionmaker(bind=engine)
        session = sessionmaker()
        first_target = session.query(Mikado.serializers.blast_serializer.Target).limit(1).one()
        astup = first_target.as_tuple()
        self.assertTrue(astup._fields, ('target_id', 'target_name', 'target_length'))

    def test_to_memory(self):
        connector = Mikado.utilities.dbutils.connect(None)
        self.assertEqual(str(connector.url), 'sqlite:///:memory:')


if __name__ == '__main__':
    unittest.main()