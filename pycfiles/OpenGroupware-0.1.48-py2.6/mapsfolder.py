# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/mapsfolder.py
# Compiled at: 2012-10-12 07:02:39
import json
from coils.core import *
from coils.logic.workflow import ActionMapper
from coils.net import DAVFolder, StaticObject

class MapsFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = {}
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.macros':
            result = []
            for name in ActionMapper.list_macros():
                command = BundleManager.get_command(ActionMapper.get_macro(name))
                result.append(command.descriptor)

            return StaticObject(self, '.macros', context=self.context, request=self.request, payload=json.dumps(result), mimetype='application/json')
        self.no_such_path()