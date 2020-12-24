# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/families/cliquecoloring.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 4251 bytes
__doc__ = 'Implementation of the clique-coloring formula \n'
from cnfformula.cnf import CNF
import cnfformula.cmdline, cnfformula.families
from itertools import combinations, permutations

@cnfformula.families.register_cnf_generator
def CliqueColoring(n, k, c):
    r"""Clique-coloring CNF formula 

    The formula claims that a graph :math:`G` with :math:`n` vertices
    simultaneously contains a clique of size :math:`k` and a coloring
    of size :math:`c`.

    If :math:`k = c + 1` then the formula is clearly unsatisfiable,
    and it is the only known example of a formula hard for cutting
    planes proof system. [1]_

    Variables :math:`e_{u,v}` to encode the edges of the graph.
    
    Variables :math:`q_{i,v}` encode a function from :math:`[k]` to
    :math:`[n]` that represents a clique.
    
    Variables :math:`r_{v,\ell}` encode a function from :math:`[n]` to
    :math:`[c]` that represents a coloring.
     
    Parameters
    ----------
    n : number of vertices in the graph
    k : size of the clique
    c : size of the coloring

    Returns
    -------
    A CNF object

    References
    ----------
    .. [1] Pavel Pudlak.
           Lower bounds for resolution and cutting plane proofs and
           monotone computations.
           Journal of Symbolic Logic (1997)

    """

    def E(u, v):
        """Name of an edge variable"""
        return 'e_{{{0},{1}}}'.format(min(u, v), max(u, v))

    def Q(i, v):
        """Name of an edge variable"""
        return 'q_{{{0},{1}}}'.format(i, v)

    def R(v, ell):
        """Name of an coloring variable"""
        return 'r_{{{0},{1}}}'.format(v, ell)

    formula = CNF()
    formula.header = 'There is a graph of {0} vertices with a {1}-clique'.format(n, k) + ' and a {0}-coloring\n\n'.format(c) + formula.header
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            formula.add_variable(E(u, v))

    for i in range(1, k + 1):
        for v in range(1, n + 1):
            formula.add_variable(Q(i, v))

    for v in range(1, n + 1):
        for ell in range(1, c + 1):
            formula.add_variable(R(v, ell))

    for k in range(1, k + 1):
        for cl in CNF.equal_to_constraint([Q(k, v) for v in range(1, n + 1)], 1):
            formula.add_clause(cl, strict=True)

    for v in range(1, n + 1):
        for i, j in combinations(range(1, k + 1), 2):
            formula.add_clause([(False, Q(i, v)), (False, Q(j, v))], strict=True)

    for u, v in combinations(range(1, n + 1), 2):
        for i, j in permutations(range(1, k + 1), 2):
            formula.add_clause([(True, E(u, v)), (False, Q(i, u)), (False, Q(j, v))], strict=True)

    for v in range(1, n + 1):
        for cl in CNF.equal_to_constraint([R(v, ell) for ell in range(1, c + 1)], 1):
            formula.add_clause(cl, strict=True)

    for u, v in combinations(range(1, n + 1), 2):
        for ell in range(1, c + 1):
            formula.add_clause([(False, E(u, v)), (False, R(u, ell)), (False, R(v, ell))], strict=True)

    return formula


@cnfformula.cmdline.register_cnfgen_subcommand
class CliqueColoringCmdHelper(object):
    """CliqueColoringCmdHelper"""
    name = 'cliquecoloring'
    description = 'There is a graph G with a k-clique and a c-coloring'

    @staticmethod
    def setup_command_line(parser):
        """Setup the command line options for clique-coloring formula

        Arguments:
        - `parser`: parser to load with options.
        """
        parser.add_argument('n', metavar='<n>', type=int, help='Number of vertices')
        parser.add_argument('k', metavar='<k>', type=int, help='Clique size')
        parser.add_argument('c', metavar='<c>', type=int, help='Coloring size')

    @staticmethod
    def build_cnf(args):
        """Build a Clique-coclique formula according to the arguments

        Arguments:
        - `args`: command line options
        """
        return CliqueColoring(args.n, args.k, args.c)