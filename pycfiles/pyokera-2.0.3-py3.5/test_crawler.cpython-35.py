# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_crawler.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 38455 bytes
import os, time, unittest
from collections import namedtuple
from okera import context, _thrift_api
from okera.tests import pycerebro_test_common as common
CRAWLER_STATUS_KEY = 'okera.crawler.status'
CRAWLER_DATA_FILE_PATH_KEY = 'okera.crawler.data_file_path'
CRAWLER_TEST_MODES = os.environ.get('CRAWLER_TEST_MODES', 'S3')
FIELDS = [
 'provider', 'name', 'root_path', 'found_tables', 'timeout']
CrawlerTest = namedtuple('CrawlerTest', FIELDS)

class CrawlerIntegrationTest(unittest.TestCase):

    def _wait_for_crawler(self, conn, crawler_db, dataset=None, max_sec=25):
        """ Waits for the crawler to find dataset for this crawler
            If dataset is None, then just wait for the crawler to report COMPLETED.
        """
        sleep_time = 1
        if max_sec > 60:
            sleep_time = 3
        if max_sec > 120:
            sleep_time = 5
        elapsed_sec = 0
        datasets = None
        while elapsed_sec < max_sec:
            time.sleep(sleep_time)
            elapsed_sec += sleep_time
            if dataset:
                datasets = conn.list_dataset_names(crawler_db)
                if crawler_db + '.' + dataset in datasets:
                    return datasets
            else:
                params = conn.execute_ddl('DESCRIBE DATABASE %s' % crawler_db)
                for p in params:
                    if p[0] == CRAWLER_STATUS_KEY and p[1] == 'COMPLETED':
                        return conn.list_dataset_names(crawler_db)

        if not datasets:
            datasets = conn.list_dataset_names(crawler_db)
        print('Found datasets: ' + str(datasets))
        self.fail('Crawler did not find dataset in time.')

    def create_crawler_and_verify(self, crawler, root_path, found_tables, max_sec=25):
        crawler_db = '_okera_crawler_' + crawler
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, root_path))
            for table in found_tables:
                print('Waiting on table: %s' % table)
                self._wait_for_crawler(conn, crawler_db, table, max_sec)

    def run_crawler_test(self, config=None):
        if not config:
            return
        if config.provider in CRAWLER_TEST_MODES:
            self.create_crawler_and_verify(config.name, config.root_path, config.found_tables, config.timeout)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_basic(self):
        tests = [
         CrawlerTest(provider='S3', name='integration_test', root_path='s3://cerebrodata-test/tpch-nation-integration-test/', found_tables=[
          'tpch_nation_integration_test'], timeout=25),
         CrawlerTest(provider='ADLS', name='integration_test', root_path='adl://okeratestdata.azuredatalakestore.net/cerebrodata-test/tpch-nation-integration-test/', found_tables=[
          'tpch_nation_integration_test'], timeout=25),
         CrawlerTest(provider='ABFS', name='integration_test', root_path='abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/tpch-nation-integration-test/', found_tables=[
          'tpch_nation_integration_test'], timeout=25)]
        for test in tests:
            self.run_crawler_test(test)

    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_not_slow_5k(self):
        tests = [
         CrawlerTest(provider='S3', name='integration_test', root_path='s3://cerebrodata-test/part_flat_5000_data_100/', found_tables=[
          'part_flat_5000_data_100'], timeout=10)]
        for test in tests:
            self.run_crawler_test(test)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_flat(self):
        tests = [
         CrawlerTest(provider='S3', name='integration_test', root_path='s3://cerebrodata-test/crawler_flat_structure/', found_tables=[
          'atp_csv', 'topbabynamesbystate_csv'], timeout=25),
         CrawlerTest(provider='ADLS', name='integration_test', root_path='adl://okeratestdata.azuredatalakestore.net/cerebrodata-test/crawler_flat_structure/', found_tables=[
          'atp_csv', 'topbabynamesbystate_csv'], timeout=25),
         CrawlerTest(provider='ABFS', name='integration_test', root_path='abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/crawler_flat_structure/', found_tables=[
          'atp_csv', 'topbabynamesbystate_csv'], timeout=25)]
        for test in tests:
            if test.provider not in CRAWLER_TEST_MODES:
                pass
            else:
                crawler_db = '_okera_crawler_' + test.name
                ctx = context()
                with ctx.connect() as (conn):
                    conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
                    conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (test.name, test.root_path))
                    self._wait_for_crawler(conn, crawler_db, None)
                    datasets = conn.list_dataset_names(crawler_db)
                    self.assertTrue(len(datasets) == 1)
                    conn.execute_ddl('DROP TABLE %s.%s' % (crawler_db, 'crawler_flat_structure'))
                    conn.execute_ddl("ALTER DATABASE %s SET DBPROPERTIES('%s'='%s')" % (
                     crawler_db, 'okera.crawler.single_file_datasets', 'true'))
                    conn.execute_ddl("ALTER DATABASE %s SET DBPROPERTIES('%s'='%s')" % (
                     crawler_db, CRAWLER_STATUS_KEY, ''))
                    for table in test.found_tables:
                        self._wait_for_crawler(conn, crawler_db, table)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_empty(self):
        crawler = 'test_empty'
        crawler_db = '_okera_crawler_' + crawler
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/empty/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/' + 'cerebrodata-test/empty_folder/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'empty_folder/'
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None)
        if contents:
            self.fail('Directory was not empty, location : ' + location)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_hidden_file(self):
        crawler = 'test_hidden_file'
        crawler_db = '_okera_crawler_' + crawler
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/hidden_files_only/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/' + 'cerebrodata-test/hidden_file/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'hidden_files_only/'
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None)
        if contents:
            self.fail('Directory was not empty or hidden file found, location : ' + location)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_bad_path_good_scheme(self):
        caught = None
        crawler = 'test_bad_path_good_scheme'
        crawler_db = '_okera_crawler_' + crawler
        bucket = 'thispathdoesnotexistcerebro'
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://%s/' % bucket
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://%s.azuredatalakestore.net/' % bucket
            elif 'ABFS' in CRAWLER_TEST_MODES:
                location = 'abfs://%s@okeratestdata.dfs.core.windows.net/' % bucket
        ctx = context()
        with ctx.connect() as (conn):
            try:
                conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
                conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            except Exception as e:
                if 'is not accessible' not in str(e) and 'does not exist' not in str(e):
                    self.fail('Exception did not match expected. Ex encountered: ' + str(e))
                else:
                    caught = True

            if not caught:
                self.fail('No exception raised, expected TRecordServiceException')

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_null_path(self):
        crawler = 'test_null_path'
        caught = None
        crawler_db = '_okera_crawler' + crawler
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            try:
                conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, None))
            except Exception as e:
                if 'Crawlers are not configured for this cloud platform' not in str(e):
                    self.fail('Exception did not match expected. Ex encountered: ' + str(e))
                else:
                    caught = True

            if not caught:
                self.fail('No exception raised, expected TRecordServiceException')

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_bad_scheme(self):
        caught = None
        crawler = 'test_bad_scheme'
        crawler_db = '_okera_crawler' + crawler
        location = 'foo://bucket/path'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            try:
                conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            except Exception as e:
                if 'Crawlers are not configured for this cloud platform' not in str(e):
                    self.fail('Exception did not match expected. Ex encountered: ' + str(e))
                else:
                    caught = True

            if not caught:
                self.fail('No exception raised, expected TRecordServiceException')

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_crawl_partitioned(self):
        crawler = 'test_crawl_partitioned'
        crawler_db = '_okera_crawler_' + crawler
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/partitions-test2/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/' + 'cerebrodata-test/partitions-test/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'partitions-test2/'
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None, 30)
        if len(contents) != 2:
            self.fail('Did not find 2 datasets at location: ' + location)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_crawl_already_registered(self, testType=None):
        crawler = 'test_crawl_already_registered'
        crawler_db = '_okera_crawler_' + crawler
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/tpch_nation/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/cerebrodata-test/tpch_nation/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'tpch_nation/'
                else:
                    self.fail('Test received invalid testType: ' + testType)
        ctx = context()
        with ctx.connect() as (conn):
            if 'S3' in CRAWLER_TEST_MODES:
                conn.execute_ddl("CREATE EXTERNAL TABLE IF NOT EXISTS`default`.`tpch_nation_s3`(s smallint, n string, t smallint, d string) LOCATION '%s'" % location)
            else:
                if 'ADLS' in CRAWLER_TEST_MODES:
                    conn.execute_ddl("CREATE EXTERNAL TABLE IF NOT EXISTS`default`.`tpch_nation_adls`(s smallint, n string, t smallint, d string) LOCATION '%s'" % location)
                elif 'ABFS' in CRAWLER_TEST_MODES:
                    conn.execute_ddl("CREATE EXTERNAL TABLE IF NOT EXISTS`default`.`tpch_nation_abfs`(s smallint, n string, t smallint, d string) LOCATION '%s'" % location)
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None)
        if contents:
            print(str(contents))
            self.fail('Found unregistered dataset when should have found none: ' + location)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_crawl_duplicate_paths(self):
        crawler1 = 'test_crawl_duplicate_paths_1'
        crawler1_db = '_okera_crawler_' + crawler1
        crawler2 = 'test_crawl_duplicate_paths_2'
        crawler2_db = '_okera_crawler_' + crawler2
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/alltypes-parquet/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/cerebrodata-test/alltypes-parquet/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'alltypes-parquet/'
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler1_db)
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler2_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler1, location))
            contents1 = self._wait_for_crawler(conn, crawler1_db, None)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler2, location))
            contents2 = self._wait_for_crawler(conn, crawler2_db, None)
            contents1 = [ds.split('.')[1] for ds in contents1]
            contents2 = [ds.split('.')[1] for ds in contents2]
        self.assertEqual(contents1, contents2)

    @staticmethod
    def __get_columns(dataset):
        cols = []
        partition_cols = []
        for c in dataset.schema.cols:
            if c.hidden:
                pass
            else:
                if c.is_partitioning_col:
                    partition_cols.append(c.name)
                else:
                    cols.append(c.name)

        return (
         cols, partition_cols)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_data_partition_col_dup(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebro-test-itay/lake4/partitioned2/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, 'partitioned2')
            dataset = conn.list_datasets(crawler_db, name='partitioned2')
            cols, partition_cols = self._CrawlerIntegrationTest__get_columns(dataset[0])
            self.assertTrue('str2' in cols)
            self.assertTrue('str2' in partition_cols)
            show = conn.execute_ddl('show create table %s.%s' % (crawler_db, 'partitioned2'))[0][0]
            self.assertEqual(2, show.count('str2 STRING'), msg=show)
            conn.execute_ddl('DROP TABLE %s.%s' % (crawler_db, 'partitioned2'))
            conn.execute_ddl("ALTER DATABASE %s SET DBPROPERTIES('%s'='%s')" % (
             crawler_db, 'okera.allow.partition_cols_in_data', 'true'))
            conn.execute_ddl("ALTER DATABASE %s SET DBPROPERTIES('%s'='%s')" % (
             crawler_db, CRAWLER_STATUS_KEY, ''))
            self._wait_for_crawler(conn, crawler_db, 'partitioned2')
            dataset = conn.list_datasets(crawler_db, name='partitioned2')
            cols, partition_cols = self._CrawlerIntegrationTest__get_columns(dataset[0])
            self.assertTrue('str2' not in cols)
            self.assertTrue('str2' in partition_cols)
            show = conn.execute_ddl('show create table %s.%s' % (crawler_db, 'partitioned2'))[0][0]
            self.assertEqual(1, show.count('str2 STRING'), msg=show)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_crawler_no_suffix(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://okera-ui/autotagger/no-postfix'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db)
            dataset = conn.list_datasets(crawler_db, name='csv')[0]
            self.assertEqual('TEXT', dataset.table_format)
            dataset = conn.list_datasets(crawler_db, name='parquet')[0]
            self.assertEqual('PARQUET', dataset.table_format)
            dataset = conn.list_datasets(crawler_db, name='avro')[0]
            self.assertEqual('AVRO', dataset.table_format)
            dataset = conn.list_datasets(crawler_db, name='json')[0]
            self.assertEqual('JSON', dataset.table_format)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_crawler_opencsv(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://okera-cust-success/nflstatistics/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, 'basic_stats', max_sec=30)
            dataset = conn.list_datasets(crawler_db, name='basic_stats')[0]
            self.assertEqual(',', dataset.serde_metadata['separatorChar'])

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_crawler_tsv(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebro-test-kevin/dea_pain_pills/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db)
            dataset = conn.list_datasets(crawler_db, name='dea_pain_pills')[0]
            self.assertEqual('TEXT', dataset.table_format)
            self.assertEqual(42, len(dataset.schema.cols))

    @unittest.skipIf(common.TEST_LEVEL != 'ci' and common.TEST_LEVEL != 'all', 'Only running at CI/ALL level.')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_root_crawler(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebrodata-test/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, 'zookeeper', max_sec=600)
            datasets = conn.list_dataset_names(crawler_db)
            self.assertTrue(len(datasets) > 250, msg=str(datasets))

    @unittest.skipIf(common.TEST_LEVEL != 'ci' and common.TEST_LEVEL != 'all', 'Only running at CI/ALL level.')
    @unittest.skipIf('ABFS' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_root_crawler_abfs(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=600)
            datasets = conn.list_dataset_names(crawler_db)
            self.assertTrue(len(datasets) > 250, msg=str(datasets))

    @unittest.skipIf(common.TEST_LEVEL != 'ci' and common.TEST_LEVEL != 'all', 'Only running at CI/ALL level.')
    @unittest.skipIf('ADLS' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_root_crawler_adls(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 'adl://okeratestdata.azuredatalakestore.net/cerebrodata-test/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=600)
            datasets = conn.list_dataset_names(crawler_db)
            self.assertTrue(len(datasets) > 250, msg=str(datasets))

    @unittest.skipIf(common.TEST_LEVEL != 'ci' and common.TEST_LEVEL != 'all', 'Only running at CI/ALL level.')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_ui_crawler(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://okera-ui/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=300)
            datasets = conn.list_dataset_names(crawler_db)
            self.assertTrue(len(datasets) > 80)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_okera_lite(self):
        crawler = 'okera_lite'
        result_db = 'okera_lite_default'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebrodata-test/tpch-nation/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % result_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, None)
            contents = conn.list_dataset_names(result_db)
            self.assertTrue('okera_lite_default.tpch_nation' in contents, msg=str(contents))

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_das_3489(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebrodata-test/put-test2/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=300)
            dataset = conn.list_datasets(crawler_db, name='put_test2')[0]
            self.assertEqual('TEXT', dataset.table_format)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_empty_json(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebro-datasets/empty-json/empty.json'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=10)
            self.assertTrue(len(conn.list_datasets(crawler_db)) == 0)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_text_boolean(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://okera-demo/consent-management/whitelist'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=10)
            dataset = conn.list_datasets(crawler_db, name='whitelist')[0]
            self.assertEqual(3, len(dataset.schema.cols))
            self.assertEqual(_thrift_api.TTypeId.STRING, dataset.schema.cols[0].type.type_id)
            self.assertEqual(_thrift_api.TTypeId.BOOLEAN, dataset.schema.cols[1].type.type_id)
            self.assertEqual(_thrift_api.TTypeId.BOOLEAN, dataset.schema.cols[2].type.type_id)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_cedilla_delimiter(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebro-datasets/cedilla_sample/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db, max_sec=10)
            dataset = conn.list_datasets(crawler_db, name='cedilla_sample')[0]
            self.assertEqual(2, len(dataset.schema.cols))

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    def test_comments(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://cerebrodata-test/crawler-schema-comments/'
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            self._wait_for_crawler(conn, crawler_db)
            whitelist = conn.list_datasets(crawler_db, name='avro_whitelist')[0]
            self.assertTrue('This dataset stores' in whitelist.description, msg=str(whitelist))
            whitelist_col = whitelist.schema.cols[1]
            self.assertTrue('Indicates if the user' in whitelist_col.comment, msg=str(whitelist_col))
            default_comments = conn.list_datasets(crawler_db, name='avro_no_comments')[0]
            self.assertTrue('Discovered by Okera crawler' in default_comments.description, msg=str(default_comments))
            default_comments_col = default_comments.schema.cols[1]
            self.assertTrue(default_comments_col.comment is None)

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    @unittest.skipIf('S3' not in CRAWLER_TEST_MODES, 'Skipping UT because platform not set in CRAWLER_TEST_MODES')
    @unittest.skipIf('AUTOTAGGER' not in CRAWLER_TEST_MODES, 'Skipping UT because Autotagger not set in CRAWLER_TEST_MODES')
    def test_autotagger(self):
        crawler = 'e2e_test'
        crawler_db = '_okera_crawler_' + crawler
        location = 's3://okera-datalake/gdpr-avro/transactions/'
        ctx = context()
        with ctx.connect() as (conn):
            for _ in range(3):
                conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
                conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
                self._wait_for_crawler(conn, crawler_db)
                transactions = conn.list_datasets(crawler_db, name='transactions')[0]
                self.assertTrue('This dataset stores' in transactions.description, msg=str(transactions))
                ccn = transactions.schema.cols[5]
                self.assertTrue(ccn.attribute_values is not None)
                self.assertEqual('credit_card_number', ccn.attribute_values[0].attribute.key)
                self.assertTrue('credit card number' in ccn.comment, msg=str(ccn))

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_crawl_ordering(self):
        crawler = 'test_crawl_ordering'
        crawler_db = '_okera_crawler_' + crawler
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://cerebrodata-test/partitioned_flat_50000/'
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/' + 'cerebrodata-test/partitioned_flat_50000/'
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + 'partitioned_flat_50000/'
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None, 30)
            self.assertEqual(contents, [
             '_okera_crawler_test_crawl_ordering.partitioned_flat_50000'])
            dataset = conn.list_datasets(crawler_db, name='partitioned_flat_50000')[0]
            datafile_path = dataset.metadata[CRAWLER_DATA_FILE_PATH_KEY]
            self.assertEqual(datafile_path, 's3a://cerebrodata-test/partitioned_flat_50000/part=9999/data_0.csv')

    @unittest.skipIf(common.TEST_LEVEL == 'smoke', 'Skipping at unit test level')
    def test_crawl_dup_names(self):
        crawler = 'test_crawl_dup_names'
        crawler_db = '_okera_crawler_' + crawler
        base_loc = 'okera-demo/'
        if 'S3' in CRAWLER_TEST_MODES:
            location = 's3://' + base_loc
        else:
            if 'ADLS' in CRAWLER_TEST_MODES:
                location = 'adl://okeratestdata.azuredatalakestore.net/' + base_loc
            else:
                if 'ABFS' in CRAWLER_TEST_MODES:
                    location = 'abfs://cerebrodata-test@okeratestdata.dfs.core.windows.net/' + base_loc
                else:
                    self.fail('Test received invalid testType: ' + CRAWLER_TEST_MODES)
        ctx = context()
        with ctx.connect() as (conn):
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % crawler_db)
            conn.execute_ddl("CREATE CRAWLER %s SOURCE '%s'" % (crawler, location))
            contents = self._wait_for_crawler(conn, crawler_db, None, 30)
            self.assertIn('_okera_crawler_test_crawl_dup_names.transactions_1', contents)


if __name__ == '__main__':
    unittest.main()