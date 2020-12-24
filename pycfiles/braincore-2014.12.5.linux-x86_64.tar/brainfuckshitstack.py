# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/braincore/examples/brainfuckshitstack.py
# Compiled at: 2014-11-26 03:45:57
from __future__ import print_function
import sys
from braincore import Cell, Stack

class CodeFeeder:

    def __init__(self, script=None):
        self.build_from(script)

    def __iter__(self):
        while self.loc_pointer < self.script_len:
            yield self.script[self.loc_pointer]
            self.loc_pointer += 1

    def __str__(self):
        return self.script

    def __repr__(self):
        return '<ScriptFeeder of "%s">' % self

    def build_from(self, script=None):
        self.script = script or ''
        self.loc_pointer = 0
        self.script_len = len(self.script)

    def jump_ahead(self):
        self.loc_pointer = self.script[self.loc_pointer:].index(']')

    def jump_back(self):
        self.loc_pointer = self.script[:self.loc_pointer].rindex('[') - 1


class BrainFuckShitStack:

    def __init__(self, script, in_fd=sys.stdin, out_fd=sys.stdout):
        self.out_fd = out_fd
        self.in_fd = in_fd
        self.script = script
        self.cell = Cell()
        self.stack = Stack()
        self.code = CodeFeeder(script)
        self.opcodes = {'>': self.cell.right, 
           '<': self.cell.left, 
           '+': self.cell.inc, 
           '-': self.cell.dec, 
           '.': self.print_char, 
           ',': self.read_char, 
           '[': self.jz, 
           ']': self.jnz, 
           '\\': self.push, 
           '/': self.pop, 
           '!': self.pvt}

    def run(self):
        for op in self.code:
            self.opcodes.get(op, lambda : None)()

    def print_char(self):
        self.out_fd.write(self.cell.read())
        self.out_fd.flush()

    def read_char(self):
        self.cell.write(ord(self.in_fd.read(1)))

    def jz(self):
        if not self.cell:
            self.code.jump_ahead()

    def jnz(self):
        if self.cell:
            self.code.jump_back()

    def push(self):
        pushed = self.cell.read()
        self.stack.push(pushed)

    def pop(self):
        popped = ord(self.stack.pop())
        self.cell.write(popped)

    def pvt(self):
        old_stack = str(self.stack)
        old_code = str(self.code)
        self.stack = Stack(old_code)
        self.code.build_from(old_stack[::-1])
        self.code.loc_pointer -= 1


def main():
    import sys

    def print_usage():
        print('usage: %s script.bfss')

    if not len(sys.argv) > 1:
        print_usage()
        exit(1)
    script = open(sys.argv[1]).read()
    sexec = BrainFuckShitStack(script)
    sexec.run()
    print()


if __name__ == '__main__':
    main()