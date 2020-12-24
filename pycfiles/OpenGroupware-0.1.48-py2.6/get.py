# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/get.py
# Compiled at: 2012-10-12 07:02:39
import os, base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class GetEntityAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'get-entity'
    __aliases__ = ['getEntityAction', 'getEntity']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        kind = self._ctx.type_manager.get_type(self._id).lower()
        if kind == 'Unknown':
            raise CoilsException('Cannot retrieve entity of Unknown type.')
        entity = self._ctx.run_command(('{0}::get').format(kind), id=int(self._id))
        if entity is None:
            raise CoilsException(('Failed to retrieve objectId#{0} via {1}::get.').format(self._id, kind))
        results = XML_Render.render(entity, self._ctx)
        self.wfile.write(results)
        return

    @property
    def result_mimetype(self):
        return 'application/xml'

    def parse_action_parameters(self):
        self._id = self.action_parameters.get('objectId', None)
        if self._id is None:
            self._id = self._ctx.account_id
        else:
            self._id = self.process_label_substitutions(self._id)
        return

    def do_epilogue(self):
        pass