# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/logic/grammar.py
# Compiled at: 2018-04-24 04:48:32
from pyparsing import *
import re

class TreeBuilder(object):
    """
    The parsing tree.
    """

    def __init__(self, logic):
        self.logic = logic
        self.reset()

    def trigger(self, a, loc, toks, op):
        if op == 'litgroup':
            negated = False
            if toks[0] == '!' or toks[0] == '*':
                if toks[0] == '*':
                    negated = 2
                else:
                    negated = True
                toks = toks[1]
            else:
                toks = toks[0]
            self.stack.append(self.logic.litgroup(negated, toks[:-1], toks[(-1)], self.logic.mln))
        if op == 'lit':
            negated = False
            if toks[0] == '!' or toks[0] == '*':
                if toks[0] == '*':
                    negated = 2
                else:
                    negated = True
                toks = toks[1]
            else:
                toks = toks[0]
            self.stack.append(self.logic.lit(negated, toks[0], toks[1], self.logic.mln))
        elif op == '!':
            if len(toks) == 1:
                formula = self.logic.negation(self.stack[-1:], self.logic.mln)
                self.stack = self.stack[:-1]
                self.stack.append(formula)
        elif op == '=':
            if len(toks) == 2:
                self.stack.append(self.logic.equality(list(toks), False, self.logic.mln))
        elif op == '!=':
            if len(toks) == 2:
                self.stack.append(self.logic.equality(list(toks), True, self.logic.mln))
        elif op == '^':
            if len(toks) > 1:
                formula = self.logic.conjunction(self.stack[-len(toks):], self.logic.mln)
                self.stack = self.stack[:-len(toks)]
                self.stack.append(formula)
        elif op == 'v':
            if len(toks) > 1:
                formula = self.logic.disjunction(self.stack[-len(toks):], self.logic.mln)
                self.stack = self.stack[:-len(toks)]
                self.stack.append(formula)
        elif op == '=>':
            if len(toks) == 2:
                children = self.stack[-2:]
                self.stack = self.stack[:-2]
                self.stack.append(self.logic.implication(children, self.logic.mln))
        elif op == '<=>':
            if len(toks) == 2:
                children = self.stack[-2:]
                self.stack = self.stack[:-2]
                self.stack.append(self.logic.biimplication(children, self.logic.mln))
        elif op == 'ex':
            if len(toks) == 2:
                formula = self.stack.pop()
                variables = map(str, toks[0])
                self.stack.append(self.logic.exist(variables, formula, self.logic.mln))
        elif op == 'count':
            if len(toks) in (3, 4):
                pred, pred_params = toks[0]
                if len(toks) == 3:
                    fixed_params, op, count = [], toks[1], int(toks[2])
                else:
                    fixed_params, op, count = list(toks[1]), toks[2], int(toks[3])
                self.stack.append(self.logic.count_constraint(pred, pred_params, fixed_params, op, count))
        return self.stack[(-1)]

    def reset(self):
        self.stack = []

    def getConstraint(self):
        if len(self.stack) > 1:
            raise Exception('Not a valid formula - reduces to more than one element %s' % str(self.stack))
        if len(self.stack) == 0:
            raise Exception('Constraint could not be parsed')
        return self.stack[0]


class Grammar(object):
    """
    Abstract super class for all logic grammars.
    """

    def __deepcopy__(self, memo):
        return self

    def parse_formula(self, s):
        self.tree.reset()
        self.formula.parseString(s)
        constr = self.tree.getConstraint()
        return constr

    def parse_atom(self, string):
        """
        Parses a predicate such as p(A,B) and returns a tuple where the first item 
        is the predicate name and the second is a list of parameters, e.g. ("p", ["A", "B"])
        """
        m = re.match('(\\w+)\\((.*?)\\)$', string)
        if m is not None:
            return (m.group(1), map(str.strip, m.group(2).split(',')))
        else:
            raise Exception("Could not parse predicate '%s'" % string)
            return

    def parse_predicate(self, s):
        return self.predDecl.parseString(s)[0]

    def isvar(self, identifier):
        raise Exception('%s does not implement isvar().' % str(type(self)))

    def isconstant(self, identifier):
        return not self.isVar(identifier)

    def istemplvar(self, s):
        return s[0] == '+' and self.isvar(s[1:])

    def parse_domain(self, s):
        """
        Parses a domain declaration and returns a tuple (domain name, list of constants)
        Returns None if it cannot be parsed.
        """
        m = re.match('(\\w+)\\s*=\\s*{(.*?)}', s)
        if m == None:
            return
        else:
            return (
             m.group(1), map(str.strip, m.group(2).split(',')))

    def parse_literal(self, s):
        """
        Parses a literal such as !p(A,B) or p(A,B)=False and returns a tuple 
        where the first item is whether the literal is true, the second is the 
        predicate name and the third is a list of parameters, e.g. (False, "p", ["A", "B"])
        """
        self.tree.reset()
        lit = self.literal.parseString(s)
        lit = self.tree.getConstraint()
        return (
         not lit.negated, lit.predname, lit.args)


class StandardGrammar(Grammar):
    """
    The standard MLN logic syntax.
    """

    def __init__(self, logic):
        identifierCharacter = alphanums + '_' + '-' + "'"
        lcCharacter = alphas.lower()
        ucCharacter = alphas.upper()
        lcName = Word(lcCharacter, alphanums + '_')
        openRB = Literal('(').suppress()
        closeRB = Literal(')').suppress()
        domName = Combine(Optional(Literal(':')) + lcName + Optional(Literal('!') | Literal('?')))
        constant = Word(identifierCharacter) | Word(nums) | Combine(Literal('"') + Word(printables.replace('"', '')) + Literal('"'))
        variable = Word(lcCharacter, identifierCharacter)
        atomArgs = Group(delimitedList(constant | Combine(Optional('+') + variable)))
        predDeclArgs = Group(delimitedList(domName))
        predName = Word(identifierCharacter)
        atom = Group(predName + openRB + atomArgs + closeRB)
        literal = Optional(Literal('!') | Literal('*')) + atom
        gndAtomArgs = Group(delimitedList(constant))
        gndLiteral = Optional(Literal('!')) + Group(predName + openRB + gndAtomArgs + closeRB)
        predDecl = Group(predName + openRB + predDeclArgs + closeRB) + StringEnd()
        varList = Group(delimitedList(variable))
        count_constraint = Literal('count(').suppress() + atom + Optional(Literal('|').suppress() + varList) + Literal(')').suppress() + (Literal('=') | Literal('>=') | Literal('<=')) + Word(nums)
        formula = Forward()
        exist = Literal('EXIST ').suppress() + Group(delimitedList(variable)) + openRB + Group(formula) + closeRB
        equality = (constant | variable) + Literal('=').suppress() + (constant | variable)
        inequality = (constant | variable) + Literal('=/=').suppress() + (constant | variable)
        negation = Literal('!').suppress() + openRB + Group(formula) + closeRB
        item = literal | exist | equality | openRB + formula + closeRB | negation
        disjunction = Group(item) + ZeroOrMore(Literal('v').suppress() + Group(item))
        conjunction = Group(disjunction) + ZeroOrMore(Literal('^').suppress() + Group(disjunction))
        implication = Group(conjunction) + Optional(Literal('=>').suppress() + Group(conjunction))
        biimplication = Group(implication) + Optional(Literal('<=>').suppress() + Group(implication))
        constraint = biimplication | count_constraint
        formula << constraint

        def lit_parse_action(a, b, c):
            tree.trigger(a, b, c, 'lit')

        def gndlit_parse_action(a, b, c):
            tree.trigger(a, b, c, 'gndlit')

        def neg_parse_action(a, b, c):
            tree.trigger(a, b, c, '!')

        def disjunction_parse_action(a, b, c):
            tree.trigger(a, b, c, 'v')

        def conjunction_parse_action(a, b, c):
            tree.trigger(a, b, c, '^')

        def exist_parse_action(a, b, c):
            tree.trigger(a, b, c, 'ex')

        def implication_parse_action(a, b, c):
            tree.trigger(a, b, c, '=>')

        def biimplication_parse_action(a, b, c):
            tree.trigger(a, b, c, '<=>')

        def equality_parse_action(a, b, c):
            tree.trigger(a, b, c, '=')

        def inequality_parse_action(a, b, c):
            tree.trigger(a, b, c, '!=')

        def count_constraint_parse_action(a, b, c):
            tree.trigger(a, b, c, 'count')

        tree = TreeBuilder(logic)
        literal.setParseAction(lit_parse_action)
        gndLiteral.setParseAction(gndlit_parse_action)
        negation.setParseAction(neg_parse_action)
        disjunction.setParseAction(disjunction_parse_action)
        conjunction.setParseAction(conjunction_parse_action)
        exist.setParseAction(exist_parse_action)
        implication.setParseAction(implication_parse_action)
        biimplication.setParseAction(biimplication_parse_action)
        equality.setParseAction(equality_parse_action)
        inequality.setParseAction(inequality_parse_action)
        count_constraint.setParseAction(count_constraint_parse_action)
        self.tree = tree
        self.formula = formula + StringEnd()
        self.predDecl = predDecl
        self.literal = literal

    def isvar(self, identifier):
        return identifier[0].islower() or identifier[0] == '+'


class PRACGrammar(Grammar):
    """
    The specialized PRAC MLN grammar supporting infix not-equals and
    arbitrary constants. Variables need to start with '?'
    """

    def __init__(self, logic):
        identifierCharacter = alphanums + 'ÄÖÜäöü' + '_' + '-' + "'" + '.' + ':' + ';' + '$' + '~' + '\\' + '!'
        lcCharacter = alphas.lower()
        ucCharacter = alphas.upper()
        lcName = Word(lcCharacter, alphanums + '_')
        qMark = '?'
        openRB = Literal('(').suppress()
        closeRB = Literal(')').suppress()
        openSB = Literal('[').suppress()
        closeSB = Literal(']').suppress()
        domName = Combine(Optional(Literal(':')) + lcName + Optional(Literal('!') | Literal('?')))
        constant = Word(identifierCharacter) | Word(nums) | Combine(Literal('"') + Word(printables.replace('"', '')) + Literal('"'))
        variable = Word(qMark, identifierCharacter)
        atomArgs = Group(delimitedList(constant | Combine(Optional('+') + variable)))
        predDeclArgs = Group(delimitedList(domName))
        predName = Word(identifierCharacter)
        predGroup = predName + OneOrMore(Literal('|').suppress() + predName)
        atom = Group(predName + openRB + atomArgs + closeRB)
        groupatom = Group(predGroup + openRB + atomArgs + closeRB)
        literal = Optional(Literal('!') | Literal('*')) + atom
        litgroup = Optional(Literal('!') | Literal('*')) + groupatom
        predDecl = Group(predName + openRB + predDeclArgs + closeRB + StringEnd())
        formula = Forward()
        exist = Literal('EXIST ').suppress() + Group(delimitedList(variable)) + openRB + Group(formula) + closeRB
        equality = (constant | variable) + Literal('=').suppress() + (constant | variable)
        inequality = (constant | variable) + Literal('=/=').suppress() + (constant | variable)
        negation = Literal('!').suppress() + openRB + Group(formula) + closeRB
        item = litgroup | literal | exist | inequality | equality | openRB + formula + closeRB | negation
        conjunction = Group(item) + ZeroOrMore(Literal('^').suppress() + Group(item))
        disjunction = Group(conjunction) + ZeroOrMore(Literal('v').suppress() + Group(conjunction))
        implication = Group(disjunction) + Optional(Literal('=>').suppress() + Group(disjunction))
        biimplication = Group(implication) + Optional(Literal('<=>').suppress() + Group(implication))
        formula << biimplication

        def lit_group_parse_action(a, b, c):
            try:
                return tree.trigger(a, b, c, 'litgroup')
            except Exception as e:
                print e

        def lit_parse_action(a, b, c):
            return tree.trigger(a, b, c, 'lit')

        def neg_parse_action(a, b, c):
            return tree.trigger(a, b, c, '!')

        def disjunction_parse_action(a, b, c):
            tree.trigger(a, b, c, 'v')

        def conjunction_parse_action(a, b, c):
            tree.trigger(a, b, c, '^')

        def exist_parse_action(a, b, c):
            return tree.trigger(a, b, c, 'ex')

        def implication_parse_action(a, b, c):
            tree.trigger(a, b, c, '=>')

        def biimplication_parse_action(a, b, c):
            tree.trigger(a, b, c, '<=>')

        def equality_parse_action(a, b, c):
            return tree.trigger(a, b, c, '=')

        def inequality_parse_action(a, b, c):
            return tree.trigger(a, b, c, '!=')

        def count_constraint_parse_action(a, b, c):
            tree.trigger(a, b, c, 'count')

        tree = TreeBuilder(logic)
        litgroup.setParseAction(lit_group_parse_action)
        literal.setParseAction(lit_parse_action)
        negation.setParseAction(neg_parse_action)
        disjunction.setParseAction(disjunction_parse_action)
        conjunction.setParseAction(conjunction_parse_action)
        exist.setParseAction(exist_parse_action)
        implication.setParseAction(implication_parse_action)
        biimplication.setParseAction(biimplication_parse_action)
        equality.setParseAction(equality_parse_action)
        inequality.setParseAction(inequality_parse_action)
        self.equality = equality
        self.tree = tree
        self.formula = formula + StringEnd()
        self.predDecl = predDecl
        self.literal = literal

    def isvar(self, identifier):
        """
        Variables must start with a question mark (or the + operator, 
        anything else is considered a constant.
        """
        return identifier[0] == '?' or identifier[0] == '+'


if __name__ == '__main__':
    from pracmln.mln.base import MLN
    from pracmln.mln.database import Database
    mln = MLN(grammar='PRACGrammar')
    mln << 'bar(x)'
    mln << 'a(s)'
    mln << 'b(s)'
    mln << 'c(s)'
    f = 'a|b|c(s) => (bar(y) <=> bar(x))'
    print 'mln:'
    mln.write()
    print '---------------------------------------------------'
    f = mln.logic.grammar.parse_formula(f)
    print f, '==================================================================================='
    f.print_structure()
    print list(f.literals())
    print 'f:', f
    mln << 'coreference(a,b)'
    mln << 'distance(d,e,f)'
    mln.formula(f)
    f = 'a|b|c(s) ^ bar(y) ^ bar(x)'
    f = mln.logic.grammar.parse_formula(f)
    mln.write()
    cnf = f.cnf()
    cnf.print_structure()
    mln.formula(cnf)
    db = Database(mln)
    matmln = mln.materialize(db)
    matmln.write()