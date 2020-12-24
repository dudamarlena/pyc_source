# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/utils/kthlist2pebbling.py
# Compiled at: 2019-11-21 07:56:44
# Size of source mod 2**32: 3381 bytes
"""Utilities to build dimacs encoding of pebbling formulas

Accepts only the kthlist graph format:

ASSUMPTIONS: the graph is given with a line for each vertex, from
sources to a *single sink*.

CNF formulas interesting for proof complexity.
"""
import os, cnfformula, cnfformula.graphs as graphs, sys, argparse

def setup_command_line(parser):
    """Setup general command line options

    Arguments:
    - `parser`: parser to fill with options
    """
    parser.add_argument('--output', '-o', type=(argparse.FileType('w')),
      metavar='<output>',
      default='-',
      help="Output file. The formula is saved\n                        on file instead of being sent to standard\n                        output. Setting '<output>' to '-' is another\n                        way to send the formula to standard output.\n                        (default: -)\n                        ")
    parser.add_argument('--input', '-i', type=(argparse.FileType('r')),
      metavar='<input>',
      default='-',
      help="Input file. The DAG is read from a file instead of being read from\n                        standard output. Setting '<input>' to '-' is\n                        another way to read from standard\n                        input.  (default: -)\n                        ")
    parser.add_argument('--quiet', '-q', action='store_false', dest='verbose', help='Output just the formula with no header.')
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
    G = graphs.readGraph((args.input), 'dag', file_format='kthlist')
    Fstart = cnfformula.PebblingFormula(G)
    Ftransform = args.transformation.transform_cnf(Fstart, args)
    print(Ftransform.dimacs(export_header=(args.verbose)), file=(args.output))


if __name__ == '__main__':
    command_line_utility(sys.argv)