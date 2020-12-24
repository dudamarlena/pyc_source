# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/output_handlers/console/console_handler.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 9298 bytes
import logging, re, time
from collections import OrderedDict
from pgobserver_gatherer.output_handlers.handler_base import HandlerBase
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

def humanize(val):
    return 'humanized ' + str(val)


def pretty_size(size):
    """ mimics pg_size_pretty() """
    if size is None:
        return
    sign = '-' if size < 0 else ''
    size = abs(size)
    if size <= 1024:
        return sign + str(size) + ' B'
    if size < 10485760:
        return sign + str(round(size / 1024)) + ' kB'
    if size < 10737418240:
        return sign + str(round(size / 1048576)) + ' MB'
    if size < 10995116277760:
        return sign + str(round(size / 1073741824)) + ' GB'
    return sign + str(round(size / 1099511627776)) + ' TB'


class Transformations:
    TF_TIME_NICE = lambda x: x.time().replace(microsecond=0)
    ROUND = --- This code section failed: ---

 L.  33         0  LOAD_FAST                'x'
                3  LOAD_CONST               None
                6  COMPARE_OP               is-not
                9  POP_JUMP_IF_FALSE    22  'to 22'
               12  LOAD_GLOBAL              round
               15  LOAD_FAST                'x'
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  RETURN_END_IF_LAMBDA
             22_0  COME_FROM             9  '9'
               22  LOAD_FAST                'x'
               25  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    TF_HUMAN_READABLE = --- This code section failed: ---

 L.  34         0  LOAD_FAST                'x'
                3  LOAD_CONST               None
                6  COMPARE_OP               is-not
                9  POP_JUMP_IF_FALSE    22  'to 22'
               12  LOAD_GLOBAL              humanize
               15  LOAD_FAST                'x'
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  RETURN_END_IF_LAMBDA
             22_0  COME_FROM             9  '9'
               22  LOAD_FAST                'x'
               25  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    SIZE_PRETTY = pretty_size


def apply_transformations(data_val, transformation_list):
    if not transformation_list:
        return data_val
    logging.debug('[consolehandler] applying transformations to "%s"', data_val)
    data_ret = data_val
    for tf_lambda in transformation_list:
        data_ret = tf_lambda(data_ret)

    return data_ret


class Handler(HandlerBase):
    DATASET_CONFIG = {Datasets.BGWRITER: OrderedDict([
                         (
                          'sbd_timestamp', {}),
                         (
                          'sbd_checkpoints_timed', {}),
                         (
                          'sbd_checkpoints_req', {}),
                         (
                          'sbd_checkpoint_write_time', {}),
                         (
                          'sbd_buffers_checkpoint', {}),
                         (
                          'sbd_buffers_backend', {}),
                         (
                          'sbd_buffers_alloc', {})]), 
     Datasets.DB: OrderedDict([
                   (
                    'sdd_timestamp', {'transform': [Transformations.TF_TIME_NICE]}),
                   (
                    'sdd_numbackends', {}),
                   (
                    'sdd_temp_bytes', {'transform': [Transformations.ROUND],  'unit': 'times_min'}),
                   (
                    'sdd_temp_files', {'transform': [Transformations.ROUND]}),
                   (
                    'sdd_blks_read', {'transform': [Transformations.ROUND]}),
                   (
                    'sdd_blks_hit', {'transform': [Transformations.ROUND]}),
                   (
                    'cache_hit_pct', {'transform': [Transformations.ROUND]}),
                   (
                    'sdd_blk_read_time', {'transform': []}),
                   (
                    'sdd_blk_write_time', {'transform': []})]), 
     Datasets.INDEX: OrderedDict([
                      (
                       'iud_timestamp', {}),
                      (
                       'i_schema', {}),
                      (
                       'i_name', {}),
                      (
                       'iud_scan', {}),
                      (
                       'iud_tup_read', {}),
                      (
                       'iud_tup_fetch', {}),
                      (
                       'iud_size', {'transform': [Transformations.SIZE_PRETTY]})]), 
     Datasets.KPI: OrderedDict([
                    (
                     'kpi_timestamp', {}),
                    (
                     'kpi_load_1min', {}),
                    (
                     'kpi_active_backends', {}),
                    (
                     'kpi_blocked_backends', {}),
                    (
                     'kpi_tps', {'transform': []}),
                    (
                     'kpi_rollbacks', {'transform': []}),
                    (
                     'kpi_temp_bytes', {'transform': [Transformations.SIZE_PRETTY]}),
                    (
                     'kpi_wal_location_b', {'transform': [Transformations.SIZE_PRETTY]}),
                    (
                     'kpi_ins', {}),
                    (
                     'kpi_upd', {}),
                    (
                     'kpi_del', {}),
                    (
                     'kpi_sproc_calls', {})]), 
     Datasets.LOAD: OrderedDict([
                     (
                      'load_timestamp', {}),
                     (
                      'load_1min_value', {}),
                     (
                      'xlog_location_b', {'transform': [Transformations.ROUND]})]), 
     Datasets.SCHEMAS: OrderedDict([
                        (
                         'sud_timestamp', {}),
                        (
                         'sud_schema_name', {}),
                        (
                         'sud_seq_scans', {}),
                        (
                         'sud_idx_scans', {}),
                        (
                         'sud_sproc_calls', {}),
                        (
                         'sud_tup_ins', {}),
                        (
                         'sud_tup_upd', {}),
                        (
                         'sud_tup_del', {})]), 
     Datasets.SPROCS: OrderedDict([
                       (
                        'sp_timestamp', {'transform': [Transformations.TF_TIME_NICE]}),
                       (
                        'schema_name', {}),
                       (
                        'function_name', {}),
                       (
                        'sp_calls', {'transform': [Transformations.ROUND],  'unit': 'times_min'}),
                       (
                        'sp_total_time', {'transform': [Transformations.ROUND]}),
                       (
                        'sp_avg_runtime_s', {'transform': [Transformations.ROUND]})]), 
     Datasets.TABLE: OrderedDict([
                      (
                       'tsd_timestamp', {}),
                      (
                       't_schema', {}),
                      (
                       't_name', {}),
                      (
                       'tsd_table_size', {}),
                      (
                       'tsd_index_size', {}),
                      (
                       'tsd_seq_scans', {}),
                      (
                       'tsd_index_scans', {})])}

    def __init__(self, settings=None, filters=None):
        self.name = 'consolehandler'
        super().__init__(self.name, settings, filters)
        logging.info('[%s] initialized. settings: %s, filters: %s', self.name, settings, filters)
        self.rows_printed = 0

    def run(self):
        logging.debug('[%s] starting up ...', self.name)
        while True:
            try:
                if self.queue.qsize() > 0:
                    host_name, dataset_name, data = self.queue.get()
                    logging.debug('[%s] printing "%s" dataset', self.name, dataset_name)
                    self.print_item(dataset_name, data)
                else:
                    logging.debug('[%s] sleeping 1s ...', self.name)
                    time.sleep(1)
            except KeyboardInterrupt:
                break

    def print_item(self, dataset_name, dataset):
        logging.debug('[%s] print_item() - items: %s', self.name, len(dataset))
        tz_col = None
        if Handler.DATASET_CONFIG.get(dataset_name):
            cols_to_print = list(self.DATASET_CONFIG[dataset_name].keys())
        else:
            cols_to_print = sorted(dataset[0].keys())
        tz_col = SUPPORTED_DATASETS[dataset_name][1] + 'timestamp'
        if tz_col in cols_to_print:
            cols_to_print.pop(cols_to_print.index(tz_col))
            cols_to_print = [tz_col] + cols_to_print
        else:
            logging.warning('[%s][%s] timestamp column "%s" not found', self.name, dataset_name)
        try:
            cols_to_print.remove(SUPPORTED_DATASETS[dataset_name][1] + 'host_id')
        except ValueError:
            pass

        cols_to_print_trimmed = []
        for x in cols_to_print:
            cols_to_print_trimmed.append(re.sub('([a-z]+_)', '', x, 1))

        logging.debug('[%s] cols_to_print: %s', self.name, cols_to_print_trimmed)
        if self.rows_printed % 10 == 0:
            print('\t'.join(cols_to_print_trimmed))
        for data in dataset:
            logging.debug('[%s] printing: %s', self.name, data)
            ds = []
            if self.filters:
                if len(SUPPORTED_DATASETS[dataset_name]) > 2:
                    key_cols = SUPPORTED_DATASETS[dataset_name][2]
                    logging.debug('[%s] start filtering - filters: %s, key_cols: %s', self.name, self.filters, key_cols)
                    is_match = True
                    for i, f in enumerate(self.filters):
                        if not data.get(key_cols[i]) or str(data[key_cols[i]]).find(f) == -1:
                            is_match = False
                            break

                    if not is_match:
                        continue
                    for col in cols_to_print:
                        if col not in data:
                            ds.append('NULL')
                            continue
                        if col == tz_col:
                            col_val = apply_transformations(data[col], [Transformations.TF_TIME_NICE])
                        else:
                            if self.DATASET_CONFIG.get(dataset_name, {}).get(col, {}).get('transform'):
                                col_val = apply_transformations(data[col], self.DATASET_CONFIG.get(dataset_name, {}).get(col, {}).get('transform', []))
                            else:
                                col_val = data[col]
                        ds.append(str(col_val))

                    print('\t'.join(ds))
                    self.rows_printed += 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    h = Handler()
    h.start()
    print('handler started')
    print(h)
    print('q', h.queue)
    for i in range(1, 5):
        item = {'k1': i,  'k2': i * 2}
        print('putting', item)
        h.queue.put(('set1', item))
        time.sleep(1)