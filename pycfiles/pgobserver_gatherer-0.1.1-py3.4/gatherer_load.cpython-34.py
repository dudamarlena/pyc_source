# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_load.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 3513 bytes
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class LoadGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.LOAD)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.LOAD][0]] * 60
        self.columns_to_store = ['load_timestamp', 'load_host_id', 'load_1min_value', 'load_5min_value',
         'load_15min_value', 'xlog_location', 'xlog_location_mb', 'xlog_location_b']
        self.datastore_table_name = 'monitor_data.host_load'

    def gather_data(self):
        sql_get = "\n            with\n            q_load as (\n              select\n                {load_avgs} as load,\n                pg_current_xlog_location() as xlog_location\n            )\n            select\n              now() as load_timestamp,\n              (q_load.load[1]*100)::int as load_1min_value, -- in old Java gatherer for some reason it's multiplied by 100\n              (q_load.load[2]*100)::int as load_5min_value,\n              (q_load.load[3]*100)::int as load_15min_value,\n              -- q_load.load[1]::double precision as load_1min_value,\n              -- q_load.load[2]::double precision as load_5min_value,\n              -- q_load.load[3]::double precision as load_15min_value,\n              q_load.xlog_location,\n              case\n                when current_setting('server_version_num')::int >= 90200 then\n                  pg_xlog_location_diff(q_load.xlog_location, '0/0')::int8\n                else\n                  null::int8\n              end as xlog_location_b\n            from\n              q_load\n        "
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get.format(load_avgs='(select array[min1, min5, min15]::numeric[] from zz_utils.get_load_average() t(min1, min5, min15))' if self.have_zz_utils else '(select array[null,null, null]::numeric[])'))
        for d in data:
            d['load_host_id'] = self.host_id
            if d['xlog_location_b'] is None:
                d['xlog_location_b'] = self.xlog_location_to_bytes(d['xlog_location'])
                d['xlog_location_mb'] = d['xlog_location_b'] / 1048576
                continue

        return data

    @staticmethod
    def xlog_location_to_bytes(xlog_location):
        """"
        xlog_location - result from Postgres pg_current_xlog_location(), e.g. 2F1/CDABE000
        returns - long int of location converted to megabytes (assuming 1 WAL file = 16MB)

        from 9.2 there's also the pg_xlog_location_diff() function, which one should use
        """
        B_PER_WAL = 16777216
        if not xlog_location:
            return
        splits = xlog_location.split('/')
        splits[1] = splits[1].zfill(8)
        logical_segments = int(splits[0], 16) * 256
        physical_segments = int(splits[1][0:2], 16)
        ret = int((logical_segments + physical_segments) * B_PER_WAL + int(splits[1][2:], 16))
        if ret < 0:
            raise Exception('Invalid xlog calculation: {} => {}'.format(xlog_location, ret))
        return ret