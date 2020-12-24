# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/__main__.py
# Compiled at: 2016-03-05 13:46:56
# Size of source mod 2**32: 2297 bytes
"""Modelmachine - model machine emulator."""
import os, sys, argparse, pytest
from modelmachine.ide import get_program, debug, assemble
__version__ = '0.1.6'

def run_program(args):
    """Get params from args and run file."""
    cpu = get_program(args.filename, args.protect_memory)
    cpu.run()


def run_debug(args):
    """Get params from args and run debug."""
    cpu = get_program(args.filename, args.protect_memory)
    debug(cpu)


def run_tests(args):
    """Run tests."""
    args = args
    path = os.path.abspath(os.path.dirname(__file__))
    sys.argv[1] = path
    pytest.main()


def run_asm(args):
    """Get params from args and run assembler."""
    assemble(args.asm_file, args.machine_file)


def main(argv, stdout):
    """Execute, when user call modelmachine."""
    parser = argparse.ArgumentParser(description='Modelmachine ' + __version__)
    parser.add_argument('-m', '--protect_memory', action='store_true', default=False, help='raise an error, if program tries to read dirty memory')
    subparsers = parser.add_subparsers(title='commands', help='commands of model machine emulator')
    run = subparsers.add_parser('run', help='run program')
    run.add_argument('filename', help='file containing machine code')
    run.set_defaults(func=run_program)
    debug_parser = subparsers.add_parser('debug', help='run program in debug mode')
    debug_parser.add_argument('filename', help='file containing machine code')
    debug_parser.set_defaults(func=run_debug)
    test = subparsers.add_parser('test', help='run internal tests end exit')
    test.set_defaults(func=run_tests)
    asm = subparsers.add_parser('asm', help='assemble model machine program')
    asm.add_argument('asm_file', help='input file containing asm source')
    asm.add_argument('machine_file', help='output file containing machine code')
    asm.set_defaults(func=run_asm)
    args = parser.parse_args(argv[1:])
    if 'func' not in args:
        parser.print_help(stdout)
    else:
        args.func(args)


def exec_main():
    """Hook for testability."""
    main(sys.argv, sys.stdout)


if __name__ == '__main__':
    exec_main()