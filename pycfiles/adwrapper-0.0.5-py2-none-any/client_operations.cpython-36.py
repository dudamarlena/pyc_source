# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alanjds/src/git/adwords-client/adwords_client/client_operations.py
# Compiled at: 2017-07-12 10:46:26
# Size of source mod 2**32: 3193 bytes
import logging, pandas as pd
from datetime import datetime
from multiprocessing import Pool, cpu_count, RLock
from .client import AdWords
from .sqlite import remove_temporary_files
logger = logging.getLogger(__name__)

def timestamp_client_table(client, table_name, timestamp):
    df = pd.read_sql_table(table_name, client.engine)
    df['tmstmp'] = timestamp
    df.to_sql(table_name, (client.engine), if_exists='replace', index=False)


def adwords_worker(timestamp, operation_function, mapper, config_file, internal_table, proc_id, total_procs, *args, **kwargs):
    adwords = AdWords(config_file)
    try:
        try:
            mapper.set_lock(LOCK)
            if kwargs.pop('map_data', True):
                mapper.map_data(adwords, internal_table, proc_id, total_procs)
            operations_log_table = kwargs.pop('operations_log_table', None)
            drop_batchlog_table = kwargs.pop('drop_batchlog_table', False)
            drop_operations_log_table = kwargs.pop('drop_operations_log_table', False)
            batchlog_table = kwargs.get('batchlog_table', None)
            operation_function(adwords, internal_table, *args, **kwargs)
            if batchlog_table:
                timestamp_client_table(adwords, batchlog_table, timestamp)
                mapper.upsync(adwords, batchlog_table, batchlog_table, drop_table=drop_batchlog_table)
            if operations_log_table:
                timestamp_client_table(adwords, internal_table, timestamp)
                mapper.upsync(adwords, internal_table, operations_log_table, drop_table=drop_operations_log_table)
            mapper.set_lock(None)
        except Exception as e:
            logger.exception(e)
            raise e

    finally:
        remove_temporary_files()


def kwargs_worker(args, kwargs):
    adwords_worker(*args, **kwargs)


def init_lock(parent_lock):
    global LOCK
    LOCK = parent_lock


class ClientOperation:

    def __init__(self, mapper, config_file):
        self.mapper = mapper
        self.config_file = config_file

    def run(self, operation_function, internal_table, *args, **kwargs):
        child_args = []
        batchlog_table = kwargs.get('batchlog_table', False)
        n_procs = kwargs.pop('n_procs', cpu_count() + 1) if batchlog_table else 1
        timestamp = datetime.now().isoformat()
        for i in range(0, n_procs):
            worker_args = [timestamp,
             operation_function,
             self.mapper,
             self.config_file,
             internal_table,
             i,
             n_procs] + list(args)
            child_args.append([worker_args, kwargs])

        lock = RLock()
        with Pool(n_procs, initializer=init_lock, initargs=(lock,)) as (p):
            p.starmap(kwargs_worker, child_args, 1)