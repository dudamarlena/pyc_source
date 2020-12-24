# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/stats/raster_test.py
# Compiled at: 2014-08-04 05:19:09
from pgeo.stats.raster import Stats
from pgeo.config.settings import settings
layer = {'uid': 'modis:test_bella_guide3'}
geostats = {'statlayercode': 'gaul1', 
   'query_condition': {'column_filter': 'adm1_code', 
                       'select': 'adm1_code, adm1_name ', 
                       'from': 'gaul1_3857', 
                       'where': "adm0_code IN ('68') GROUP BY adm1_code, adm1_name "}, 
   'save_stats': True}
json_stats = {'raster': {'name': 'MODISQ13', 
              'uid': 'trmm:3B42RT.2014010100.7.03hr'}, 
   'vector': {'name': 'gaul0', 
              'type': 'database', 
              'options': {'query_condition': {'select': 'adm0_code, adm0_name', 
                                              'from': '{{SCHEMA}}.gaul0', 
                                              'where': "adm0_code IN ('68', '69') GROUP BY adm0_code, adm0_name "}, 
                          'column_filter': 'adm0_code', 
                          'stats_columns': {'polygon_id': 'adm0_code', 
                                            'label_en': 'adm0_name'}}}, 
   'stats': {'force': True, 
             'save_stats': True, 
             'table_name': 'raster.name_vector.name', 
             'table_definition': '$GEOMETADATA_DEFAULT_PATH/GAUL0/table.sql', 
             'table_insert': {'polygon_id': '', 
                              'label_en': '', 
                              'fromdate': '', 
                              'todate': '', 
                              'dekad': '', 
                              'hist': '', 
                              'max': '', 
                              'min': '', 
                              'sd': ''}, 
             'table_indexes': '$GEOMETADATA_DEFAULT_PATH/GAUL0/table_indexes.sql', 
             'delete_tmp_files': True}}
geostats = Stats(settings)
geostats.zonal_stats(json_stats)