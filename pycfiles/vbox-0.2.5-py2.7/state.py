# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\vm\state.py
# Compiled at: 2013-03-15 12:05:06
"""Vm power state maneger - running, off, saved, etc."""
from . import base

class State(object):
    vm = None
    cli = property(lambda s: s.vm.cli)
    pause = lambda s: s.cli.manage.controlvm.pause(s.vm.name)
    resume = lambda s: s.cli.manage.controlvm.resume(s.vm.name)
    reset = lambda s: s.cli.manage.controlvm.reset(s.vm.name)
    powerOff = lambda s, *a, **kw: s.vm.powerOff(*a, **kw)
    start = lambda s, *a, **kw: s.vm.start(*a, **kw)
    knownStates = ('running', 'paused', 'poweroff')

    def __init__(self, vm):
        super(State, self).__init__()
        self.vm = vm

    @property
    def val(self):
        rv = self.vm.getProp('VMState')
        assert rv in self.knownStates, repr(rv)
        return rv

    for name in knownStates:
        locals()[name] = (lambda X: property(lambda s: s.val == X))(name)

    del name