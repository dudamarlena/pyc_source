# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/families/tseitin.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 3425 bytes
"""Implementation of Tseitin formulas
"""
from cnfformula.cnf import CNF
from cnfformula.cmdline import SimpleGraphHelper
from cnfformula.graphs import enumerate_vertices, neighbors
import random, cnfformula.cmdline, cnfformula.families

@cnfformula.families.register_cnf_generator
def TseitinFormula(graph, charges=None):
    """Build a Tseitin formula based on the input graph.

    Odd charge is put on the first vertex by default, unless other
    vertices are is specified in input.

    Arguments:
    - `graph`: input graph
    - `charges': odd or even charge for each vertex
    """
    V = enumerate_vertices(graph)
    if charges == None:
        charges = [
         1] + [0] * (len(V) - 1)
    else:
        charges = [bool(c) for c in charges]
    if len(charges) < len(V):
        charges = charges + [0] * (len(V) - len(charges))
    tse = CNF()
    edgename = {}
    for u, v in sorted((graph.edges()), key=sorted):
        edgename[(u, v)] = 'E_{{{0},{1}}}'.format(u, v)
        edgename[(v, u)] = 'E_{{{0},{1}}}'.format(u, v)
        tse.add_variable(edgename[(u, v)])

    for v, c in zip(V, charges):
        names = [edgename[(u, v)] for u in neighbors(graph, v)]
        for cls in CNF.parity_constraint(names, c):
            tse.add_clause((list(cls)), strict=True)

    return tse


@cnfformula.cmdline.register_cnfgen_subcommand
class TseitinCmdHelper(object):
    __doc__ = 'Command line helper for Tseitin  formulas\n    '
    name = 'tseitin'
    description = 'tseitin formula'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for Tseitin formula

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('--charge', metavar='<charge>', default='first', choices=[
         'first', 'random', 'randomodd', 'randomeven'],
          help="charge on the vertices.\n                                    `first'  puts odd charge on first vertex;\n                                    `random' puts a random charge on vertices;\n                                    `randomodd' puts random odd  charge on vertices;\n                                    `randomeven' puts random even charge on vertices.\n                                     ")
        SimpleGraphHelper.setup_command_line(parser)

    @staticmethod
    def build_cnf(args):
        """Build Tseitin formula according to the arguments

        Arguments:
        - `args`: command line options
        """
        G = SimpleGraphHelper.obtain_graph(args)
        if G.order() < 1:
            charge = None
        else:
            if args.charge == 'first':
                charge = [1] + [0] * (G.order() - 1)
            else:
                charge = [random.randint(0, 1) for _ in range(G.order() - 1)]
                parity = sum(charge) % 2
                if args.charge == 'random':
                    charge.append(random.randint(0, 1))
                else:
                    if args.charge == 'randomodd':
                        charge.append(1 - parity)
                    else:
                        if args.charge == 'randomeven':
                            charge.append(parity)
                        else:
                            raise ValueError('Illegal charge specification on command line')
        return TseitinFormula(G, charge)