# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prepare_env_test_mode/take_backup.py
# Compiled at: 2018-09-13 02:55:15
# Size of source mod 2**32: 24204 bytes
from master_backup_script.backuper import Backup
from prepare_env_test_mode.run_benchmark import RunBenchmark
from time import sleep
import os, signal, shutil, logging, concurrent.futures
from shlex import split
from subprocess import Popen, getstatusoutput
from general_conf import path_config
logger = logging.getLogger(__name__)

class WrapperForBackupTest(Backup):

    def __init__(self, config=path_config.config_path_file, full_dir=None, inc_dir=None, basedir=None):
        self.conf = config
        super().__init__(config=(self.conf))
        if full_dir is not None:
            self.full_dir = full_dir
        if inc_dir is not None:
            self.inc_dir = inc_dir
        if basedir is not None:
            self.basedir = basedir

    @staticmethod
    def general_tablespace_rel(basedir):
        directory = '{}/relative_path'.format(basedir)
        if os.path.exists(directory):
            try:
                logger.debug('Removing relative_path...')
                shutil.rmtree(directory)
            except Exception as err:
                logger.debug('FAILED: Removing relative_path')
                logger.error(err)

        try:
            logger.debug('Creating relative_path...')
            os.makedirs(directory)
        except Exception as err:
            logger.debug('FAILED: Creating relative_path')
            logger.error(err)

    @staticmethod
    def parallel_sleep_queries(basedir, sql, sock):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = "{}/run_sql_queries.sh {} {} '{}'".format(dir_path, basedir, sock, sql)
        try:
            process = Popen((split(bash_command)),
              stdin=None,
              stdout=None,
              stderr=None)
        except Exception as e:
            print(e)

    @staticmethod
    def run_ddl_test_sh(basedir, sock):
        logger.debug('Trying to run call_ddl_test.sh')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = '{}/call_ddl_test.sh {} {} {}'.format(dir_path, dir_path, basedir, sock)
        try:
            process = Popen((split(bash_command)),
              stdin=None,
              stdout=None,
              stderr=None)
        except Exception as e:
            print(e)

    @staticmethod
    def run_temp_table_test_sh(basedir, sock):
        logger.debug('Trying to run call_temp_table_test.sh')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = '{}/call_temp_table_test.sh {} {} {}'.format(dir_path, dir_path, basedir, sock)
        try:
            process = Popen((split(bash_command)),
              stdin=None,
              stdout=None,
              stderr=None)
        except Exception as e:
            print(e)

    @staticmethod
    def run_call_create_index_temp_sh(basedir, sock):
        logger.debug('Trying to run call_temp_table_test.sh')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = '{}/call_create_index_temp.sh {} {} {}'.format(dir_path, dir_path, basedir, sock)
        try:
            process = Popen((split(bash_command)),
              stdin=None,
              stdout=None,
              stderr=None)
        except Exception as e:
            print(e)

    @staticmethod
    def run_call_innodb_online_alter_encryption_sql_sh(basedir, sock):
        logger.debug('Trying to run call_innodb_online_alter_encryption_sql.sh')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = '{}/call_innodb_online_alter_encryption_sql.sh {} {} {}'.format(dir_path, basedir, sock, dir_path)
        status, output = getstatusoutput(bash_command)
        if status == 0:
            logger.debug('Running call_innodb_online_alter_encryption_sql.sh - OK')
        else:
            logger.error('Failed to run')
            logger.error(output)

    @staticmethod
    def run_call_innodb_online_alter_encryption_alters_sh(basedir, sock):
        logger.debug('Trying to run call_innodb_online_alter_encryption_alters.sh')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        bash_command = '{}/call_innodb_online_alter_encryption_alters.sh {} {} {}'.format(dir_path, basedir, sock, dir_path)
        try:
            process = Popen((split(bash_command)),
              stdin=None,
              stdout=None,
              stderr=None)
        except Exception as e:
            print(e)

    @staticmethod
    def check_kill_process(pstring):
        for line in os.popen('ps ax | grep ' + pstring + ' | grep -v grep'):
            fields = line.split()
            pid = fields[0]
            if pid:
                os.kill(int(pid), signal.SIGKILL)

    @staticmethod
    def create_million_tables(basedir):
        for i in range(1000000):
            sql_create = 'create table sysbench_test_db.ddl_table{}(id int not null)'
            RunBenchmark.run_sql_statement(basedir=basedir, sql_statement=(sql_create.format(i)))

    def run_all_backup(self):
        RunBenchmark().run_sysbench_prepare(basedir=(self.basedir))
        if '5.7' in self.basedir:
            sql_create_dictionary = "CREATE COMPRESSION_DICTIONARY numbers('08566691963-88624912351-16662227201-46648573979-64646226163-77505759394-75470094713-41097360717-15161106334-50535565977')"
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_dictionary)
            sql_create_tablespace = "create tablespace ts3_enc add datafile 'ts3_enc.ibd' encryption='Y'"
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_tablespace)
            self.run_call_innodb_online_alter_encryption_sql_sh(basedir=(self.basedir), sock=('{}/socket.sock'.format(self.basedir)))
            self.run_call_innodb_online_alter_encryption_alters_sh(basedir=(self.basedir), sock=('{}/socket.sock'.format(self.basedir)))
            sql_create_table = 'CREATE TABLE sysbench_test_db.t10 (a INT AUTO_INCREMENT PRIMARY KEY, b INT)'
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_table)
            for _ in range(10):
                insert_rand = 'INSERT INTO sysbench_test_db.t10 (b) VALUES (FLOOR(RAND() * 10000)), (FLOOR(RAND() * 10000)), (FLOOR(RAND() * 10000))'
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=insert_rand)

            for _ in range(5):
                insert_select = 'INSERT INTO sysbench_test_db.t10 (b) SELECT b FROM sysbench_test_db.t10'
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=insert_select)

            self.run_temp_table_test_sh(basedir=(self.basedir), sock=('{}/socket.sock'.format(self.basedir)))
            self.run_call_create_index_temp_sh(basedir=(self.basedir), sock=('{}/socket.sock'.format(self.basedir)))
            for i in range(1, 5):
                sql_encrypt = "alter table sysbench_test_db.sbtest{} encryption='Y'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_encrypt)
                sql_compress = "alter table sysbench_test_db.sbtest{} compression='lz4'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_compress)
                sql_optimize = 'optimize table sysbench_test_db.sbtest{}'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_optimize)
                sql_virtual_column = 'alter table sysbench_test_db.sbtest{} add column json_test_v json generated always as (json_array(k,c,pad)) virtual'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_virtual_column)
                sql_stored_column = 'alter table sysbench_test_db.sbtest{} add column json_test_s json generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_stored_column)
                sql_create_json_column = 'alter table sysbench_test_db.sbtest{} add column json_test_index varchar(255) generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_json_column)
                sql_alter_add_index = 'alter table sysbench_test_db.sbtest{} add index(json_test_index)'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_add_index)

            general_tablespace = "create tablespace ts1 add datafile 'ts1.ibd' engine=innodb"
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=general_tablespace)
            outside_tablespace_full_path = '{}/out_ts1.ibd'.format(self.basedir)
            if os.path.isfile(outside_tablespace_full_path):
                os.remove(outside_tablespace_full_path)
            general_out_tablespace = "create tablespace out_ts1 add datafile '{}' engine=innodb".format(outside_tablespace_full_path)
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=general_out_tablespace)
            for i in range(5, 10):
                sql_compress = "alter table sysbench_test_db.sbtest{} compression='zlib'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_compress)
                sql_optimize = 'optimize table sysbench_test_db.sbtest{}'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_optimize)
                sql_alter_compression_dict = 'alter table sysbench_test_db.sbtest{} modify c varchar(250) column_format compressed with compression_dictionary numbers'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_compression_dict)

            for i in range(10, 15):
                sql_virtual_column = 'alter table sysbench_test_db.sbtest{} add column json_test_v json generated always as (json_array(k,c,pad)) virtual'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_virtual_column)
                sql_stored_column = 'alter table sysbench_test_db.sbtest{} add column json_test_s json generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_stored_column)
                sql_create_json_column = 'alter table sysbench_test_db.sbtest{} add column json_test_index varchar(255) generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_json_column)
                sql_alter_add_index = 'alter table sysbench_test_db.sbtest{} add index(json_test_index)'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_add_index)
                sql_encrypt = "alter table sysbench_test_db.sbtest{} encryption='N'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_encrypt)
                sql_alter_tablespace = 'alter table sysbench_test_db.sbtest{} tablespace=ts1'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_tablespace)

            for i in range(15, 20):
                sql_virtual_column = 'alter table sysbench_test_db.sbtest{} add column json_test_v json generated always as (json_array(k,c,pad)) virtual'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_virtual_column)
                sql_stored_column = 'alter table sysbench_test_db.sbtest{} add column json_test_s json generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_stored_column)
                sql_create_json_column = 'alter table sysbench_test_db.sbtest{} add column json_test_index varchar(255) generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_json_column)
                sql_alter_add_index = 'alter table sysbench_test_db.sbtest{} add index(json_test_index)'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_add_index)
                sql_encrypt = "alter table sysbench_test_db.sbtest{} encryption='N'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_encrypt)
                sql_alter_tablespace = 'alter table sysbench_test_db.sbtest{} tablespace=out_ts1'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_tablespace)

            for i in range(25, 30):
                sql_encrypt = "alter table sysbench_test_db.sbtest{} encryption='Y'".format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_encrypt)
                sql_virtual_column = 'alter table sysbench_test_db.sbtest{} add column json_test_v json generated always as (json_array(k,c,pad)) virtual'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_virtual_column)
                sql_stored_column = 'alter table sysbench_test_db.sbtest{} add column json_test_s json generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_stored_column)
                sql_create_json_column = 'alter table sysbench_test_db.sbtest{} add column json_test_index varchar(255) generated always as (json_array(k,c,pad)) stored'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_json_column)
                sql_alter_add_index = 'alter table sysbench_test_db.sbtest{} add index(json_test_index)'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_add_index)
                sql_alter_tablespace = 'alter table sysbench_test_db.sbtest{} tablespace=ts3_enc'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter_tablespace)

        if '5.5' in self.basedir:
            for i in range(1, 5):
                sql_alter = 'alter table sysbench_test_db.sbtest{} modify c varchar(120) CHARACTER SET utf8 COLLATE utf8_general50_ci'.format(i)
                RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_alter)

        if '5.6' in self.basedir or '5.7' in self.basedir:
            if os.path.exists('{}/{}'.format(self.basedir, 'sysbench_test_db')):
                shutil.rmtree('{}/{}'.format(self.basedir, 'sysbench_test_db'))
            sql_create_table = "create table sysbench_test_db.t1(c varchar(255)) data directory='{}'".format(self.basedir)
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_create_table)
            sql_insert_data = 'insert into sysbench_test_db.t1 select c from sysbench_test_db.sbtest1'
            RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=sql_insert_data)
        flush_tables = 'flush tables'
        RunBenchmark.run_sql_statement(basedir=(self.basedir), sql_statement=flush_tables)
        sleep(10)
        try:
            try:
                for _ in range(int(self.incremental_count) + 1):
                    self.all_backup()

            except Exception as err:
                print(err)
                raise
            else:
                if os.path.isfile('{}/out_ts1.ibd'.format(self.basedir)):
                    os.remove('{}/out_ts1.ibd'.format(self.basedir))
                if os.path.isfile('{}/sysbench_test_db/t1.ibd'.format(self.basedir)):
                    os.remove('{}/sysbench_test_db/t1.ibd'.format(self.basedir))
        finally:
            self.check_kill_process('call_temp_table_test')
            self.check_kill_process('call_create_index_temp')
            self.check_kill_process('call_innodb_alter_encryption_alters')
            self.check_kill_process('call_innodb_alter_encryption_sql')

        return True