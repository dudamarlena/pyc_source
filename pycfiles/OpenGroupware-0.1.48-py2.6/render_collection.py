# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_collection.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *

def render_collection(entity, detail, ctx):
    """ { 'creation': <DateTime '20100414T13:01:13' at 7f972f740c68>,
          'creatorObjectId': 10100,
          'entityName': 'Folder',
          'folderObjectId': 844520,
          'objectId': 14216643,
          'ownerObjectId': 10100,
          'projectObjectId': 844500,
          'title': '201004'} """
    collection = {'entityName': 'Collection', 'objectId': as_integer(entity.object_id), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'projectObjectId': as_integer(entity.project_id), 
       'comment': as_string(entity.comment), 
       'kind': as_string(entity.kind), 
       'version': as_integer(entity.version), 
       'otp': as_string(entity.auth_token), 
       'davEnabled': as_integer(entity.dav_enabled), 
       'title': as_string(entity.title)}
    if detail & 128:
        tm = ctx.type_manager
        collection['_MEMBERSHIP'] = []
        contents = ctx.run_command('collection::get-assignments', collection=entity)
        for obj in contents:
            collection['_MEMBERSHIP'].append({'entityName': 'collectionAssignment', 'objectId': obj.object_id, 
               'collectionObjectId': entity.object_id, 
               'assignedObjectId': obj.assigned_id, 
               'assignedEntityName': tm.get_type(obj.assigned_id), 
               'sortKey': as_integer(obj.sort_key)})

    return render_object(collection, entity, detail, ctx)