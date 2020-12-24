# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_as_ics.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.core.icalendar import Render as ICalendar_Render
from coils.core.vcard import Render as VCard_Render

def filename_for_ics(object_id, version, user_agent_id):
    id_string = str(object_id)
    prefix_a = id_string[-2:]
    prefix_b = id_string[-4:-2]
    return ('cache/ics/{0}/{1}/{2}.{3}.{4}.ics').format(prefix_a, prefix_b, object_id, version, user_agent_id)


def is_ics_cached(object_id, version, user_agent_id):
    return BLOBManager.Exists(filename_for_ics(object_id, version, user_agent_id))


def read_cached_ics(object_id, version, user_agent_id):
    handle = BLOBManager.Open(filename_for_ics(object_id, version, user_agent_id), 'r')
    if handle is None:
        return
    else:
        data = handle.read()
        BLOBManager.Close(handle)
        return data


def cache_ics(object_id, version, user_agent_id, ics):
    filename = filename_for_ics(object_id, version, user_agent_id)
    handle = BLOBManager.Create(filename.split('/'))
    handle.write(ics)
    handle.flush()
    BLOBManager.Close(handle)


class GetObjectAsICalendar(GetCommand):
    __domain__ = 'object'
    __operation__ = 'get-as-ics'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)
        self.disable_access_check()

    def parse_parameters(self, **params):
        if params.has_key('object'):
            self.data = [
             params['object']]
            self.set_single_result_mode()
        elif params.has_key('objects'):
            self.data = params['objects']
            self.set_multiple_result_mode()
        else:
            raise 'No objects provided to command.'
        self._use_cache = params.get('use_cache', True)

    def run(self):
        results = []
        for entity in self.data:
            if self._use_cache:
                ics = read_cached_ics(entity.object_id, entity.version, self._ctx.user_agent_id)
            else:
                ics = None
            if ics is None:
                if isinstance(entity, Contact) or isinstance(entity, Enterprise) or isinstance(entity, Team):
                    ics = VCard_Render.render(entity, self._ctx)
                else:
                    ics = ICalendar_Render.render(entity, self._ctx)
                if ics is not None:
                    if isinstance(ics, list):
                        ics = ics[0]
                    self.log.debug(('Caching ICS representation for objectId#{0} .').format(entity.object_id))
                    cache_ics(entity.object_id, entity.version, self._ctx.user_agent_id, ics)
                    if entity.info:
                        if not (entity.info.file_size == len(ics) and entity.info.version == entity.version):
                            entity.info.update(entity, file_size=len(ics))
                            self._ctx.dirty()
            else:
                self.log.debug(('Using cached ICS representation for objectId#{0}.').format(entity.object_id))
            if ics is not None:
                results.append(ics)

        self.set_return_value(results)
        return