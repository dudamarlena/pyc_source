# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/update_route.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.core.logic import UpdateCommand
from keymap import COILS_ROUTE_KEYMAP
from utility import filename_for_route_markup

class UpdateRoute(UpdateCommand):
    __domain__ = 'route'
    __operation__ = 'set'

    def __init__(self):
        UpdateCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.keymap = COILS_ROUTE_KEYMAP
        self.entity = Route
        UpdateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)
        if 'markup' in params:
            self.values['markup'] = params['markup']

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('route::get', id=object_id, access_check=access_check)

    def save_route_markup(self):
        if self.obj.get_markup() is not None:
            handle = BLOBManager.Create(filename_for_route_markup(self.obj), encoding='binary')
            handle.write(self.obj.get_markup())
            BLOBManager.Close(handle)
        return

    def run(self):
        UpdateCommand.run(self)
        if 'markup' in self.values:
            self.obj.set_markup(self.values['markup'])
        if 'keep' in self.values:
            if self.values.get('keep', False):
                value = 'YES'
            else:
                value = 'NO'
            self._ctx.property_manager.set_property(self.obj, 'http://www.opengroupware.us/oie', 'preserveAfterCompletion', value)
        self.save_route_markup()
        self._result = self.obj