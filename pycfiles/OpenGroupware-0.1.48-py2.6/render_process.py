# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_process.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *

def render_process(entity, detail, ctx):
    """
        '_OBJECTLINKS': [],
         '_PROPERTIES': [],
         'objectId':
         'entityName': 'Route',
         'name':       'XrefrType4DuplicateErrorReport',
         'created':    ,
         'modified':   ,
         'version':    ,
         'ownerObjectId': 10100
         'routeObjectId':
         'priority'

        """
    p = {'entityName': 'Process', 
       'objectId': entity.object_id, 
       'GUID': as_string(entity.uuid), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'routeObjectId': as_integer(entity.route_id), 
       'created': as_datetime(entity.created), 
       'modified': as_datetime(entity.modified), 
       'completed': as_datetime(entity.completed), 
       'parked': as_datetime(entity.parked), 
       'started': as_datetime(entity.started), 
       'version': as_integer(entity.version), 
       'inputMessageUUID': as_string(entity.input_message), 
       'outputMessageUUID': as_string(entity.output_message), 
       'taskObjectId': as_integer(entity.task_id), 
       'priority': as_integer(entity.priority)}
    if detail & 2048:
        try:
            comment = ctx.run_command('process::get-log', process=entity)
            if comment is None:
                p['comment'] = '(Unavailable)'
            else:
                p['comment'] = comment
        except Exception, e:
            p['comment'] = '(Unavailable)'

    if entity.state == 'Q':
        p['state'] = 'queued'
    elif entity.state == 'R':
        p['state'] = 'running'
    elif entity.state == 'F':
        p['state'] = 'failed'
    elif entity.state == 'C':
        p['state'] = 'completed'
    elif entity.state == 'P':
        p['state'] = 'parked'
    elif entity.state == 'I':
        p['state'] = 'initialized'
    elif entity.state == 'Z':
        p['state'] = 'zombie'
    if entity.route is None:
        p['routeName'] = ''
    else:
        p['routeName'] = as_string(entity.route.name)
    flags = []
    if entity.owner_id == ctx.account_id:
        flags.append('OWNER')
    rights = ctx.access_manager.access_rights(entity)
    if 'r' in rights:
        flags.append('READ')
    if 'd' in rights or 'w' in rights:
        flags.append('DELETE')
    if 'w' in rights:
        flags.append('WRITE')
    else:
        flags.append('READONLY')
    p['FLAGS'] = flags
    p['_MESSAGES'] = []
    for message in ctx.run_command('process::get-messages', process=entity):
        p['_MESSAGES'].append({'entityName': 'message', 'processObjectId': entity.object_id, 
           'uuid': as_string(message.uuid), 
           'scope': as_string(message.scope), 
           'mimetype': as_string(message.mimetype), 
           'size': as_integer(message.size), 
           'label': as_string(message.label), 
           'version': as_integer(message.version), 
           'created': as_datetime(message.created), 
           'modified': as_datetime(message.modified)})

    return render_object(p, entity, detail, ctx)