# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/logic/macro.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import Command, CoilsException

class MacroCommand(Command):

    def __init__(self):
        Command.__init__(self)

    @property
    def descriptor(self):
        raise NotImplementedException('Macro descriptor not implemented.')

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._variables = params.get('variables', {})

    def get_variable(self, name):
        return self._variables(name, None)

    def set_variable(self, name, value):
        self._variables[name] = value

    def verify(self):
        return True

    def do_action(self):
        pass

    def run(self):
        self.parse_action_parameters()
        if self.verify_action():
            self.do_prepare()
            self.do_action()
            self.do_epilogue()
        else:
            raise CoilsException('Macro verification failed.')
        self._result = unicode(self._result)