# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/families/counting.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 4267 bytes
"""Implementation of counting/matching formulas
"""
from cnfformula.cnf import CNF
from cnfformula.cmdline import SimpleGraphHelper
from cnfformula.cmdline import register_cnfgen_subcommand
from cnfformula.families import register_cnf_generator
from cnfformula.graphs import enumerate_vertices, neighbors
from itertools import combinations

@register_cnf_generator
def CountingPrinciple(M, p):
    """Generates the clauses for the counting matching principle.
    
    The principle claims that there is a way to partition M in sets of
    size p each.

    Arguments:
    - `M`  : size of the domain
    - `p`  : size of each class

    """
    cnf = CNF()
    name = 'Counting Principle: {0} divided in parts of size {1}.'.format(M, p)
    cnf.header = name + '\n' + cnf.header

    def var_name(tpl):
        return 'Y_{{' + ','.join('{0}'.format(v) for v in tpl) + '}}'

    incidence = [[] for _ in range(M)]
    for tpl in combinations(range(M), p):
        for i in tpl:
            incidence[i].append(tpl)

    for el in range(M):
        edge_vars = [var_name(tpl) for tpl in incidence[el]]
        for cls in CNF.equal_to_constraint(edge_vars, 1):
            cnf.add_clause(cls)

    return cnf


@register_cnf_generator
def PerfectMatchingPrinciple(G):
    """Generates the clauses for the graph perfect matching principle.
    
    The principle claims that there is a way to select edges to such
    that all vertices have exactly one incident edge set to 1.

    Parameters
    ----------
    G : undirected graph

    """
    cnf = CNF()
    name = 'Perfect Matching Principle'
    if hasattr(G, 'name'):
        cnf.header = name + ' of graph:\n' + G.name + '\n' + cnf.header
    else:
        cnf.header = name + '.\n' + cnf.header

    def var_name(u, v):
        if u <= v:
            return 'x_{{{0},{1}}}'.format(u, v)
        else:
            return 'x_{{{0},{1}}}'.format(v, u)

    for v in enumerate_vertices(G):
        edge_vars = [var_name(u, v) for u in neighbors(G, v)]
        for cls in CNF.equal_to_constraint(edge_vars, 1):
            cnf.add_clause(cls)

    return cnf


@register_cnfgen_subcommand
class ParityCmdHelper(object):
    __doc__ = 'Command line helper for Parity Principle formulas\n    '
    name = 'parity'
    description = 'parity principle'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Parity Principle formula

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('N', metavar='<N>', type=int, help='domain size')

    @staticmethod
    def build_cnf(args):
        return CountingPrinciple(args.N, 2)


@register_cnfgen_subcommand
class PMatchingCmdHelper(object):
    __doc__ = 'Command line helper for Perfect Matching Principle formulas\n    '
    name = 'matching'
    description = 'perfect matching principle'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Perfect Matching Principle formula

        Arguments:
        - `parser`: parser to load with options.
        """
        SimpleGraphHelper.setup_command_line(parser)

    @staticmethod
    def build_cnf(args):
        G = SimpleGraphHelper.obtain_graph(args)
        return PerfectMatchingPrinciple(G)


@register_cnfgen_subcommand
class CountingCmdHelper:
    __doc__ = 'Command line helper for Counting Principle formulas\n    '
    name = 'count'
    description = 'counting principle'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Counting Principle formula

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('M', metavar='<M>', type=int, help='domain size')
        parser.add_argument('p', metavar='<p>', type=int, help='size of the parts')

    @staticmethod
    def build_cnf(args):
        """Build an Counting Principle formula according to the arguments

        Arguments:
        - `args`: command line options
        """
        return CountingPrinciple(args.M, args.p)