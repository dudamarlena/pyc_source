# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_common/geobricks_common/config/config.py
# Compiled at: 2015-06-11 11:04:00
import logging
config = {'debug': True, 
   'host': 'localhost', 
   'port': 5907, 
   'settings': {'logging': {'level': logging.INFO, 
                            'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
                            'datefmt': '%d-%m-%Y | %H:%M:%s'}, 
                'folders': {'tmp': '/tmp', 
                            'geoserver_datadir': '../tests/data/geoserver_data_dir/', 
                            'storage': '../tests/data/storage/', 
                            'workspace_layer_separator': ':'}, 
                'email': {'user': 'user', 
                          'password': 'password'}, 
                'metadata': {'url_get_metadata_uid': 'http://fenix.fao.org/d3s_dev/msd/resources/metadata/uid/<uid>'}}}