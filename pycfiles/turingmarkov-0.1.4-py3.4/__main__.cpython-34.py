# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/turingmarkov/__main__.py
# Compiled at: 2015-06-18 10:10:57
# Size of source mod 2**32: 2455 bytes
"""turingmarkov - Turing machine and markov algorithm emulator."""
from .markov import Algorithm
from .turing import build_machine
import pytest, os, sys
VERSION = '0.1.4'
USAGE = 'Usage: turingmarkov command [file]\nAvailable commands:\n    compile markov : make python code from markov algorithm and put to stdout\n    compile turing : make python code from turing machine and put to stdout\n    run markov     : run markov algorithm (from requred file); stdin->stdout\n    run turing     : run turing machine (from requred file); stdin->stdout\n    test           : run internal tests\n    version        : print version and exit\n    help           : print this help and exit'

def load_markov(argv, stdin):
    """Load and return markov algorithm."""
    if len(argv) > 3:
        with open(argv[3]) as (input_file):
            return Algorithm(input_file.readlines())
    else:
        return Algorithm(stdin.readlines())


def load_turing(argv, stdin):
    """Load and return turing machine."""
    if len(argv) > 3:
        with open(argv[3]) as (input_file):
            return build_machine(input_file.readlines())
    else:
        return build_machine(stdin.readlines())


def main(argv, stdin, stdout):
    """Execute, when user call turingmarkov."""
    if len(argv) > 1 and argv[1:3] == ['compile', 'markov']:
        algo = load_markov(argv, stdin)
        print(algo.compile(), file=stdout)
    else:
        if len(argv) == 4 and argv[1:3] == ['run', 'markov']:
            algo = load_markov(argv, stdin)
            for line in stdin:
                print(algo.execute(''.join(line.split())), file=stdout)

        else:
            if len(argv) > 1 and argv[1:3] == ['compile', 'turing']:
                machine = load_turing(argv, stdin)
                print(machine.compile(), file=stdout)
            else:
                if len(argv) == 4 and argv[1:3] == ['run', 'turing']:
                    machine = load_turing(argv, stdin)
                    for line in stdin:
                        print(machine.execute(line), file=stdout)

                else:
                    if len(argv) == 2 and argv[1] == 'test':
                        path = os.path.abspath(os.path.dirname(__file__))
                        argv[1] = path
                        pytest.main()
                    else:
                        if len(argv) == 2 and argv[1] == 'version':
                            print('TuringMarkov', VERSION, file=stdout)
                        else:
                            print(USAGE, file=stdout)
    if not (len(argv) == 2 and argv[1] == 'help'):
        exit(1)


def exec_main():
    """Hook for testability."""
    main(sys.argv, sys.stdin, sys.stdout)