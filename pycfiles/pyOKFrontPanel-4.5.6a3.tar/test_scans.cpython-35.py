# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_scans.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 10087 bytes
import time, unittest, numpy
from okera.tests import pycerebro_test_common as common
import cerebro_common as cerebro
retry_count = 0

class BasicTest(unittest.TestCase):

    def test_sparse_data(self):
        with common.get_planner() as (planner):
            df = planner.scan_as_pandas('rs.sparsedata')
            self.assertEqual(96, len(df), msg=df)
            self.assertEqual(68, df['age'].count(), msg=df)
            self.assertEqual(10.0, df['age'].min(), msg=df)
            self.assertEqual(96.0, df['age'].max(), msg=df)
            self.assertEqual('sjc', df['defaultcity'].max(), msg=df)
            self.assertEqual(86, df['description'].count(), msg=df)

    def test_nulls(self):
        with common.get_planner() as (planner):
            df = planner.scan_as_pandas('select string_col from rs.alltypes_null')
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['string_col'][0]), msg=df)
            df = planner.scan_as_pandas('select length(string_col) as c from rs.alltypes_null')
            self.assertEqual(1, len(df), msg=df)
            self.assertTrue(numpy.isnan(df['c'][0]), msg=df)

    def test_timestamp_functions(self):
        with common.get_planner() as (planner):
            json = planner.scan_as_json("\n                select date_add('2009-01-01', 10) as c from okera_sample.sample")
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('2009-01-11 00:00:00.000', str(json[0]['c']), msg=json)
            self.assertEqual('2009-01-11 00:00:00.000', str(json[1]['c']), msg=json)

    def test_duplicate_cols(self):
        with common.get_planner() as (planner):
            json = planner.scan_as_json('\n                select record, record from okera_sample.sample')
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record']), msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2']), msg=json)
        with common.get_planner() as (planner):
            json = planner.scan_as_json('\n                select record, record as record_2, record from okera_sample.sample')
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record']), msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2']), msg=json)
            self.assertEqual('This is a sample test file.', str(json[0]['record_2_2']), msg=json)

    def test_large_decimals(self):
        with common.get_planner() as (planner):
            json = planner.scan_as_json('select num from rs.large_decimals2')
            self.assertTrue(len(json) == 6, msg=json)
            self.assertEqual('9012248907891233.020304050670', str(json[0]['num']), msg=json)
            self.assertEqual('2343.999900000000', str(json[1]['num']), msg=json)
            self.assertEqual('900.000000000000', str(json[2]['num']), msg=json)
            self.assertEqual('32.440000000000', str(json[3]['num']), msg=json)
            self.assertEqual('54.230000000000', str(json[4]['num']), msg=json)
            self.assertEqual('4525.340000000000', str(json[5]['num']), msg=json)
        with common.get_planner() as (planner):
            df = planner.scan_as_pandas('select num from rs.large_decimals2')
            self.assertTrue(len(df) == 6, msg=df)
            self.assertEqual('9012248907891233.020304050670', str(df['num'][0]), msg=df)
            self.assertEqual('2343.999900000000', str(df['num'][1]), msg=df)
            self.assertEqual('900.000000000000', str(df['num'][2]), msg=df)
            self.assertEqual('32.440000000000', str(df['num'][3]), msg=df)
            self.assertEqual('54.230000000000', str(df['num'][4]), msg=df)
            self.assertEqual('4525.340000000000', str(df['num'][5]), msg=df)

    def test_date(self):
        with common.get_planner() as (planner):
            json = planner.scan_as_json('select * from datedb.date_csv')
            self.assertTrue(len(json) == 2, msg=json)
            self.assertEqual('Robert', str(json[0]['name']), msg=json)
            self.assertEqual(100, json[0]['id'], msg=json)
            self.assertEqual('1980-01-01', str(json[0]['dob']), msg=json)
            self.assertEqual('Michelle', str(json[1]['name']), msg=json)
            self.assertEqual(200, json[1]['id'], msg=json)
            self.assertEqual('1991-12-31', str(json[1]['dob']), msg=json)
        with common.get_planner() as (planner):
            pd = planner.scan_as_pandas('select * from datedb.date_csv')
            self.assertTrue(len(pd) == 2, msg=pd)
            self.assertEqual('Robert', pd['name'][0], msg=pd)
            self.assertEqual(100, pd['id'][0], msg=pd)
            self.assertEqual('1980-01-01', str(pd['dob'][0]), msg=pd)
            self.assertEqual('Michelle', pd['name'][1], msg=pd)
            self.assertEqual(200, pd['id'][1], msg=pd)
            self.assertEqual('1991-12-31', str(pd['dob'][1]), msg=pd)

    def test_scan_as_json_max_records(self):
        sql = 'select * from okera_sample.sample'
        with common.get_planner() as (planner):
            json = planner.scan_as_json(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(json) == 1, msg='max_records not respected')
            json = planner.scan_as_json(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(json) == 2, msg='max_records not respected')

    def test_scan_as_pandas_max_records(self):
        sql = 'select * from okera_sample.sample'
        with common.get_planner() as (planner):
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 1, msg='max_records not respected')
            pd = planner.scan_as_pandas(sql, max_records=100, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 2, msg='max_records not respected')

    def test_scan_retry(self):
        global retry_count
        sql = 'select * from okera_sample.sample'
        with common.get_planner() as (planner):
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            self.assertTrue(len(pd.index) == 1, msg='test_scan_retry sanity check failed')
            retry_count = 0

            def test_hook_retry(func_name, retries, attempt):
                global retry_count
                if func_name != 'plan':
                    return
                retry_count = retry_count + 1
                if attempt < 2:
                    raise IOError('Fake Error')

            planner.test_hook_retry = test_hook_retry
            pd = planner.scan_as_pandas(sql, max_records=1, max_client_process_count=1)
            assert retry_count == 3
            self.assertTrue(len(pd.index) == 1, msg='Failed to get data with retries')

    def test_worker_retry(self):
        global retry_count
        with common.get_worker() as (worker):
            v = worker.get_protocol_version()
            self.assertEqual('1.0', v)
            retry_count = 0

            def test_hook_retry(func_name, retries, attempt):
                global retry_count
                if func_name != 'get_protocol_version':
                    return
                retry_count = retry_count + 1
                if attempt < 2:
                    raise IOError('Fake Error')

            worker.test_hook_retry = test_hook_retry
            v = worker.get_protocol_version()
            assert retry_count == 3
            self.assertEqual('1.0', v)

    def test_overwrite_file(self):
        with common.get_planner() as (planner):
            planner.execute_ddl('DROP TABLE IF EXISTS rs.dim')
            planner.execute_ddl("CREATE EXTERNAL TABLE rs.dim\n                (country_id INT, country_name STRING, country_code STRING)\n                ROW FORMAT DELIMITED FIELDS TERMINATED BY ','\n                LOCATION 's3://cerebro-datasets/starschema_demo/country_dim/'")
            cerebro.run_shell_cmd('aws s3 cp ' + 's3://cerebro-datasets/country_dim_src/country_DIM.csv ' + 's3://cerebro-datasets/starschema_demo/country_dim/country_DIM.csv')
            before = planner.scan_as_json('rs.dim')[1]
            self.assertEqual('France', before['country_name'], msg=str(before))
            time.sleep(1)
            cerebro.run_shell_cmd('aws s3 cp ' + 's3://cerebro-datasets/country_dim_src/country_DIM2.csv ' + 's3://cerebro-datasets/starschema_demo/country_dim/country_DIM.csv')
            i = 0
            while i < 10:
                after = planner.scan_as_json('rs.dim')[1]
                if 'france' in after['country_name']:
                    return
                self.assertEqual('France', after['country_name'], msg=str(after))
                time.sleep(0.1)
                i = i + 1

            self.fail(msg='Did not updated result in time.')


if __name__ == '__main__':
    unittest.main()