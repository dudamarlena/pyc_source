# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_sproc.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 7093 bytes
import logging
from pgobserver_gatherer.gatherer_base import GathererBase
from pgobserver_gatherer.id_cache import IdCache
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS

class SprocGatherer(GathererBase):
    DEFAULT_INCLUDE_SCHEMA_PATTERNS = [
     '%']
    DEFAULT_EXCLUDE_SCHEMA_PATTERNS = ['tmp%', 'temp%', 'information_schema', 'pg\\_%']

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.SPROCS)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.SPROCS][0]] * 60
        self.columns_to_store = ['sp_timestamp', 'sp_host_id', 'sp_sproc_id', 'sp_calls',
         'sp_total_time', 'sp_self_time']
        self.datastore_table_name = 'monitor_data.sproc_performance_data'
        self.schemas_to_include = []
        self.schemas_to_exclude = []
        self.cache_table_name = 'monitor_data.sprocs'
        self.cache_id_column = 'sproc_id'
        self.cache_host_id_column = 'sproc_host_id'
        self.cache_key_columns = ['sproc_schema', 'sproc_name']
        self.sproc_id_cache = IdCache(self.cache_table_name, self.cache_id_column, self.cache_key_columns, self.cache_host_id_column, self.host_id)

    def gather_data(self):
        data = []
        if not self.schemas_to_include:
            if not self.schemas_to_exclude:
                self.schemas_to_include, self.schemas_to_exclude = self.get_schemas_to_monitor()
                if not self.schemas_to_include and not self.schemas_to_exclude:
                    logging.warning('[%s][%s] no schemas found to monitor!', self.host_name, self.gatherer_name)
                    return data
        sql_get = "\n            SELECT\n              now() as sp_timestamp,\n              schemaname AS schema_name,\n              funcname  AS function_name,\n              ( select array_to_string(array(select format_type(t,null) from unnest(coalesce(proallargtypes, proargtypes::oid[])) tt (t)),',') ) as func_arguments,\n              array_to_string(proargmodes, ',') AS func_argmodes,\n              calls as sp_calls,\n              self_time::int8 as sp_self_time,\n              total_time::int8 as sp_total_time\n            FROM\n              pg_stat_user_functions f,\n              pg_proc\n            WHERE\n              pg_proc.oid = f.funcid\n              AND schemaname IN ( select name\n                                  from ( SELECT nspname, rank() OVER ( PARTITION BY regexp_replace(nspname, E'_api_r[_0-9]+', '', 'i') ORDER BY nspname DESC)\n                                         FROM pg_namespace\n                                         WHERE nspname LIKE ANY (%(schemas_to_include)s)\n                                           AND NOT nspname LIKE ANY (%(schemas_to_exclude)s)\n                                       ) apis (name, rank)\n                                  where rank <= 4)\n            "
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get, {'schemas_to_include': self.schemas_to_include,  'schemas_to_exclude': self.schemas_to_exclude})
        for d in data:
            d['sp_host_id'] = self.host_id
            d['sproc_name'] = SprocGatherer.formulate_function_name(d)

        return data

    def store_data(self, data):
        logging.info('[%s][%s] running custom store_data() for %s rows', self.host_name, self.gatherer_name, len(data))
        if len(self.sproc_id_cache.cache) == 0:
            self.sproc_id_cache.refresh_from_db()
        new_sprocs = [x for x in data if not self.sproc_id_cache.has((x['schema_name'], x['sproc_name']))]
        if new_sprocs:
            for x in new_sprocs:
                self.sproc_id_cache.put((x['schema_name'], x['sproc_name']))

        for d in data:
            d['sp_sproc_id'] = self.sproc_id_cache.get((d['schema_name'], d['sproc_name']))

        super().store_data(data)

    def get_schemas_to_monitor(self):
        if self.host_id == 0:
            return (SprocGatherer.DEFAULT_INCLUDE_SCHEMA_PATTERNS, SprocGatherer.DEFAULT_EXCLUDE_SCHEMA_PATTERNS)
        exclude_patterns = []
        include_patterns = []
        sql = 'select\n                   scmc_schema_name_pattern as pattern,\n                   scmc_is_pattern_included as is_included\n                 from\n                   sproc_schemas_monitoring_configuration\n                where\n                  scmc_host_id = 0\n                  and not exists (\n                    select 1 from sproc_schemas_monitoring_configuration where scmc_host_id = %(host_id)s)\n                union all\n                select\n                  scmc_schema_name_pattern as pattern,\n                  scmc_is_pattern_included as is_included\n                from\n                  sproc_schemas_monitoring_configuration\n                where\n                  scmc_host_id = %(host_id)s\n                '
        data = datadb.execute(sql, {'host_id': self.host_id})
        for d in data:
            if d['is_included']:
                include_patterns.append(d['pattern'])
            else:
                exclude_patterns.append(d['pattern'])

        logging.info('[%s][%s] include_patterns: %s, exclude_patterns: %s', self.host_name, self.gatherer_name, include_patterns, exclude_patterns)
        return (include_patterns, exclude_patterns)

    @staticmethod
    def formulate_function_name(data_row: dict):
        ret = data_row['function_name'] + '('
        if data_row['func_arguments']:
            args = data_row['func_arguments'].split(',')
            modes = []
            if not data_row['func_argmodes']:
                modes = [
                 'i'] * len(args)
            else:
                modes = data_row['func_argmodes'].replace('o', '').split(',')
            for i in range(len(args)):
                if i > 0:
                    ret += ', '
                ret += modes[i] + ' ' + args[i] if modes[i] == 'i' else args[i]

        ret += ')'
        return ret


if __name__ == '__main__':
    dr = {'func_arguments': 'text,timestamp with time zone',  'function_name': 'drop_old_partitions',  'schema_name': 'z_blocking',  'func_argmodes': None}
    fn = SprocGatherer.formulate_function_name(dr)
    print(fn, fn == 'drop_old_partitions(i text, i timestamp with time zone)')
    dr = {'func_arguments': 'text,text,boolean',  'function_name': 'article_is_ean_created',  'schema_name': 'zcat_api_r15_00_16_2015_04_15_to_be_deleted', 
     'func_argmodes': 'i,o,o'}
    fn = SprocGatherer.formulate_function_name(dr)
    print(fn, fn == 'article_is_ean_created(i text, text, boolean)')