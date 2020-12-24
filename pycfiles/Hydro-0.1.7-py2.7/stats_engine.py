# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/stats_engine.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'yanivshalev'
from hydro.common.configurator import Configurator

class StatsEngine(object):
    _stats = {}

    def __init__(self):
        if Configurator.USE_STATS_DB:
            from connectors.mysql import MySqlConnector
            params = {'connection_type': 'connection_string', 
               'connection_string': Configurator.DATABASES['stats']['HOST'], 
               'db_name': Configurator.DATABASES['stats']['NAME'], 
               'db_user': Configurator.DATABASES['stats']['USER'], 
               'db_password': Configurator.DATABASES['stats']['PASSWORD']}
            self._conn = MySqlConnector(params)
            self.gather_statistics = self._gather_statistics
        else:
            self.gather_statistics = lambda x, y: None

    def _gather_statistics(self, source_id, segment_id):
        keys = Configurator.OPTIMIZER_STATISTICS['ALL'].keys()
        res = self._conn.execute(("SELECT {0} FROM {1} WHERE source_id = '{2}' and segment_id = '{3}' ").format((',').join(keys), 'source_statistics', source_id, segment_id))
        return res


stats_engine = StatsEngine()