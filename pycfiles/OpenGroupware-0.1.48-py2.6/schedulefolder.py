# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/schedulefolder.py
# Compiled at: 2012-10-12 07:02:39
import yaml, json
from tempfile import mkstemp
from coils.core import *
from coils.net.foundation import StaticObject
from coils.net import DAVFolder, OmphalosCollection
from signalobject import SignalObject
from workflow import WorkflowPresentation
from scheduleobject import ScheduleObject

class ScheduleFolder(DAVFolder, WorkflowPresentation):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.payload = None
        return

    def supports_PUT(self):
        return False

    def _load_contents(self):
        if isinstance(self.payload, list):
            return True
        self.payload = self.context.run_command('workflow::get-schedule', raise_error=True, timeout=60)
        if isinstance(self.payload, list):
            for entry in self.payload:
                name = ('{0}.json').format(entry['UUID'])
                self.insert_child(name, ScheduleObject(self, name, parameters=self.parameters, request=self.request, context=self.context, entry=entry))

            return True
        return False

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            if self.has_child(name, supports_aliases=False):
                return self.get_child(name, supports_aliases=False)
            if name == '.json':
                return StaticObject(self, '.,json', context=self.context, request=self.request, payload=json.dumps(self.payload), mimetype='application/json')
        raise self.no_such_path()

    def do_PUT(self, request_name):
        """ Allows schedule entries to be made via PUT """
        try:
            payload = self.request.get_request_payload()
            data = json.load(payload)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Content parsing failed')

        raise NotImplementedException('Creating schedule entries via PUT is not implemented; patches welcome.')