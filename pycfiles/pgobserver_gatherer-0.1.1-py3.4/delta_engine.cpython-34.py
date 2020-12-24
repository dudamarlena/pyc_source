# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/delta_engine.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 19470 bytes
from collections import OrderedDict
from collections import defaultdict
import logging, datetime
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS
from pgobserver_gatherer.globalconfig import config

class Transformations:
    TIMEDELTA = 'timedelta'
    DERIVATIVE = 'derivative'
    PERCENTAGE = 'percentage'


class Units:
    VALUE = 'value'
    VALUE_PRETTY = 'value_pretty'
    TEXT = 'text'
    BYTE = 'byte'
    KB = 'kb'
    MB = 'mb'
    BYTES_S = 'bytes_s'
    BYTES_M = 'bytes_m'
    KB_S = 'kb_s'
    MB_M = 'mb_m'
    MB_H = 'mb_h'
    TZ = 'tz'
    SECONDS = 's'
    MINUTES = 'm'
    HOURS = 'h'
    MILLIS = 'ms'
    TIMES_S = 'times_s'
    TIMES_M = 'times_m'
    TIMES_H = 'times_h'


METRICS = {Datasets.BGWRITER: {'sbd_checkpoints_timed': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_H},  'sbd_checkpoints_req': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_H},  'sbd_checkpoint_write_time': {'transform': Transformations.TIMEDELTA},  'sbd_checkpoint_sync_time': {'transform': Transformations.TIMEDELTA},  'sbd_buffers_checkpoint': {'transform': Transformations.TIMEDELTA},  'sbd_buffers_clean': {'transform': Transformations.TIMEDELTA},  'sbd_maxwritten_clean': {'transform': Transformations.TIMEDELTA},  'sbd_buffers_backend': {'transform': Transformations.TIMEDELTA},  'sbd_buffers_backend_fsync': {'transform': Transformations.TIMEDELTA},  'sbd_buffers_alloc': {'transform': Transformations.TIMEDELTA}},  Datasets.CONNS: {},  Datasets.DB: {'sdd_xact_commit': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sdd_xact_rollback': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sdd_blks_hit': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sdd_blks_read': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'cache_hit_pct': {'transform': Transformations.PERCENTAGE,  'key': 'sdd_blks_hit',  'sum_keys': [
                                              'sdd_blks_read', 'sdd_blks_hit']}, 
               'sdd_temp_files': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sdd_temp_bytes': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.MB_M},  'sdd_blk_read_time': {'transform': Transformations.TIMEDELTA,  'precision': 3},  'sdd_blk_write_time': {'transform': Transformations.TIMEDELTA,  'precision': 3}}, 
 Datasets.INDEX: {'iud_scan': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'iud_tup_read': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'iud_tup_fetch': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M}},  Datasets.KPI: {'kpi_tps': {'transform': Transformations.TIMEDELTA},  'kpi_rollbacks': {'transform': Transformations.TIMEDELTA},  'kpi_blks_read': {'transform': Transformations.TIMEDELTA},  'kpi_blks_hit': {'transform': Transformations.TIMEDELTA},  'kpi_temp_bytes': {'transform': Transformations.TIMEDELTA},  'kpi_wal_location_b': {'transform': Transformations.TIMEDELTA},  'kpi_seq_scans': {'transform': Transformations.TIMEDELTA},  'kpi_ins': {'transform': Transformations.TIMEDELTA},  'kpi_upd': {'transform': Transformations.TIMEDELTA},  'kpi_del': {'transform': Transformations.TIMEDELTA},  'kpi_sproc_calls': {'transform': Transformations.TIMEDELTA},  'kpi_blk_read_time': {'transform': Transformations.TIMEDELTA},  'kpi_blk_write_time': {'transform': Transformations.TIMEDELTA}},  Datasets.LOAD: {'xlog_location_b': {'unit': Units.BYTE,  'transform': Transformations.TIMEDELTA,  'unit_out': Units.BYTES_S}},  Datasets.SCHEMAS: {'sud_sproc_calls': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sud_seq_scans': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sud_idx_scans': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sud_tup_ins': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sud_tup_upd': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M},  'sud_tup_del': {'transform': Transformations.TIMEDELTA,  'unit_out': Units.TIMES_M}},  Datasets.SPROCS: {'sp_calls': {'transform': Transformations.TIMEDELTA},  'sp_self_time': {'transform': Transformations.TIMEDELTA},  'sp_total_time': {'transform': Transformations.TIMEDELTA},  'sp_avg_runtime_s': {'transform': Transformations.DERIVATIVE,  'dividend': 'sp_total_time',  'divisor': 'sp_calls',  'unit_out': 's'}},  Datasets.TABLE: {'tsd_seq_scans': {'transform': Transformations.TIMEDELTA},  'tsd_index_scans': {'transform': Transformations.TIMEDELTA}},  Datasets.TABLEIO: {'tio_heap_read': {'transform': Transformations.TIMEDELTA},  'tio_heap_hit': {'transform': Transformations.TIMEDELTA},  'tio_idx_read': {'transform': Transformations.TIMEDELTA},  'tio_idx_hit': {'transform': Transformations.TIMEDELTA}}}

class Conversions:

    @staticmethod
    def value_pretty(value):
        if value < 1:
            return str(round(value, 2))
        if value < 1000:
            return str(value)
        if value < 1000000:
            return str(round(value / 1000, 1)) + 'k'
        if value < 1000000000:
            return str(round(value / 1000000, 1)) + 'mio'

    @staticmethod
    def convert_units(value, unit_in, unit_out, precision=0):
        """ Base units are 1s, 1 byte, bytes/min, 1/min """
        logging.debug('convert_units(%s,%s,%s)', value, unit_in, unit_out)
        if not unit_in:
            unit_in = Units.VALUE
        scale_in = 1
        scale_out = 1
        if unit_in == Units.VALUE:
            if unit_out == Units.VALUE_PRETTY:
                return Conversions.value_pretty(value)
        if unit_in == Units.KB:
            scale_in = 1024
        elif unit_in == Units.MB:
            scale_in = 1048576
        if unit_out == Units.KB:
            scale_out = 1024
        else:
            if unit_out == Units.MB:
                scale_out = 1048576
            if unit_in == Units.MILLIS:
                scale_in = 0.001
            else:
                if unit_in == Units.TIMES_M:
                    scale_in = 60
                else:
                    if unit_in == Units.MINUTES:
                        scale_in = 60
                    else:
                        if unit_in == Units.TIMES_H:
                            scale_in = 3600
                        elif unit_in == Units.HOURS:
                            scale_in = 3600
                        if unit_out == Units.TIMES_M:
                            scale_out = 60
                        else:
                            if unit_out == Units.MINUTES:
                                scale_out = 60
                            else:
                                if unit_out == Units.TIMES_H:
                                    scale_out = 3600
                                elif unit_out == Units.HOURS:
                                    scale_out = 3600
        if precision > 0:
            return round(value * scale_in / scale_out, precision)
        else:
            return round(value * scale_in / scale_out)


class DeltaEngine(object):
    __doc__ = "Calculates 'diffs' between time-ordered datasets for the defined keys. Keeps a cache of objectsimple_deltas"

    def __init__(self, host_name, dataset_name, key_columns=None, simple_deltas=False):
        self.metric_store = defaultdict(OrderedDict)
        self.host_name = host_name
        self.dataset_name = dataset_name
        self.key_columns = key_columns if key_columns else []
        self.tz_column_name = SUPPORTED_DATASETS[dataset_name][1] + 'timestamp'
        self.simple_deltas = simple_deltas
        self.max_items = 100

    def add_datarow_to_queue_if_not_there(self, key_tuple, dr):
        if len(self.metric_store[key_tuple]) == 0:
            self.metric_store[key_tuple][dr[self.tz_column_name]] = dr
        elif dr[self.tz_column_name] not in self.metric_store[key_tuple]:
            self.metric_store[key_tuple][dr[self.tz_column_name]] = dr
        return len(self.metric_store[key_tuple])

    def calculate_simple_delta(self, dict1, dict2, key):
        logging.debug('[DeltaEngine][%s][%s] calculating simple delta for key "%s". dict1: %s, dict2: %s ', self.host_name, self.dataset_name, key, dict1[key], dict2[key])
        delta = dict2[key] - dict1[key]
        if type(dict2[key]) == datetime.datetime:
            return delta.total_seconds()
        if delta < 0:
            logging.warning('[%s][%s] negative value or time delta found for key "%s". means stats reset mostly.  (%s - %s)', self.dataset_name, self.host_name, key, dict2[key], dict1[key])
            return
        return delta

    def calculate_percentage(self, dict1, dict2, key, sum_keys):
        logging.debug('[DeltaEngine][%s][%s] calculating percentage for key="%s", sum_keys="%s"', self.host_name, self.dataset_name, key, sum_keys)
        sum = 0
        for k in sum_keys:
            ret = self.calculate_simple_delta(dict1, dict2, k)
            if ret > 0:
                sum += ret
                continue

        return self.calculate_simple_delta(dict1, dict2, key) / sum * 100

    def calculate_derivative(self, dict1, dict2, dividend_key, divisor_key):
        logging.debug('[DeltaEngine][%s][%s] calculating derivative for (%s / %s). (%s - %s) / (%s - %s)', self.host_name, self.dataset_name, dividend_key, divisor_key, dict2[dividend_key], dict1[dividend_key], dict2[divisor_key], dict1[divisor_key])
        dividend_delta = dict2[dividend_key] - dict1[dividend_key]
        divisor_delta = dict2[divisor_key] - dict1[divisor_key]
        if type(dict1[divisor_key]) == datetime.datetime:
            divisor_delta = divisor_delta.total_seconds()
        if dividend_delta < 0 or divisor_delta < 0:
            logging.warning('[DeltaEngine][%s][%s] negative value or time delta found for (%s / %s). means stats reset mostly. (%s - %s) / (%s - %s)', self.dataset_name, self.host_name, dividend_key, divisor_key, dict2[dividend_key], dict1[dividend_key], dict2[divisor_key], dict1[divisor_key])
            return
        if divisor_delta == 0:
            return 0
        return dividend_delta / divisor_delta

    def add_snapshot_and_return_transformed(self, data):
        ret_dataset = []
        for dr in data:
            ret_row = dr.copy()
            for field, props in METRICS.get(self.dataset_name, {}).items():
                if field not in dr:
                    if not props.get('transform'):
                        logging.warning('[DeltaEngine][%s][%s] column %s not found from input data (%s)', self.host_name, self.dataset_name, field, dr)
                        continue
                    transformed_val = dr.get(field)
                    if props.get('transform') in [Transformations.TIMEDELTA, Transformations.DERIVATIVE, Transformations.PERCENTAGE]:
                        if dr.get(self.tz_column_name) is None:
                            raise Exception('No timestamp column ({})  found from input data! dataset={}, data={}'.format(self.tz_column_name, self.dataset_name, dr))
                        key_tuple = self.get_key_tuple(dr, self.key_columns)
                        item_count = self.add_datarow_to_queue_if_not_there(key_tuple, dr)
                        if item_count > 1:
                            logging.debug('[DeltaEngine][%s][%s] calculating delta for "%s"', self.host_name, self.dataset_name, field)
                            metrics_as_list = list(self.metric_store[key_tuple].values())
                            prev_dr = metrics_as_list[(-2)]
                            cur_dr = metrics_as_list[(-1)]
                            if props.get('transform') == Transformations.TIMEDELTA and self.simple_deltas:
                                transformed_val = self.calculate_simple_delta(prev_dr, cur_dr, field)
                            else:
                                if props.get('transform') == Transformations.PERCENTAGE:
                                    transformed_val = self.calculate_percentage(prev_dr, cur_dr, props['key'], props['sum_keys'])
                                else:
                                    dividend_column = field
                                    divisor_column = self.tz_column_name
                                    if props.get('transform') == 'derivative':
                                        dividend_column = props.get('dividend')
                                        divisor_column = props.get('divisor')
                                    transformed_val = self.calculate_derivative(prev_dr, cur_dr, dividend_column, divisor_column)
                        else:
                            transformed_val = None
                    if transformed_val:
                        if props.get('unit_out') and not config.get('features', {}).get('simple_deltas'):
                            transformed_val = Conversions.convert_units(transformed_val, props.get('unit'), props.get('unit_out'))
                    if props.get('out_name'):
                        ret_row[props['out_name']] = transformed_val
                else:
                    ret_row[field] = transformed_val

            ret_dataset.append(ret_row)

        return ret_dataset

    def get_key_tuple(self, datarow, key_columns):
        key = []
        for k in key_columns:
            key.append(datarow[k])

        return tuple(key)

    def transform_set(self, datarows, key_colums):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    import arrow
    print(Conversions.convert_units(2, None, Units.TIMES_M))
    print(Conversions.convert_units(12345, Units.MILLIS, Units.SECONDS, 2))
    print(Conversions.convert_units(12345, Units.MILLIS, Units.MINUTES, 2))
    print(Conversions.convert_units(12345, Units.MILLIS, Units.HOURS, 5))
    exit()
    d1 = [
     {'sdd_timestamp': arrow.get('2015-12-08 18:23:28.910774+01').datetime,  'sdd_numbackends': 1, 
      'sdd_xact_commit': 1}]
    d2 = [
     {'sdd_timestamp': arrow.get('2015-12-08 18:24:28.910774+01').datetime,  'sdd_numbackends': 2, 
      'sdd_xact_commit': 20}]
    de = DeltaEngine('local', Datasets.DB)
    print(de.calculate_derivative(d2[0], d1[0], 'sdd_xact_commit', 'sdd_numbackends'))