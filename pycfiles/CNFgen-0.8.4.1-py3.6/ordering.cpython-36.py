# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/families/ordering.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 8410 bytes
"""Implementation of the ordering principle formulas
"""
from cnfformula.cnf import CNF
from cnfformula.cmdline import SimpleGraphHelper
import cnfformula.cmdline, cnfformula.families
from cnfformula.graphs import enumerate_vertices, neighbors
from itertools import combinations, permutations
import networkx

@cnfformula.families.register_cnf_generator
def OrderingPrinciple(size, total=False, smart=False, plant=False, knuth=0):
    """Generates the clauses for ordering principle

    Arguments:
    - `size`  : size of the domain
    - `total` : add totality axioms (i.e. "x < y" or "x > y")
    - `smart` : "x < y" and "x > y" are represented by a single variable (implies totality)
    - `plant` : allow a single element to be minimum (could make the formula SAT)
    - `knuth` : Donald Knuth variant of the formula ver. 2 or 3 (anything else suppress it)
    """
    return GraphOrderingPrinciple(networkx.complete_graph(size), total, smart, plant, knuth)


def varname(v1, v2):
    return 'x_{{{0},{1}}}'.format(v1, v2)


@cnfformula.families.register_cnf_generator
def GraphOrderingPrinciple(graph, total=False, smart=False, plant=False, knuth=0):
    """Generates the clauses for graph ordering principle

    Arguments:
    - `graph` : undirected graph
    - `total` : add totality axioms (i.e. "x < y" or "x > y")
    - `smart` : "x < y" and "x > y" are represented by a single variable (implies `total`)
    - `plant` : allow last element to be minimum (and could make the formula SAT)
    - `knuth` : Don Knuth variants 2 or 3 of the formula (anything else suppress it)
    """
    gop = CNF()
    if total or smart:
        name = 'Total graph ordering principle'
    else:
        name = 'Ordering principle'
    if smart:
        name = name + '(compact representation)'
    else:
        if hasattr(graph, 'name'):
            gop.header = name + '\n on graph ' + graph.name + '.\n\n' + gop.header
        else:
            gop.header = name + '.\n\n' + gop.header
    V = enumerate_vertices(graph)
    iterator = combinations if smart else permutations
    for v1, v2 in iterator(V, 2):
        gop.add_variable(varname(v1, v2))

    for med in range(len(V) - (plant and 1)):
        clause = []
        for lo in range(med):
            if graph.has_edge(V[med], V[lo]):
                clause += [(True, varname(V[lo], V[med]))]

        for hi in range(med + 1, len(V)):
            if not graph.has_edge(V[med], V[hi]):
                continue
            else:
                if smart:
                    clause += [(False, varname(V[med], V[hi]))]
                else:
                    clause += [(True, varname(V[hi], V[med]))]

        gop.add_clause(clause, strict=True)

    if len(V) >= 3:
        if smart:
            for v1, v2, v3 in combinations(V, 3):
                gop.add_clause([(True, varname(v1, v2)),
                 (
                  True, varname(v2, v3)),
                 (
                  False, varname(v1, v3))],
                  strict=True)
                gop.add_clause([(False, varname(v1, v2)),
                 (
                  False, varname(v2, v3)),
                 (
                  True, varname(v1, v3))],
                  strict=True)

        else:
            if total:
                for v1, v2, v3 in combinations(V, 3):
                    gop.add_clause([(False, varname(v1, v2)),
                     (
                      False, varname(v2, v3)),
                     (
                      False, varname(v3, v1))],
                      strict=True)
                    gop.add_clause([(False, varname(v1, v3)),
                     (
                      False, varname(v3, v2)),
                     (
                      False, varname(v2, v1))],
                      strict=True)

            else:
                for v1, v2, v3 in permutations(V, 3):
                    if knuth == 2:
                        if not v2 < v1:
                            if v2 < v3:
                                continue
                            if knuth == 3:
                                if not v3 < v1:
                                    if v3 < v2:
                                        continue
                            gop.add_clause([(False, varname(v1, v2)),
                             (
                              False, varname(v2, v3)),
                             (
                              True, varname(v1, v3))],
                              strict=True)

    if not smart:
        for v1, v2 in combinations(V, 2):
            gop.add_clause([(False, varname(v1, v2)),
             (
              False, varname(v2, v1))],
              strict=True)

        if total:
            for v1, v2 in combinations(V, 2):
                gop.add_clause([(True, varname(v1, v2)),
                 (
                  True, varname(v2, v1))],
                  strict=True)

    return gop


@cnfformula.cmdline.register_cnfgen_subcommand
class OPCmdHelper(object):
    __doc__ = 'Command line helper for Ordering principle formulas\n    '
    name = 'op'
    description = 'ordering principle'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Ordering principle formula

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('N', metavar='<N>', type=int, help='domain size')
        g = parser.add_mutually_exclusive_group()
        g.add_argument('--total', '-t', default=False, action='store_true', help='assume a total order')
        g.add_argument('--smart', '-s', default=False, action='store_true', help="encode 'x<y' and 'x>y' in a single variable (implies totality)")
        g.add_argument('--knuth2', action='store_const', dest='knuth', const=2, help='transitivity axioms: "(i<j)(j<k)->(i,k)" only for j>i,k')
        g.add_argument('--knuth3', action='store_const', dest='knuth', const=3, help='transitivity axioms: "(i<j)(j<k)->(i,k)" only for k>i,j')
        parser.add_argument('--plant', '-p', default=False, action='store_true', help='allow a minimum element')

    @staticmethod
    def build_cnf(args):
        """Build an Ordering principle formula according to the arguments

        Arguments:
        - `args`: command line options
        """
        return OrderingPrinciple(args.N, args.total, args.smart, args.plant, args.knuth)


@cnfformula.cmdline.register_cnfgen_subcommand
class GOPCmdHelper(object):
    __doc__ = 'Command line helper for Graph Ordering principle formulas\n    '
    name = 'gop'
    description = 'graph ordering principle'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Graph ordering principle formula

        Arguments:
        - `parser`: parser to load with options.
        """
        g = parser.add_mutually_exclusive_group()
        g.add_argument('--total', '-t', default=False, action='store_true', help='assume a total order')
        g.add_argument('--smart', '-s', default=False, action='store_true', help="encode 'x<y' and 'x>y' in a single variable (implies totality)")
        g.add_argument('--knuth2', action='store_const', dest='knuth', const=2, help='transitivity axioms: "(i<j)(j<k)->(i,k)" only for j>i,k')
        g.add_argument('--knuth3', action='store_const', dest='knuth', const=3, help='transitivity axioms: "(i<j)(j<k)->(i,k)" only for k>i,j')
        parser.add_argument('--plant', '-p', default=False, action='store_true', help='allow a minimum element')
        SimpleGraphHelper.setup_command_line(parser)

    @staticmethod
    def build_cnf(args):
        """Build a Graph ordering principle formula according to the arguments

        Arguments:
        - `args`: command line options
        """
        G = SimpleGraphHelper.obtain_graph(args)
        return GraphOrderingPrinciple(G, args.total, args.smart, args.plant, args.knuth)