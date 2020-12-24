# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\develop\code\Python\scape\scape\template\project_name\parsers\parser.py
# Compiled at: 2020-04-20 20:46:37
# Size of source mod 2**32: 566 bytes
from scape.core.parser import Parser
from scape.signal.signal import CompoundSignal
from scape.action.action import CompoundAction

class ParserDemo(Parser):

    def __init__(self):
        super().__init__()
        self.hello_signal = CompoundSignal('signal')
        self.add_rule(self.hello_signal, self.rule)
        self.init_activate(self.hello_signal)

    def rule(self, status):
        if status[0]['new'] == 'say':
            if status[1]['new'] == 'hello':
                self.deactivate(self.hello_signal)
                return CompoundAction('hello')