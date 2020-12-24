# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_metadata_manager/geobricks_metadata_manager/config/config.py
# Compiled at: 2014-12-19 12:52:04
import logging
config = {'settings': {'debug': True, 
                'host': 'localhost', 
                'port': 5904, 
                'logging': {'level': logging.INFO, 
                            'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
                            'datefmt': '%d-%m-%Y | %H:%M:%s'}, 
                'metadata': {'url_create_metadata': '//exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources/metadata', 
                             'url_get_metadata_uid': '//exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources/metadata/uid/<uid>', 
                             'url_get_metadata': '//exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources/metadata/uid/<uid>', 
                             'url_get_full_metadata': '//exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources/metadata/uid/<uid>?full=true&dsd=true', 
                             'url_create_coding_system': '//exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources', 
                             'url_data_coding_system': '://exldvsdmxreg1.ext.fao.org:7788/v2/msd/resources/data/uid/<uid>'}}}