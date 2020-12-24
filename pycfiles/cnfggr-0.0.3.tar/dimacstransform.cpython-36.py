# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/utils/dimacstransform.py
# Compiled at: 2019-11-21 07:56:44
# Size of source mod 2**32: 3075 bytes
__doc__ = 'CNF transformation, it increases the hardness of a CNF.\n\nThis is the implementation of a command line utility that transform\nCNF files in DIMACS format into new  CNFs\n\nUtilities to apply to a dimacs CNF file, a transformation which\nincrease the hardness of the formula\n\nAccept a cnf in dimacs format in input\n'
import os
from . import dimacs2cnf
import sys, argparse, cnfformula

def setup_command_line(parser):
    """Setup general command line options

    Arguments:
    - `parser`: parser to fill with options
    """
    parser.add_argument('--input', '-i', type=(argparse.FileType('r')),
      metavar='<input>',
      default='-',
      help="Input file. The input formula is read as a dimacs CNF file file\n                        instead of standard input. Setting '<input>'\n                        to '-' is another way to read from standard\n                        input. (default: -) ")
    parser.add_argument('--output', '-o', type=(argparse.FileType('w')),
      metavar='<output>',
      default='-',
      help="Output file. The formula is saved\n                        on file instead of being sent to standard\n                        output. Setting '<output>' to '-' is another\n                        way to send the formula to standard output.\n                        (default: -)\n                        ")
    parser.add_argument('--quiet', '-q', action='store_false', default=True, dest='verbose', help='Output just the formula with no header.')
    from cnfformula import transformations
    from cnfformula.cmdline import is_cnf_transformation_subcommand
    from cnfformula.cmdline import find_methods_in_package
    subparsers = parser.add_subparsers(title='Available transformation', metavar='<transformation>')
    for sc in find_methods_in_package(transformations, is_cnf_transformation_subcommand,
      sortkey=(lambda x: x.name)):
        p = subparsers.add_parser((sc.name), help=(sc.description))
        sc.setup_command_line(p)
        p.set_defaults(transformation=sc)


import signal

def signal_handler(insignal, frame):
    if not insignal != None:
        raise AssertionError
    elif not frame != None:
        raise AssertionError
    print('Program interrupted', file=(sys.stderr))
    sys.exit(-1)


signal.signal(signal.SIGINT, signal_handler)

def command_line_utility(argv=sys.argv):
    parser = argparse.ArgumentParser(prog=(os.path.basename(argv[0])))
    setup_command_line(parser)
    args = parser.parse_args(argv[1:])
    F = dimacs2cnf(args.input)
    G = args.transformation.transform_cnf(F, args)
    print((G.dimacs(args.verbose)), file=(args.output))


if __name__ == '__main__':
    command_line_utility(sys.argv)