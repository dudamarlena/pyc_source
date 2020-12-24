# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_tagsync.py
# Compiled at: 2019-05-23 11:08:11
import unittest
from policytool import tagsync
from policytool.atlas import AtlasError
from mock import MagicMock

class TestTagsyncModuleGlobal(unittest.TestCase):

    def test_strip_qualified_name(self):
        self.assertEqual(tagsync.strip_qualified_name('foo@bar'), 'foo')

    def test_tags_from_src(self):
        test_data = [{'tags': 'tag1'}, {'tags': 'tag1,tag2,tag3'}]
        self.assertEqual(tagsync.tags_from_src(test_data), set(['tag1', 'tag2', 'tag3']))

    def test__tags_as_set(self):
        test_data = {'tags': 'tag1,tag2'}
        self.assertEqual(tagsync._tags_as_set(test_data), {'tag1', 'tag2'})

    def test__tags_as_set_no_tags(self):
        test_data = {'tags': ''}
        self.assertEqual(tagsync._tags_as_set(test_data), set())

    def test__tags_as_set_with_extra_comma(self):
        test_data = {'tags': 'tag1,tag2,'}
        self.assertEqual(tagsync._tags_as_set(test_data), {'tag1', 'tag2'})


class TestSync(unittest.TestCase):

    def setUp(self):
        self.atlas_client = type('atlas_client', (), {})()
        self.hive_client = type('hive_client', (), {})()
        self.to_test = tagsync.Sync(self.atlas_client, retries=2, retry_delay=1, hive_client=self.hive_client)

    def test_sync_table_tags_expect_tags_added_to_one_table(self):
        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': [
                                  'tag']},
         {'status': 'ACTIVE', 'guid': 'UUID2', 
            'typeName': 'hive_table', 
            'displayText': 'table2', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table2@dhadoopname', 
                           'name': 'table2', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.add_tags_on_guid = lambda guid, tags: added_tags.append((guid, tags))
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'tags': 'tag'},
         {'schema': 'test_schema', 'table': 'table2', 
            'tags': 'tag'}]
        result = self.to_test.sync_table_tags(test_data)
        self.assertEqual([('UUID2', ['tag'])], added_tags)
        self.assertEqual({'run:1 test_schema.table2 added tag': set(['tag'])}, result)

    def test_sync_table_tags_expect_tags_added_to_no_table(self):
        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': [
                                  'tag']}]
        self.atlas_client.add_tags_on_guid = lambda guid, tags: added_tags.append((guid, tags))
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'tags': 'tag'}]
        result = self.to_test.sync_table_tags(test_data)
        self.assertEqual([], added_tags)
        self.assertEqual({}, result)

    def test_sync_table_tags_expect_table_missing_in_atlas(self):
        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: []
        self.atlas_client.add_tags_on_guid = lambda guid, tags: added_tags.append((guid, tags))
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'tags': 'tag'}]
        with self.assertRaises(tagsync.SyncError) as (e):
            self.to_test.sync_table_tags(test_data)
        self.assertEqual('run:3 The table(s) test_schema.table1 does not exist in Atlas.', e.exception.message)

    def test_sync_table_tags_expect_table_guid_exist_third_run(self):
        runs = []

        def add_tags_on_guid(guid, tags):
            runs.append(1)
            if len(runs) > 2:
                added_tags.append((guid, tags))
            else:
                raise AtlasError('I am a teapot', 418)

        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.add_tags_on_guid = add_tags_on_guid
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'tags': 'tag'}]
        result = self.to_test.sync_table_tags(test_data)
        self.assertEqual([('UUID1', ['tag'])], added_tags)
        self.assertEqual({'run:3 test_schema.table1 added tag': set(['tag'])}, result)
        self.assertEqual(3, len(runs))

    def test_sync_column_tags_expect_tags_added_to_one_column(self):
        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.get_columns = lambda db, table: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_column', 
            'displayText': 'column1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.' + table + '.column1@dhadoopname', 
                           'name': 'column1', 
                           'description': None}, 
            'classificationNames': [
                                  'tag']},
         {'status': 'ACTIVE', 'guid': 'UUID2', 
            'typeName': 'hive_column', 
            'displayText': 'column2', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.' + table + '.column2@dhadoopname', 
                           'name': 'column2', 
                           'description': None}, 
            'classificationNames': []},
         {'status': 'ACTIVE', 'guid': 'UUID2', 
            'typeName': 'hive_column', 
            'displayText': 'column3', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.' + table + '.column3@dhadoopname', 
                           'name': 'column3', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.add_tags_on_guid = lambda guid, tags: added_tags.append((guid, tags))
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'attribute': 'column1', 
            'tags': 'tag'},
         {'schema': 'test_schema', 'table': 'table1', 
            'attribute': 'column2', 
            'tags': 'tag'}]
        result = self.to_test.sync_column_tags(test_data)
        self.assertEqual([('UUID2', ['tag'])], added_tags)
        self.assertEqual({'run:1 columns not existing in tags file': set(['test_schema.table1.column3']), 'run:1 test_schema.table1.column2 added tag': set(['tag'])}, result)

    def test_sync_table_tags_expect_column_missing_in_atlas(self):
        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.get_columns = lambda db, table: []
        self.atlas_client.add_tags_on_guid = lambda guid, tags: added_tags.append((guid, tags))
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'attribute': 'column1', 
            'tags': 'tag'}]
        with self.assertRaises(tagsync.SyncError) as (e):
            self.to_test.sync_column_tags(test_data)
        self.assertEqual('run:3 The column(s) test_schema.table1.column1 does not exist in Atlas.', e.exception.message)

    def test_sync_column_tags_expect_column_guid_exist_third_run(self):
        runs = []

        def add_tags_on_guid(guid, tags):
            runs.append(1)
            if len(runs) > 2:
                added_tags.append((guid, tags))
            else:
                raise AtlasError('I am a teapot', 418)

        added_tags = []
        self.atlas_client.known_tags = lambda : [{'name': 'tag'}]
        self.atlas_client.get_tables = lambda db: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_table', 
            'displayText': 'table1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.table1@dhadoopname', 
                           'name': 'table1', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.get_columns = lambda db, table: [
         {'status': 'ACTIVE', 'guid': 'UUID1', 
            'typeName': 'hive_column', 
            'displayText': 'column1', 
            'attributes': {'owner': 'owner', 
                           'qualifiedName': db + '.' + table + '.column1@dhadoopname', 
                           'name': 'column1', 
                           'description': None}, 
            'classificationNames': []}]
        self.atlas_client.add_tags_on_guid = add_tags_on_guid
        test_data = [
         {'schema': 'test_schema', 'table': 'table1', 
            'attribute': 'column1', 
            'tags': 'tag'}]
        result = self.to_test.sync_column_tags(test_data)
        self.assertEqual([('UUID1', ['tag'])], added_tags)
        self.assertEqual({'run:3 test_schema.table1.column1 added tag': set(['tag'])}, result)
        self.assertEqual(3, len(runs))

    def test_sync_tags_for_one_tables_storage(self):
        self.to_test.hive_client.get_location = MagicMock(return_value='hdfs://system/my/path')
        self.to_test.atlas_client.add_hdfs_path = MagicMock(return_value='12345')
        self.to_test.atlas_client.get_tags_on_guid = MagicMock(return_value=set(['tag1', 'tag4']))
        self.to_test.atlas_client.add_tags_on_guid = MagicMock()
        self.to_test.atlas_client.delete_tags_on_guid = MagicMock()
        self.to_test._sync_tags_for_one_tables_storage('myschema', 'mytable', set(['tag1', 'tag2']))
        self.hive_client.get_location.assert_called_with('myschema', 'mytable')
        self.atlas_client.add_hdfs_path.assert_called_with('hdfs://system/my/path')
        self.atlas_client.get_tags_on_guid('12345')
        self.atlas_client.add_tags_on_guid('12345', ['tag2'])
        self.atlas_client.delete_tags_on_guid('12345', ['tag4'])

    def test_ensure_tags_in_atlas_add_new_tags(self):
        saved_tags = set()

        def add_tag_definitions_mock(tags):
            saved_tags.update(tags)

        in_data = [{'tags': 'tag1'}, {'tags': 'tag1,tag2,tag3'}]
        self.atlas_client.add_tag_definitions = add_tag_definitions_mock
        self.to_test.tags_from_atlas = MagicMock(return_value={'tag1', 'tag3'})
        self.to_test.ensure_tags_in_atlas(in_data)
        self.assertEqual(saved_tags, {'tag2'})


if __name__ == '__main__':
    unittest.main()