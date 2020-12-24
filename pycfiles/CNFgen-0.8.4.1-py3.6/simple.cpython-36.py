# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/families/simple.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 3200 bytes
"""Implementation of simple formulas
"""
from cnfformula.cnf import CNF
import cnfformula.cmdline

@cnfformula.cmdline.register_cnfgen_subcommand
class OR(object):
    __doc__ = 'Command line helper for a single clause formula\n    '
    name = 'or'
    description = 'a single disjunction'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for single or of literals

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('P', metavar='<P>', type=int, help='positive literals')
        parser.add_argument('N', metavar='<N>', type=int, help='negative literals')

    @staticmethod
    def build_cnf(args):
        """Build an disjunction

        Arguments:
        - `args`: command line options
        """
        clause = [(True, 'x_{}'.format(i)) for i in range(args.P)] + [(False, 'y_{}'.format(i)) for i in range(args.N)]
        orcnf = CNF([clause])
        orcnf.header = 'Clause with {} positive and {} negative literals\n\n'.format(args.P, args.N) + orcnf.header
        return orcnf


@cnfformula.cmdline.register_cnfgen_subcommand
class AND(object):
    __doc__ = 'Command line helper for a 1-CNF (i.e. conjunction)\n    '
    name = 'and'
    description = 'a single conjunction'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for an and of literals

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('P', metavar='<P>', type=int, help='positive literals')
        parser.add_argument('N', metavar='<N>', type=int, help='negative literals')

    @staticmethod
    def build_cnf(args):
        """Build a conjunction

        Arguments:
        - `args`: command line options
        """
        clauses = [[(True, 'x_{}'.format(i))] for i in range(args.P)] + [[(False, 'y_{}'.format(i))] for i in range(args.N)]
        andcnf = CNF(clauses)
        andcnf.header = 'Singleton clauses: {} positive and {} negative\n\n'.format(args.P, args.N) + andcnf.header
        return andcnf


@cnfformula.cmdline.register_cnfgen_subcommand
class EMPTY(object):
    __doc__ = 'Command line helper for the empty CNF (no clauses)\n    '
    name = 'empty'
    description = 'empty CNF formula'

    @staticmethod
    def setup_command_line(parser):
        pass

    @staticmethod
    def build_cnf(args):
        """Build an empty CNF formula 

        Parameters
        ----------
        args : ignored 
             command line options
        """
        return CNF()


@cnfformula.cmdline.register_cnfgen_subcommand
class EMPTY_CLAUSE(object):
    __doc__ = 'Command line helper for the contradiction (one empty clauses)  \n    '
    name = 'emptyclause'
    description = 'one empty clause'

    @staticmethod
    def setup_command_line(parser):
        pass

    @staticmethod
    def build_cnf(args):
        """Build a CNF formula with an empty clause 

        Parameters
        ----------
        args : ignored 
             command line options
        """
        return CNF([[]])