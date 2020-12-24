# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/datastore_viewer/presentation/ui/api/encoder.py
# Compiled at: 2020-03-26 19:39:46
# Size of source mod 2**32: 2785 bytes
import base64, datetime
from typing import List
from typing import Optional
from google.cloud import datastore
from google.cloud.datastore import Entity

class DataStoreEntityJSONEncoder:

    def _property_type_checker(self, prop):
        if isinstance(prop, str):
            return 'string'
        if isinstance(prop, bool):
            return 'boolean'
        if isinstance(prop, int):
            return 'integer'
        if isinstance(prop, float):
            return 'float'
        if isinstance(prop, datetime.datetime):
            return 'timestamp'
        if isinstance(prop, datastore.Key):
            return 'key'
        if isinstance(prop, bytes):
            return 'blob'
        if isinstance(prop, list) or isinstance(prop, set):
            return 'array'
        if isinstance(prop, dict):
            return 'embedded'
        if prop is None:
            return 'null'
        return 'unknown'

    def _array_value_encode(self, value):
        value_type, value = self._property_encode(value)
        return {'value_type':value_type,  'value':value}

    def _property_encode(self, property_value):
        value = property_value
        value_type = self._property_type_checker(property_value)
        if value_type == 'key':
            value = property_value.path
        else:
            if value_type == 'blob':
                value = base64.b64encode(property_value).decode('utf-8')
            else:
                if value_type == 'array':
                    value = [self._array_value_encode(v) for v in value]
                else:
                    if value_type == 'embedded':
                        value = {'properties': DataStoreEntityJSONEncoder().encode(value, None)['entity']['properties']}
        return (
         value_type, value)

    def encode(self, entity: Entity, property_names: Optional[List[str]]):
        entity_dict = {'entity':{'key':{'partitionId':{'projectId': entity.key.project if (entity and entity.key) else None}, 
           'path':entity.key.path if entity and entity.key else None}, 
          'properties':[]}, 
         'URLSafeKey':entity._serialized_key if hasattr(entity, '_serialized_key') else None}
        for prop_name in entity.keys():
            value_type, value = self._property_encode(entity.get(prop_name))
            entity_dict['entity']['properties'].append({'property_name':prop_name, 
             'value_type':value_type, 
             'value':value, 
             'index':prop_name in property_names if property_names else None})

        return entity_dict