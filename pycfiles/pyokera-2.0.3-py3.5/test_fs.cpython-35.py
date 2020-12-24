# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_fs.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 8840 bytes
import unittest
from okera import context, _thrift_api
from okera.tests import pycerebro_test_common as common

class FsTest(unittest.TestCase):

    def test_ls(self):
        planner = common.get_planner()
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/')
        self.assertEqual([
         's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample')
        self.assertEqual([
         's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual([
         's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt2')
        self.assertEqual([], result)
        planner.close()

    def test_cat(self):
        planner = common.get_planner()
        result = planner.cat('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual('This is a sample test file.\nIt should consist of two lines.', result)
        planner.close()

    def test_errors(self):
        planner = common.get_planner()
        with self.assertRaises(ValueError):
            planner.cat('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/not-a-file')
        planner.close()

    def test_as_testuser(self):
        ctx = context()
        ctx.enable_token_auth(token_str='testuser')
        planner = ctx.connect()
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/')
        self.assertEqual([
         's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual([
         's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'], result)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt2')
        self.assertEqual([], result)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException, 'does not have access'):
            result = planner.ls('s3://cerebro-datasets/nytaxi-data/')


class RegisteredTest(unittest.TestCase):

    def test_basic(self):
        planner = common.get_planner()
        result = planner.get_catalog_objects_at('file:/opt/data/users')
        self.assertTrue('file:/opt/data/users' in result)
        self.assertTrue('okera_sample.users' in result['file:/opt/data/users'])
        self.assertTrue('cerebro_sample.users' in result['file:/opt/data/users'])
        result = planner.get_catalog_objects_at('file:/opt/data/')
        self.assertTrue('file:/opt/data/sample' in result)
        self.assertTrue('file:/opt/data/users' in result)
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(2, len(datasets), msg=str(datasets))
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')
        self.assertEqual(1, len(result), msg=str(result))
        result = result['s3://cerebrodata-test/decimal-test']
        self.assertEqual(2, len(result), msg=str(result))
        result = planner.cat('s3://cerebrodata-test/alltypes')
        self.assertEqual('true|0|1|2|3|4.0|5.0|hello|vchar1|char1|2015-01-01|3.141592', result.split('\n')[0])
        planner.close()

    def test_as_testuser(self):
        ctx = context()
        ctx.enable_token_auth(token_str='testuser')
        planner = ctx.connect()
        result = planner.get_catalog_objects_at('file:/opt/data/')
        self.assertTrue('file:/opt/data/sample' in result)
        self.assertTrue('file:/opt/data/users' in result)
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))
        result1 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result1))
        result2 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions///')
        self.assertEqual(1, len(result2))
        result3 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions/')
        self.assertEqual(1, len(result3))
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(1, len(datasets))
        self.assertTrue('demo_test.transactions_schemaed' in datasets)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException, 'does not have access'):
            planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')
        result = planner.cat('s3://cerebrodata-test/alltypes')
        self.assertEqual('2,4.0,hello', result.split('\n')[0])
        planner.close()

    def test_masking(self):
        ctx = context()
        ctx.enable_token_auth(token_str='root')
        planner = ctx.connect()
        result = planner.cat('s3://cerebrodata-test/ccn').split('\n')[0]
        self.assertEqual('user1,4539797705756008', result)
        planner.close()
        ctx.enable_token_auth(token_str='testuser')
        planner = ctx.connect()
        result = planner.cat('s3://cerebrodata-test/ccn').split('\n')[0]
        self.assertEqual('user1,XXXXXXXXXXXX6008', result)
        planner.close()

    def test_dropping(self):
        ctx = context()
        planner = ctx.connect()
        planner.execute_ddl('DROP DATABASE IF EXISTS ofs CASCADE')
        planner.execute_ddl('CREATE DATABASE ofs')
        planner.execute_ddl('CREATE EXTERNAL TABLE ofs.t1(s string) ' + "LOCATION 's3://cerebrodata-test/empty-path-test'")
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(1, len(datasets))
        self.assertEqual('ofs.t1', datasets[0])
        planner.execute_ddl('CREATE EXTERNAL TABLE ofs.t2(s string) ' + "LOCATION 's3://cerebrodata-test/empty-path-test'")
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(2, len(datasets))
        self.assertTrue('ofs.t1' in datasets)
        self.assertTrue('ofs.t2' in datasets)
        planner.execute_ddl('DROP TABLE ofs.t2')
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(1, len(datasets))
        self.assertEqual('ofs.t1', datasets[0])
        planner.execute_ddl('DROP TABLE ofs.t1')
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(0, len(result))


if __name__ == '__main__':
    unittest.main()