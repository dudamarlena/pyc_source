# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: F:\build\scripts-2.7\vm.py
# Compiled at: 2014-12-01 20:46:56
import sys
from vm.killer import kill_process
from vm.printer import print_s
from vm.corefuncs import push, pop, clear_s
from vm.math import add, subtract, divide, multiply
from vm.exceptions import VMError
stack = []

def load_program(argv):
    try:
        f = open(argv[1])
    except:
        print 'No files'
        sys.exit(1)

    l = f.read()
    l = l.replace('\n', ' ')
    return l.split()


def exec_prog(l):
    loop = 1
    i = 0
    while loop:
        instruction = l[i]
        if instruction == '01':
            push(i, l, stack)
        elif instruction == '02':
            pop(stack)
        elif instruction == '03':
            print_s(stack)
        elif instruction == '04':
            add(stack)
        elif instruction == '05':
            subtract(stack)
        elif instruction == '06':
            multiply(stack)
        elif instruction == '07':
            divide(stack)
        elif instruction == '08':
            clear_s(stack)
        elif instruction == '09':
            kill_process(l[(i + 1)])
        elif instruction == '00':
            loop = 0
        else:
            try:
                int(instruction, 16)
            except:
                raise VMError('Invalid instruction: ' + instruction)
                loop -= 1

        i += 1


def main(argv):
    l = load_program(argv)
    exec_prog(l)
    return 0


def target(*argv):
    return (
     main, None)


if __name__ == '__main__':
    main(sys.argv)