# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/start.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class StartAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'start'
    __aliases__ = ['eventAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def parse_action_parameters(self):
        pass

    def do_action(self):
        pass

    def do_epilogue(self):
        self.log_message('start')