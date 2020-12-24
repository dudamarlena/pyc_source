# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/config/settings.py
# Compiled at: 2014-09-01 07:28:09
import json, os, logging
settings = {'debug': True, 
   'host': 'localhost', 
   'port': 5005, 
   'target_root': '/home/Desktop/GIS', 
   'default_layer_name': 'layer.geotiff', 
   'logging': {'level': logging.INFO, 
               'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
               'datefmt': '%d-%m-%Y | %H:%M:%s'}, 
   'email': {'settings': '/home/vortex/Desktop/LAYERS/email.json', 
             'user': None, 
             'password': None}, 
   'folders': {'config': 'config/', 
               'tmp': '/home/vortex/Desktop/LAYERS/tmp', 
               'data_providers': 'data_providers/', 
               'metadata': 'metadata/', 
               'stats': 'stats/', 
               'geoserver': 'geoserver/', 
               'metadata_templates': 'metadata/templates/', 
               'geoserver_datadir': '/home/vortex/programs/SERVERS/tomcat_geoservers/data/', 
               'distribution': '/home/vortex/Desktop/LAYERS/DISTRIBUTION/'}, 
   'db': {'metadata': {'connection': 'mongodb://localhost:27017/', 
                       'database': 'metadata', 
                       'document': {'layer': 'layer'}}, 
          'spatial': {'dbname': 'pgeo', 
                      'host': 'localhost', 
                      'port': '5432', 
                      'username': 'fenix', 
                      'password': 'Qwaszx', 
                      'schema': 'spatial'}, 
          'stats': {'dbname': 'pgeo', 
                    'host': 'localhost', 
                    'port': '5432', 
                    'username': 'fenix', 
                    'password': 'Qwaszx', 
                    'schema': 'stats'}}, 
   'geoserver': {'geoserver_master': 'http://localhost:9090/geoserver/rest', 
                 'geoserver_slaves': [], 'username': 'admin', 
                 'password': 'geoserver', 
                 'default_workspace': 'fenix', 
                 'default_datastore': 'pgeo'}, 
   'stats': {'db': {'spatial': 'spatial', 
                    'stats': 'stats'}}, 
   'metadata': {}}

def read_config_file_json(filename, folder=''):
    directory = os.path.dirname(os.path.dirname(__file__))
    filename = filename.lower()
    path = directory + '/' + settings['folders']['config'] + settings['folders'][folder]
    extension = '' if '.json' in filename else '.json'
    return json.loads(open(path + filename + extension).read())


def read_template(filename):
    try:
        directory = os.path.dirname(os.path.dirname(__file__))
        filename = filename.lower()
        path = os.path.join(directory, settings['folders']['config'], settings['folders']['metadata_templates'])
        extension = '' if '.json' in filename else '.json'
        return json.loads(open(path + filename + extension).read())
    except Exception as e:
        print e


def set_email_settings():
    print os.path.isfile(settings['email']['settings'])
    if os.path.isfile(settings['email']['settings']):
        settings['email'] = json.loads(open(settings['email']['settings']).read())


set_email_settings()