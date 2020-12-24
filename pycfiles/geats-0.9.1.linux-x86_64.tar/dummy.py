# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/virtualmachine/dummy.py
# Compiled at: 2012-08-10 02:26:59
from abstract import AbstractVirtualMachine

class DummyVirtualMachine(AbstractVirtualMachine):

    def _define(self):
        print 'DummyVirtualMachine: Defining', self.name
        self.state = 'stopped'

    def _start(self):
        print 'DummyVirtualMachine: Starting', self.name
        self.state = 'running'

    def _stop(self):
        print 'DummyVirtualMachine: Stopping', self.name
        self.state = 'stopped'

    def _shutdown(self):
        print 'DummyVirtualMachine: ShuttingDown', self.name
        self.state = 'stopped'

    def _undefine(self):
        print 'DummyVirtualMachine: Undefine', self.name
        self.state = 'unknown'

    def get_state(self):
        try:
            return (
             self.state, self.state)
        except AttributeError:
            return ('unknown', 'unknown')