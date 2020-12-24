# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/ptolemy/numericalSolutionsToGroebnerBasis.py
# Compiled at: 2017-05-26 08:27:22
from __future__ import print_function
from .polynomial import Polynomial
from .component import NonZeroDimensionalComponent
from ..pari import pari

def numerical_solutions_with_one(polys):
    solutions = numerical_solutions(polys)
    for solution in solutions:
        if not isinstance(solution, NonZeroDimensionalComponent):
            solution['1'] = pari(1)

    return solutions


class PariPolynomialAndVariables:

    def __init__(self, polynomial, variables=None):
        if isinstance(polynomial, Polynomial):
            self.pari_polynomial = pari(polynomial.to_string(lambda x: ('+', '(%s)' % x)))
            self.variables = polynomial.variables()
        else:
            self.pari_polynomial = polynomial
            self.variables = variables

    def get_variable_if_univariate(self):
        if len(self.variables) == 1:
            return self.variables[0]

    def substitute(self, var, value):
        return PariPolynomialAndVariables(polynomial=self.pari_polynomial.substpol(var, value), variables=[ v for v in self.variables if not v == var ])

    def get_roots(self):
        return self.pari_polynomial.polroots(precision=3.4 * pari.get_real_precision())


def numerical_solutions(polys):
    polysReduced = [ poly.factor_out_variables() for poly in polys ]
    polysFiltered = [ poly for poly in polysReduced if not poly.is_constant() or poly.get_constant() == 0
                    ]
    for poly in polysFiltered:
        if poly.is_constant():
            return NonZeroDimensionalComponent()

    polysAndVars = [ PariPolynomialAndVariables(poly) for poly in polysFiltered ]
    solutions = _numerical_solutions_recursion(polysAndVars, {})
    number_variables = len(set(sum([ poly.variables() for poly in polys ], [])))
    return [ solution if len(solution) == number_variables else NonZeroDimensionalComponent() for solution in solutions
           ]


def _get_first(l):
    if l:
        return l[0]
    else:
        return


def _remove(l, element):
    return [ x for x in l if x is not element ]


def _numerical_solutions_recursion(polysAndVars, solutionDict):
    if polysAndVars == []:
        return [solutionDict]
    else:
        univariatePoly = _get_first([ poly for poly in polysAndVars if poly.get_variable_if_univariate()
                                    ])
        if univariatePoly is not None:
            variable = univariatePoly.get_variable_if_univariate()
            variableDicts = []
            for solution in univariatePoly.get_roots():
                newSolutionDict = solutionDict.copy()
                newSolutionDict[variable] = solution
                new_polys = [ poly.substitute(variable, solution) for poly in _remove(polysAndVars, univariatePoly)
                            ]
                variableDicts += _numerical_solutions_recursion(new_polys, newSolutionDict)

            return variableDicts
        return [
         solutionDict]