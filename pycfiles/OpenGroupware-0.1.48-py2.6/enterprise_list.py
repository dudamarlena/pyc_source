# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/enterprise_list.py
# Compiled at: 2012-10-12 07:02:39
import os
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class EnterpriseList(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'list-enterprises'
    __aliases__ = ['listEnterprises', 'listEnterprisesAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        result = self._ctx.run_command('enterprise::list', contexts=[
         self._context_id], properties=[
         Enterprise], limit=self._limit)
        XML_Render.render(result, self._ctx, detail_level=self._detail, stream=self.wfile)

    @property
    def result_mimetype(self):
        return 'application/xml'

    def parse_action_parameters(self):
        self._detail = int(self.action_parameters.get('detailLevel', 65503))
        self._context_id = self.action_parameters.get('contextId', self._ctx.account_id)
        self._context_id = self.process_label_substitutions(self._context_id)
        self._context_id = int(self._context_id)
        self._limit = int(self.action_parameters.get('limit', 65535))

    def do_epilogue(self):
        pass