# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/objinfomanager.py
# Compiled at: 2012-10-12 07:02:39
import traceback, os
from typemanager import TypeManager
from coils.foundation import ObjectInfo, BLOBManager
from exception import CoilsException
KINDS_WITH_FILESIZE = ('Document', 'note', 'Note')
KINDS_WITH_ICALENDAR = ('Contact', 'Enterprise', 'Team', 'Task', 'note', 'Note', 'Appointment')

class ObjectInfoManager(object):
    __slots__ = ('_ctx', '_log', '_srv')

    def __init__(self, ctx, log=None, service=None):
        self._ctx = ctx
        self._log = log
        self._srv = service

    @staticmethod
    def Repair(entity, ctx, log=None, service=None):
        om = ObjectInfoManager(ctx, log=log, service=service)
        if om.repair(entity=entity):
            ctx.dirty()
            return True
        return False

    def repair(self, object_id=None, entity=None):
        if object_id:
            entity = self._ctx.type_manager.get_entity(object_id, repair_enabled=False)
        elif entity:
            if hasattr(entity, 'object_id'):
                object_id = entity.object_id
            else:
                return False
        elif object_id is None and entity is None:
            raise CoilsException('Either an "object_id" or an "entity" must be specified for ObjectInfo repair.')
        else:
            return False
        info = self._ctx.db_session().query(ObjectInfo).filter(ObjectInfo.object_id == object_id).all()
        if info:
            info = info[0]
        else:
            kind = self._ctx.type_manager.deep_search_for_type(object_id)
            if kind:
                if kind == 'Unknown':
                    self._log.debug(('Type of objectId#{0} not found.').format(object_id))
                    return False
                kind = TypeManager.translate_kind_to_legacy(kind)
                info = ObjectInfo(object_id, kind)
                self._ctx.db_session().add(info)
            else:
                return False
        if entity:
            try:
                ics_size = None
                file_size = None
                if entity.__entityName__ in KINDS_WITH_FILESIZE:
                    file_size = entity.file_size
                    if file_size is None and entity.__entityName__.lower() == 'note':
                        handle = self._ctx.run_command('note::get-handle', id=entity.object_id)
                        handle.stream.seek(0, os.SEEK_END)
                        entity.file_size = handle.tell()
                        file_size = entity.file_size
                        BLOBManager.Close(handle)
                else:
                    file_size = None
                if entity.__entityName__ in KINDS_WITH_ICALENDAR:
                    ics = self._ctx.run_command('object::get-as-ics', object=entity)
                    if ics:
                        ics_size = len(ics)
                info.update(entity, file_size=file_size, ics_size=ics_size)
            except UnicodeEncodeError:
                message = ('ObjectId:{0} ({1})\n\nError:{2}').format(entity.object_id, entity.__entityName__, traceback.format_exc())
                if self._ctx.amq_available:
                    self._ctx.send_administrative_notice(category='data', urgency=6, subject='UnicodeEncodeError in ObjectInfo Repair', message=message)
                if self._log:
                    self._log.error(message)
                return False
            except Exception, e:
                if self._log:
                    self._log.exception(e)
                return False

        return True