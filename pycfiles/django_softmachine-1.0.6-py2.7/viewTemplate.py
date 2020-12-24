# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/viewTemplate.py
# Compiled at: 2014-05-07 15:25:05
from datetime import datetime
from protoLib.utilsBase import slugify
PROTO_PREFIX = 'prototype.ProtoTable.'

def baseDefinition(pEntity, entityName, viewTitle):
    """ protoEntity: Es la traza de la generacion del protipo  dominio.modelo.entidad  
    """
    viewName = slugify(viewTitle)
    return {'__ptType': 'pcl', 
       'viewEntity': 'prototype.ProtoTable', 
       'viewCode': PROTO_PREFIX + viewName, 
       'protoEntity': entityName, 
       'protoEntityId': pEntity.id, 
       'description': pEntity.description, 
       'jsonField': 'info', 
       'viewIcon': 'icon-proto', 
       'localSort': True, 
       'shortTitle': viewTitle, 
       'updateTime': datetime.now(), 
       'metaVersion': '13.0301', 
       'idProperty': 'id', 
       'fields': [
                {'name': 'id', 
                   'readOnly': True, 
                   'hidden': True, 
                   'type': 'autofield'},
                {'name': 'entity', 
                   'readOnly': True, 
                   'hidden': True},
                {'name': 'entity_id', 
                   'readOnly': True, 
                   'hidden': True, 
                   'prpDefault': pEntity.id},
                {'name': 'info', 
                   'searchable': True, 
                   'readOnly': True, 
                   'hidden': True, 
                   'type': 'jsonfield'},
                {'name': 'smOwningUser', 
                   'readOnly': True, 
                   'type': 'foreigntext'},
                {'name': 'smOwningTeam', 
                   'readOnly': True, 
                   'type': 'foreigntext'},
                {'name': 'smCreatedOn', 
                   'readOnly': True, 
                   'type': 'datetime'}], 
       'detailsConfig': [], 'gridConfig': {'listDisplay': [], 'baseFilter': [], 'searchFields': [
                                     'info'], 
                      'sortFields': [], 'hiddenFields': [
                                     'id', 'info', 'entity_id'], 
                      'readOnlyFields': []}, 
       'formConfig': {'__ptType': 'formConfig', 
                      'items': [
                              {'__ptType': 'fieldset', 
                                 'fsLayout': '2col', 
                                 'items': []}]}}