# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/entity_def.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1749 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Todd Radel <tradel@appdynamics.com>\n'
from . import JsonObject, JsonList

class EntityDefinition(JsonObject):
    FIELDS = {'entity_id':'entityId', 
     'type':'entityType'}
    ENTITY_TYPES = ('ACCOUNT', 'AGENT_CONFIGURATION', 'ALL', 'APPLICATION', 'APPLICATION_COMPONENT',
                    'APPLICATION_COMPONENT_NODE', 'APPLICATION_DIAGNOSTIC_DATA',
                    'AUTOMATIC_LEAK_DETECTION', 'BACKEND', 'BACKEND_DISCOVERY_CONFIG',
                    'BUSINESS_TRANSACTION', 'BUSINESS_TRANSACTION_GROUP', 'CALL_GRAPH_CONFIGURATION',
                    'CUSTOM_EXIT_POINT_DEFINITION', 'CUSTOM_MATCH_POINT_DEFINITION',
                    'CUSTOM_MEMORY_STRUCTURE', 'DASHBOARD', 'ERROR', 'ERROR_CONFIGURATION',
                    'DOT_NET_ERROR_CONFIGURATION', 'PHP_ERROR_CONFIGURATION', 'EUM_CONFIGURATION',
                    'EVENT', 'GLOBAL_CONFIGURATION', 'INCIDENT', 'JMX_CONFIG', 'MACHINE_INSTANCE',
                    'MEMORY_CONFIGURATION', 'NOTIFICATION_CONFIG', 'OBJECT_INSTANCE_TRACKING',
                    'POLICY', 'RULE', 'SQL_DATA_GATHERER_CONFIG', 'STACK_TRACE',
                    'THREAD_TASK', 'TRANSACTION_MATCH_POINT_CONFIG', 'USER', 'GROUP',
                    'ACCOUNT_ROLE', 'WORKFLOW', 'WORKFLOW_EXCUTION', 'POJO_DATA_GATHERER_CONFIG',
                    'HTTP_REQUEST_DATA_GATHERER_CONFIG', 'BASE_PAGE', 'IFRAME', 'AJAX_REQUEST',
                    'INFO_POINT')

    def __init__(self, entity_id=0, entity_type=''):
        self._type = None
        self.id, self.type = entity_id, entity_type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._list_setter('_type', new_type, EntityDefinition.ENTITY_TYPES)