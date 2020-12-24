# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_project.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *
from render_task import render_task

def render_project(entity, detail, ctx):
    """
            'comment': 'Update project comment',
            'endDate': <DateTime '20321231T18:59:00' at b796b34c>,
            'entityName': 'Project',
            'folderObjectId': 479360,
            'kind': '',
            'name': 'Updated project name',
            'number': 'P479340',
            'objectId': 479340,
            'ownerObjectId': 10160,
            'placeHolder': 0,
            'startDate': <DateTime '20070213T05:00:00' at b7964e0c>,
            'status': '',
            'version': ''}
    """
    p = {'comment': as_string(entity.comment), 
       'endDate': as_datetime(entity.end), 
       'entityName': 'Project', 
       'folderObjectId': as_integer(entity.folder.object_id), 
       'kind': as_string(entity.kind), 
       'name': as_string(entity.name), 
       'number': as_string(entity.number), 
       'objectId': as_integer(entity.object_id), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'parentObjectId': as_integer(entity.parent_id), 
       'placeHolder': as_integer(entity.is_fake), 
       'startDate': as_datetime(entity.start), 
       'status': as_string(entity.status), 
       'version': as_integer(entity.version)}
    if detail & 4096:
        p['_TASKS'] = []
        for task in entity.tasks:
            p['_TASKS'].append(render_task(task, 0, ctx))

    if detail & 512 or detail & 256:
        tm = ctx.type_manager
        if detail & 512:
            p['_ENTERPRISES'] = []
        if detail & 256:
            p['_CONTACTS'] = []
        for assignment in entity.assignments:
            kind = tm.get_type(assignment.child_id)
            if kind == 'Enterprise' and detail & 512:
                p['_ENTERPRISES'].append({'entityName': 'assignment', 'objectId': as_integer(assignment.object_id), 
                   'sourceEntityName': 'Project', 
                   'sourceObjectId': as_integer(assignment.parent_id), 
                   'targetEntityName': 'Enterprise', 
                   'targetObjectId': as_integer(assignment.child_id)})
            elif kind == 'Contacts' and detail & 256:
                p['_CONTACTS'].append({'entityName': 'assignment', 'objectId': as_integer(assignment.object_id), 
                   'sourceEntityName': 'Project', 
                   'sourceObjectId': as_integer(assignment.parent_id), 
                   'targetEntityName': 'Contact', 
                   'targetObjectId': as_integer(assignment.child_id)})

    return render_object(p, entity, detail, ctx)