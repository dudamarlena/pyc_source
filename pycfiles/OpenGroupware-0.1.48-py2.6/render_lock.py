# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_lock.py
# Compiled at: 2012-10-12 07:02:39
from render_object import as_string, as_integer, as_datetime

def render_lock(entity, detail, ctx, favorite_ids=None):
    """ { 'operations': 'dwx',
          'exclusive': 'YES' | 'NO',
          'objectId': 54720,
          'entityName': 'lock',
          'targetEntityName': 'Contact',
          'token': '' } """
    lock = {'entityName': 'lock', 'targetObjectId': as_integer(entity.object_id), 
       'operations': as_string(entity.operations), 
       'exclusive': 'YES' if entity.exclusive == 'Y' else 'NO', 
       'targetEntityName': as_string(ctx.type_manager.get_type(entity.object_id)), 
       'token': as_string(entity.token), 
       'granted': as_integer(entity.granted), 
       'expires': as_integer(entity.expires)}
    return lock