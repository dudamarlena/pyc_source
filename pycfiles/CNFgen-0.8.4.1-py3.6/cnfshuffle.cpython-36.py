# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/utils/cnfshuffle.py
# Compiled at: 2019-11-21 07:56:44
# Size of source mod 2**32: 4032 bytes
"""Cnf formulas shuffling."""
import os, sys, random
from .. import CNF
from . import dimacs2cnf
from ..transformations.shuffle import Shuffle

def command_line_utility(argv=sys.argv):
    try:
        import argparse
    except ImportError:
        print(('Sorry: %s requires `argparse` library, which is missing.\n' % argv[0]), file=(sys.stderr))
        print('Either use Python 2.7 or install it from one of the following URLs:', file=(sys.stderr))
        print(' * http://pypi.python.org/pypi/argparse', file=(sys.stderr))
        print(' * http://code.google.com/p/argparse', file=(sys.stderr))
        print('', file=(sys.stderr))
        exit(-1)

    progname = os.path.basename(argv[0])
    parser = argparse.ArgumentParser(prog=progname, description='\n    Reshuffle the input CNF. Returns a formula logically\n    equivalent to the input with random application of\n    (1) Polarity flips (2) Variables permutation (3) Clauses permutation.\n    ',
      epilog=("\n    For more information type '%s [--help | -h ]'\n    " % progname))
    parser.add_argument('--output', '-o', type=(argparse.FileType('w')),
      metavar='<output>',
      default='-',
      help="Output file. The formula is saved\n                        on file instead of being sent to standard\n                        output. Setting '<output>' to '-' is another\n                        way to send the formula to standard output.\n                        (default: -)\n                        ")
    parser.add_argument('--seed', '-S', metavar='<seed>',
      default=None,
      type=str,
      action='store',
      help='Seed for any random process in the\n                        program. Any python hashable object will\n                        be fine.  (default: current time)\n                        ')
    parser.add_argument('--input', '-i', type=(argparse.FileType('r')),
      metavar='<input>',
      default='-',
      help="Input file. A formula in dimacs format. Setting '<input>' to '-' is\n                        another way to read from standard input.\n                        (default: -)\n                        ")
    parser.add_argument('--no-polarity-flips', '-p', action='store_true', dest='no_polarity_flips', help='No polarity flips')
    parser.add_argument('--no-variables-permutation', '-v', action='store_true', dest='no_variable_permutations', help='No permutation of variables')
    parser.add_argument('--no-clauses-permutation', '-c', action='store_true', dest='no_clause_permutations', help='No permutation of clauses')
    parser.add_argument('--quiet', '-q', action='store_false', default=True, dest='verbose', help='Output just the formula with no header.')
    args = parser.parse_args(argv[1:])
    if hasattr(args, 'seed'):
        if args.seed:
            random.seed(args.seed)
    input_cnf = dimacs2cnf(args.input)
    output_cnf = Shuffle(input_cnf, variable_permutation=(None if not args.no_variable_permutations else list(input_cnf.variables())),
      clause_permutation=(None if not args.no_clause_permutations else list(range(len(input_cnf)))),
      polarity_flip=(None if not args.no_polarity_flips else [1] * len(list(input_cnf.variables()))))
    output_cnf._dimacs_dump_clauses(output=(args.output), export_header=(args.verbose))
    if args.output != sys.stdout:
        args.output.close()


if __name__ == '__main__':
    command_line_utility(sys.argv)