# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_route.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *

def render_route(entity, detail, ctx):
    """
        '_OBJECTLINKS': [],
         '_PROPERTIES': [],
         'comment': '',
         'entityName': 'Route',
         'name':       'XrefrType4DuplicateErrorReport',
         'created':    ,
         'modified':   ,
         'version':    ,
         'ownerObjectId': 10100
        """
    r = {'entityName': 'Route', 
       'objectId': entity.object_id, 
       'name': as_string(entity.name), 
       'comment': as_string(entity.comment), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'created': as_datetime(entity.created), 
       'modified': as_datetime(entity.modified), 
       'version': as_integer(entity.version)}
    flags = []
    if entity.owner_id == ctx.account_id:
        flags.append('SELF')
    rights = ctx.access_manager.access_rights(entity)
    r['FLAGS'] = flags
    return render_object(r, entity, detail, ctx)