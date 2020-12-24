# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/hookbox/output_wrapper.py
# Compiled at: 2012-07-04 04:55:04
import sys

class OutputWrapper(object):

    def __init__(self, outputter, orig):
        self.outputter = outputter
        self.orig = orig

    def write(self, data):
        self.outputter.write(self.orig, data)

    def __getattr__(self, key):
        return getattr(self.orig, key)


class Outputter(object):

    def __init__(self, stdout):
        self.observers = []
        self.stdout = stdout
        self.buffer = ''
        self.locked = False

    def add_observer(self, observer):
        self.observers.append(observer)

    def do_write(self):
        if '\n' in self.buffer:
            out, self.buffer = self.buffer.rsplit('\n', 1)
            for observer in self.observers:
                observer(out + '\n')

        self.locked = False

    def _print(self, *args):
        self.stdout.write((' ').join([ str(a) for a in args ]) + '\n')

    def write(self, target, data):
        target.write(data)
        self.buffer += data
        if not self.locked:
            self.locked = True
            eventlet.spawn(self.do_write)


outputter = Outputter(sys.stdout)
sys.stdout = OutputWrapper(outputter, sys.stdout)
sys.stderr = OutputWrapper(outputter, sys.stderr)
import eventlet