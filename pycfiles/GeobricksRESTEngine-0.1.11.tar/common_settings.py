# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_rest_engine/geobricks_rest_engine/config/common_settings.py
# Compiled at: 2015-03-19 05:01:01
import logging, os, json
settings = {'settings': {'base_url': '', 
                'logging': {'level': logging.INFO, 
                            'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
                            'datefmt': '%d-%m-%Y | %H:%M:%s'}, 
                'email': {'user': 'user', 
                          'password': 'password'}, 
                'folders': {'tmp': '/home/vortex/Desktop/LAYERS/geobricks/tmp/', 
                            'geoserver_datadir': '/home/vortex/programs/SERVERS/tomcat_geoservers/data/', 
                            'distribution': '/home/vortex/Desktop/LAYERS/geobricks/distribution', 
                            'distribution_sld': '/home/vortex/repos/FENIX-MAPS/geobricks/geobricks_sld/distribution_sld/', 
                            'storage': '/home/vortex/Desktop/LAYERS/geobricks/storage/', 
                            'workspace_layer_separator': ':'}, 
                'db': {'spatial': {'dbname': 'fenix', 
                                   'host': 'localhost', 
                                   'port': '5432', 
                                   'username': 'user', 
                                   'password': 'pwd', 
                                   'schema': 'schema'}}, 
                'storage': {'url': 'localhost', 
                            'user': 'user', 
                            'password': 'password'}, 
                'metadata': {}, 'geoserver': {'geoserver_master': 'http://localhost:9090/geoserver/rest', 
                              'geoserver_slaves': [], 'username': 'admin', 
                              'password': 'geoserver'}}}

def set_email_settings():
    if 'email' in settings['settings']:
        if 'settings' in settings['settings']['email'] and os.path.isfile(settings['settings']['email']['settings']):
            settings['settings']['email'] = json.loads(open(settings['settings']['email']['settings']).read())


set_email_settings()