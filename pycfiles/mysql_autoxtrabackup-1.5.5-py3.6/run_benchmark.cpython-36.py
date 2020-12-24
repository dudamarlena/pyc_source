# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prepare_env_test_mode/run_benchmark.py
# Compiled at: 2018-09-13 02:55:15
# Size of source mod 2**32: 6196 bytes
from general_conf.generalops import GeneralClass
from prepare_env_test_mode.clone_build_start_server import CloneBuildStartServer
import subprocess, logging
from general_conf import path_config
logger = logging.getLogger(__name__)

class RunBenchmark:
    __doc__ = '\n    General class for running all kind of Benchmarks; For now running sysbench against started server.\n    '

    def __init__(self, config=path_config.config_path_file):
        self.conf = config
        self.testpath = GeneralClass(self.conf).testpath
        self.basedir = CloneBuildStartServer(self.conf).get_basedir()

    @staticmethod
    def get_sock(basedir):
        logger.debug('Trying to get socket file...')
        file_name = '{}/cl_noprompt_nobinary'
        with open(file_name.format(basedir)) as (config):
            sock_file = config.read().split()[3][2:]
        return sock_file

    @staticmethod
    def get_mysql_conn(basedir, file_name=None):
        logger.debug('Trying to get mysql client connection...')
        if file_name is None:
            get_conn = 'cat {}/cl_noprompt_nobinary'
            status, output = subprocess.getstatusoutput(get_conn.format(basedir))
        else:
            get_conn = 'cat {}/{}'
            status, output = subprocess.getstatusoutput(get_conn.format(basedir, file_name))
        if status == 0:
            logger.debug('Could get mysql client')
            return output
        logger.error('Failed to get mysql client connection')
        logger.error(output)
        raise RuntimeError('Failed to get mysql client connection')

    @staticmethod
    def run_sql_statement(basedir, sql_statement):
        sql = '{} -e "{}"'.format(RunBenchmark.get_mysql_conn(basedir), sql_statement)
        status, output = subprocess.getstatusoutput(sql)
        if status == 0:
            logger.debug('OK: Running -> {}'.format(sql))
            return True
        logger.error('FAILED: running SQL -> {}'.format(sql))
        logger.error(output)
        raise RuntimeError('FAILED: running SQL -> {}'.format(sql))

    def create_db(self, db_name, basedir):
        conn = self.get_mysql_conn(basedir)
        sql = "{} -e 'create database if not exists {} '"
        logger.debug('Trying to create DB...')
        status, output = subprocess.getstatusoutput(sql.format(conn, db_name))
        if status == 0:
            logger.debug('Given DB is created')
            return True
        else:
            logger.error('Failed to create DB')
            logger.error(output)
            return False

    def run_sysbench_prepare(self, basedir):
        db_name = 'sysbench_test_db'
        self.create_db(db_name=db_name, basedir=basedir)
        sock_name = self.get_sock(basedir)
        sysbench_cmd = 'sysbench /usr/share/sysbench/oltp_insert.lua --table-size={} --tables={} --mysql-db={} --mysql-user=root  --threads={} --db-driver=mysql --mysql-socket={} prepare'
        logger.debug('Running command -> {}'.format(sysbench_cmd.format(1000, 35, db_name, 100, sock_name)))
        status, output = subprocess.getstatusoutput(sysbench_cmd.format(1000, 35, db_name, 100, sock_name))
        if status == 0:
            logger.debug('Sysbench succeeded!')
            return True
        logger.error('Failed to run sysbench')
        logger.error(output)
        raise RuntimeError('Failed to run sysbench')

    def run_sysbench_run(self, basedir):
        db_name = 'sysbench_test_db'
        sock_name = self.get_sock(basedir)
        sysbench_cmd = 'sysbench /usr/share/sysbench/oltp_update_non_index.lua --table-size={} --tables={} --mysql-db={} --mysql-user=root  --threads={} --db-driver=mysql --mysql-socket={} run'
        logger.debug('Running command -> {}'.format(sysbench_cmd.format(1000, 35, db_name, 100, sock_name)))
        status, output = subprocess.getstatusoutput(sysbench_cmd.format(1000, 35, db_name, 100, sock_name))
        if status == 0:
            logger.debug('Sysbench succeeded!')
            return True
        logger.error('Failed to run sysbench')
        logger.error(output)
        raise RuntimeError('Failed to run sysbench')