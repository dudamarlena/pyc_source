# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/cloudmesh/rest/settings.py
# Compiled at: 2017-04-12 13:00:41
cluster = {'schema': {'frontend': {'type': 'objectid', 
                           'data_relation': {'resource': 'node', 
                                             'field': '_id', 
                                             'embeddable': True}}, 
              'computenodes': {'type': 'list', 
                               'schema': {'type': 'objectid', 
                                          'data_relation': {'resource': 'node', 
                                                            'field': '_id', 
                                                            'embeddable': True}}}}}
node = {'schema': {'name': {'type': 'string'}, 
              'label': {'type': 'string'}, 
              'ncpu': {'type': 'integer'}, 
              'RAM': {'type': 'string'}, 
              'disk': {'type': 'string'}, 
              'NIC': {'type': 'list', 
                      'schema': {'type': 'objectid', 
                                 'data_relation': {'resource': 'nic', 
                                                   'field': '_id', 
                                                   'embeddable': True}}}}}
nic = {'schema': {'name': {'type': 'string'}, 
              'mac': {'type': 'string'}, 
              'IP': {'type': 'string'}}}
eve_settings = {'MONGO_HOST': 'localhost', 
   'MONGO_DBNAME': 'testing', 
   'RESOURCE_METHODS': [
                      'GET', 'POST', 'DELETE'], 
   'BANDWIDTH_SAVER': False, 
   'DOMAIN': {'cluster': cluster, 
              'node': node, 
              'nic': nic}}