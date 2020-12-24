# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/delete_route.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from coils.core import *
from coils.foundation import *
from coils.core.logic import DeleteCommand
from utility import *

class DeleteRoute(DeleteCommand):
    __domain__ = 'route'
    __operation__ = 'delete'

    def run(self):
        source = BLOBManager.Open(filename_for_route_markup(self.obj), 'rb', encoding='binary')
        target = BLOBManager.Create(filename_for_deleted_route_markup(self.obj), encoding='binary')
        if source is not None and target is not None:
            shutil.copyfileobj(source, target)
            BLOBManager.Close(source)
            BLOBManager.Close(target)
            DeleteCommand.run(self)
        elif source is None:
            raise CoilsException(('No route markup to delete for routeId#{0}').format(self.obj.object_id))
        else:
            raise CoilsException(('Unable to archive route markup for routeId#{0}').format(self.obj.object_id))
        return