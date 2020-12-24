# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\develop\code\Python\scape\scape\template\project_name\parsers\parser.py
# Compiled at: 2020-04-28 04:54:03
# Size of source mod 2**32: 652 bytes
from scape.core.parser import Parser
from scape.signal.signal import SignalFactory
from scape.action.action import ActionFactory

class ParserDemo(Parser):

    def __init__(self):
        super().__init__()
        self.add_rule(SignalFactory.make('signal'), self.rule)
        self.init_activate(SignalFactory.make('signal'))

    def rule(self):
        signal = self.received_signal()
        status = signal.get_status()
        if signal.get_name() == 'signal':
            if status[0]['new'] == 'say':
                if status[1]['new'] == 'hello':
                    self.deactivate(SignalFactory.make('signal'))
                    return ActionFactory.make('hello')