# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulvicol/Code/Python/equibel_to_update/equibel/formatters/aspformatter.py
# Compiled at: 2016-05-29 19:10:59
"""Formatter to create the Answer Set Programming (ASP) representation
of an arbitrary EquibelGraph instance. The ASP format is used when 
giving a graph to the ``gringo``/``clingo`` ASP tools.
"""
from sympy.logic.boolalg import *
__all__ = [
 'to_asp', 'convert_formula_to_asp']
NODE_TEMPLATE = 'node({0}).\n'
RANGE_TEMPLATE = 'node({0}..{1}).\n'
EDGE_TEMPLATE = 'edge({0},{1}).\n'
WEIGHT_TEMPLATE = 'weight({0},{1},{2}).\n'
FORMULA_TEMPLATE = 'formula({0},{1}).\n'
ATOM_TEMPLATE = 'atom({0}).\n'
IMPLIES_TEMPLATE = 'implies({0},{1})'
IFF_TEMPLATE = 'iff({0},{1})'
AND_TEMPLATE = 'and({0},{1})'
OR_TEMPLATE = 'or({0},{1})'
NEG_TEMPLATE = 'neg({0})'

def to_asp(G, atoms=None):
    asp_str = ''
    for node_id in G.nodes():
        asp_str += NODE_TEMPLATE.format(node_id)

    for from_node_id, to_node_id in G.edges():
        asp_str += EDGE_TEMPLATE.format(from_node_id, to_node_id)
        if not G.is_directed():
            asp_str += EDGE_TEMPLATE.format(to_node_id, from_node_id)

    for node_id in G.nodes():
        formulas = G.formulas(node_id)
        for formula in formulas:
            if formula != True:
                formatted_formula = convert_formula_to_asp(formula)
                asp_str += FORMULA_TEMPLATE.format(node_id, formatted_formula)

    if not atoms:
        atoms = G.atoms()
    for atom in atoms:
        asp_str += ATOM_TEMPLATE.format(atom)

    return asp_str


def convert_formula_to_asp(formula):
    """Creates a string representing a Sympy formula object, formatted as 
    """
    if formula.is_Atom:
        return formula
    func, args = formula.func, formula.args
    if func == Not:
        formatted_term = convert_formula_to_asp(args[0])
        return NEG_TEMPLATE.format(formatted_term)
    if len(args) == 2:
        first_operand = convert_formula_to_asp(args[0])
        second_operand = convert_formula_to_asp(args[1])
    else:
        first_operand = convert_formula_to_asp(args[0])
        rest_of_formula = func(*args[1:])
        second_operand = convert_formula_to_asp(rest_of_formula)
    if func == And:
        return AND_TEMPLATE.format(first_operand, second_operand)
    if func == Or:
        return OR_TEMPLATE.format(first_operand, second_operand)
    if func == Implies:
        return IMPLIES_TEMPLATE.format(first_operand, second_operand)
    if func == Equivalent:
        return IFF_TEMPLATE.format(first_operand, second_operand)