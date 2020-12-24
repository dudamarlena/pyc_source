# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_as_vevent.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.core.icalendar import Render
from utility import read_cached_vevent, cache_vevent

class GetProcessAsVEvent(GetCommand):
    __domain__ = 'process'
    __operation__ = 'get-as-vevent'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        if params.has_key('object'):
            self.data = [
             params['object']]
        elif params.has_key('objects'):
            self.data = params['objects']
        else:
            raise 'No processes provided to command.'

    def run(self):
        results = []
        for process in self.data:
            ics = read_cached_vevent(process.object_id, process.version)
            if ics is None:
                ics = Render.render(process, self._ctx)
                if ics is not None:
                    self.log.debug(('Caching ProcessId#{0} VEVENT representation.').format(process.object_id))
                    cache_vevent(process.object_id, process.version, ics)
            else:
                self.log.debug(('Using cached ProcessId#{0} VEVENT representation.').format(process.object_id))
            if ics is not None:
                results.append(ics)

        self.set_result(results)
        return