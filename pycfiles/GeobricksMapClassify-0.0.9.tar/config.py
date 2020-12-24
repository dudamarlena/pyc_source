# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_sld/geobricks_mapclassify/config/config.py
# Compiled at: 2015-03-03 10:12:04
import logging
config = {'settings': {'base_url': '', 
                'debug': True, 
                'host': 'localhost', 
                'port': 5974, 
                'logging': {'level': logging.INFO, 
                            'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
                            'datefmt': '%d-%m-%Y | %H:%M:%s'}, 
                'folders': {'distribution_sld': '/home/vortex/repos/FENIX-MAPS/geobricks/geobricks_sld/distribution_sld/'}}}