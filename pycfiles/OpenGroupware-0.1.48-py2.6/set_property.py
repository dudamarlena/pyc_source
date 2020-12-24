# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/set_property.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class SetProcessPropertyAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'set-process-property'
    __aliases__ = ['setProcessPropertyAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        self._ctx.property_manager.set_property(self.process, self._namespace, self._attribute, self._value)

    def parse_action_parameters(self):
        self._namespace = self.process_label_substitutions(self.action_parameters.get('namespace'))
        self._attribute = self.process_label_substitutions(self.action_parameters.get('attribute'))
        self._value = self.process_label_substitutions(self.action_parameters.get('value'))

    def do_epilogue(self):
        pass