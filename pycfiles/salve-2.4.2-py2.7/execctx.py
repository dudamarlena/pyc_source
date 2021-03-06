# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/context/execctx.py
# Compiled at: 2015-11-06 23:45:35
import salve
from salve import Enum, Singleton, with_metaclass

class ExecutionContext(with_metaclass(Singleton)):
    """
    Identifies the phase of execution, and carries any global or shared data
    from phase to phase.
    """
    phases = Enum('STARTUP', 'PARSING', 'COMPILATION', 'VERIFICATION', 'EXECUTION')

    def __init__(self, startphase=phases.STARTUP):
        self.phase = startphase
        self.vars = {}

    def __str__(self):
        return self.phase

    def __setitem__(self, key, value):
        self.vars[key] = value

    def __getitem__(self, key):
        return self.vars[key]

    def __contains__(self, key):
        return key in self.vars

    def transition(self, newphase, quiet=False):
        if not newphase in self.phases:
            raise AssertionError
            if self.phase == newphase:
                return
            transition_text = quiet or 'SALVE Execution Phase Transition ' + '[%s] -> [%s]' % (
             self.phase, newphase)
            extra = {'hide_salve_context': True}
            salve.logger.debug(transition_text, extra=extra)
        self.phase = newphase