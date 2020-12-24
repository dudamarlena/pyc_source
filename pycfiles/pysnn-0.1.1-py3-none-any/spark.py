# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_apps/cli/spark.py
# Compiled at: 2017-11-15 13:56:16
__version__ = 'SPARK-0.6.1'
import re, sys

def _namelist(instance):
    namelist, namedict, classlist = [], {}, [instance.__class__]
    for c in classlist:
        for b in c.__bases__:
            classlist.append(b)

        for name in c.__dict__.keys():
            if name not in namedict:
                namelist.append(name)
                namedict[name] = 1

    return namelist


class GenericScanner:
    __module__ = __name__

    def __init__(self):
        pattern = self.reflect()
        self.re = re.compile(pattern, re.VERBOSE)
        self.index2func = {}
        for (name, number) in self.re.groupindex.items():
            self.index2func[number - 1] = getattr(self, 't_' + name)

    def makeRE(self, name):
        doc = getattr(self, name).__doc__
        rv = '(?P<%s>%s)' % (name[2:], doc)
        return rv

    def reflect(self):
        rv = []
        for name in _namelist(self):
            if name[:2] == 't_' and name != 't_default':
                rv.append(self.makeRE(name))

        rv.append(self.makeRE('t_default'))
        return ('|').join(rv)

    def error(self, s, pos):
        sys.stderr.write('Lexical error at position %s' % pos)
        raise SystemExit

    def tokenize(self, s):
        pos = 0
        n = len(s)
        while pos < n:
            m = self.re.match(s, pos)
            if m is None:
                self.error(s, pos)
            groups = m.groups()
            for i in range(len(groups)):
                if groups[i] and i in self.index2func:
                    self.index2func[i](groups[i])

            pos = m.end()

        return

    def t_default(self, s):
        r"""( . | \n )+"""
        pass


class GenericParser:
    __module__ = __name__

    def __init__(self, start):
        self.rules = {}
        self.rule2func = {}
        self.rule2name = {}
        self.collectRules()
        self.startRule = self.augment(start)
        self.ruleschanged = 1

    _START = 'START'
    _EOF = 'EOF'

    def preprocess(self, rule, func):
        return (
         rule, func)

    def addRule(self, doc, func):
        rules = doc.split()
        index = []
        for i in range(len(rules)):
            if rules[i] == '::=':
                index.append(i - 1)

        index.append(len(rules))
        for i in range(len(index) - 1):
            lhs = rules[index[i]]
            rhs = rules[index[i] + 2:index[(i + 1)]]
            rule = (lhs, tuple(rhs))
            (rule, fn) = self.preprocess(rule, func)
            if lhs in self.rules:
                self.rules[lhs].append(rule)
            else:
                self.rules[lhs] = [
                 rule]
            self.rule2func[rule] = fn
            self.rule2name[rule] = func.__name__[2:]

        self.ruleschanged = 1

    def collectRules(self):
        for name in _namelist(self):
            if name[:2] == 'p_':
                func = getattr(self, name)
                doc = func.__doc__
                self.addRule(doc, func)

    def augment(self, start):
        startRule = (
         self._START, (start, self._EOF))
        self.rule2func[startRule] = lambda args: args[0]
        self.rules[self._START] = [startRule]
        self.rule2name[startRule] = ''
        return startRule

    def makeFIRST(self):
        union = {}
        self.first = {}
        for rulelist in self.rules.values():
            for (lhs, rhs) in rulelist:
                if lhs not in self.first:
                    self.first[lhs] = {}
                if len(rhs) == 0:
                    self.first[lhs][None] = 1
                    continue
                sym = rhs[0]
                if sym not in self.rules:
                    self.first[lhs][sym] = 1
                else:
                    union[(sym, lhs)] = 1

        changes = 1
        while changes:
            changes = 0
            for (src, dest) in union.keys():
                destlen = len(self.first[dest])
                self.first[dest].update(self.first[src])
                if len(self.first[dest]) != destlen:
                    changes = 1

        return

    def typestring(self, token):
        return

    def error(self, token):
        sys.stderr.write("Syntax error at or near `%s' token" % token)
        raise SystemExit

    def parse(self, tokens):
        tree = {}
        tokens.append(self._EOF)
        states = {0: [(self.startRule, 0, 0)]}
        if self.ruleschanged:
            self.makeFIRST()
        for i in range(len(tokens)):
            states[i + 1] = []
            if states[i] == []:
                break
            self.buildState(tokens[i], states, i, tree)

        if i < len(tokens) - 1 or states[(i + 1)] != [(self.startRule, 2, 0)]:
            self.error(tokens[(i - 1)])
        rv = self.buildTree(tokens, tree, ((self.startRule, 2, 0), i + 1))
        del tokens[-1]
        return rv

    def buildState(self, token, states, i, tree):
        needsCompletion = {}
        state = states[i]
        predicted = {}
        for item in state:
            (rule, pos, parent) = item
            (lhs, rhs) = rule
            if pos == len(rhs):
                if len(rhs) == 0:
                    needsCompletion[lhs] = (
                     item, i)
                for pitem in states[parent]:
                    if pitem is item:
                        break
                    (prule, ppos, pparent) = pitem
                    (plhs, prhs) = prule
                    if prhs[ppos:ppos + 1] == (lhs,):
                        new = (
                         prule, ppos + 1, pparent)
                        if new not in state:
                            state.append(new)
                            tree[(new, i)] = [(item, i)]
                        else:
                            tree[(new, i)].append((item, i))

                continue
            nextSym = rhs[pos]
            if nextSym in self.rules:
                if nextSym in needsCompletion:
                    new = (
                     rule, pos + 1, parent)
                    olditem_i = needsCompletion[nextSym]
                    if new not in state:
                        state.append(new)
                        tree[(new, i)] = [olditem_i]
                    else:
                        tree[(new, i)].append(olditem_i)
                if nextSym in predicted:
                    continue
                predicted[nextSym] = 1
                ttype = token is not self._EOF and self.typestring(token) or None
                if ttype is not None:
                    for prule in self.rules[nextSym]:
                        new = (
                         prule, 0, i)
                        prhs = prule[1]
                        if len(prhs) == 0:
                            state.append(new)
                            continue
                        prhs0 = prhs[0]
                        if prhs0 not in self.rules:
                            if prhs0 != ttype:
                                continue
                            else:
                                state.append(new)
                                continue
                        first = self.first[prhs0]
                        if None not in first and ttype not in first:
                            continue
                        state.append(new)

                    continue
                for prule in self.rules[nextSym]:
                    prhs = prule[1]
                    if len(prhs) > 0 and prhs[0] not in self.rules and token != prhs[0]:
                        continue
                    state.append((prule, 0, i))

            elif token == nextSym:
                states[(i + 1)].append((rule, pos + 1, parent))

        return

    def buildTree(self, tokens, tree, root):
        stack = []
        self.buildTree_r(stack, tokens, -1, tree, root)
        return stack[0]

    def buildTree_r(self, stack, tokens, tokpos, tree, root):
        ((rule, pos, parent), state) = root
        while pos > 0:
            want = ((rule, pos, parent), state)
            if want not in tree:
                pos = pos - 1
                state = state - 1
                stack.insert(0, tokens[tokpos])
                tokpos = tokpos - 1
            else:
                children = tree[want]
                if len(children) > 1:
                    child = self.ambiguity(children)
                else:
                    child = children[0]
                tokpos = self.buildTree_r(stack, tokens, tokpos, tree, child)
                pos = pos - 1
                ((crule, cpos, cparent), cstate) = child
                state = cparent

        (lhs, rhs) = rule
        result = self.rule2func[rule](stack[:len(rhs)])
        stack[:(len(rhs))] = [result]
        return tokpos

    def ambiguity(self, children):
        sortlist = []
        name2index = {}
        for i in range(len(children)):
            ((rule, pos, parent), index) = children[i]
            (lhs, rhs) = rule
            name = self.rule2name[rule]
            sortlist.append((len(rhs), name))
            name2index[name] = i

        sortlist.sort()
        l = [ x[1] for x in sortlist ]
        return children[name2index[self.resolve(l)]]

    def resolve(self, list):
        return list[0]


class GenericASTBuilder(GenericParser):
    __module__ = __name__

    def __init__(self, AST, start):
        GenericParser.__init__(self, start)
        self.AST = AST

    def preprocess(self, rule, func):
        rebind = lambda lhs, self=self: lambda args, lhs=lhs, self=self: self.buildASTNode(args, lhs)
        (lhs, rhs) = rule
        return (
         rule, rebind(lhs))

    def buildASTNode(self, args, lhs):
        children = []
        for arg in args:
            if isinstance(arg, self.AST):
                children.append(arg)
            else:
                children.append(self.terminal(arg))

        return self.nonterminal(lhs, children)

    def terminal(self, token):
        return token

    def nonterminal(self, type, args):
        rv = self.AST(type)
        rv[:(len(args))] = args
        return rv


class GenericASTTraversalPruningException(Exception):
    __module__ = __name__


class GenericASTTraversal:
    __module__ = __name__

    def __init__(self, ast):
        self.ast = ast

    def typestring(self, node):
        return node.type

    def prune(self):
        raise GenericASTTraversalPruningException

    def preorder(self, node=None):
        if node is None:
            node = self.ast
        try:
            name = 'n_' + self.typestring(node)
            if hasattr(self, name):
                func = getattr(self, name)
                func(node)
            else:
                self.default(node)
        except GenericASTTraversalPruningException:
            return

        for kid in node:
            self.preorder(kid)

        name = name + '_exit'
        if hasattr(self, name):
            func = getattr(self, name)
            func(node)
        return

    def postorder(self, node=None):
        if node is None:
            node = self.ast
        for kid in node:
            self.postorder(kid)

        name = 'n_' + self.typestring(node)
        if hasattr(self, name):
            func = getattr(self, name)
            func(node)
        else:
            self.default(node)
        return

    def default(self, node):
        pass


class GenericASTMatcher(GenericParser):
    __module__ = __name__

    def __init__(self, start, ast):
        GenericParser.__init__(self, start)
        self.ast = ast

    def preprocess(self, rule, func):
        rebind = lambda func, self=self: lambda args, func=func, self=self: self.foundMatch(args, func)
        (lhs, rhs) = rule
        rhslist = list(rhs)
        rhslist.reverse()
        return (
         (
          lhs, tuple(rhslist)), rebind(func))

    def foundMatch(self, args, func):
        func(args[(-1)])
        return args[(-1)]

    def match_r(self, node):
        self.input.insert(0, node)
        children = 0
        for child in node:
            if children == 0:
                self.input.insert(0, '(')
            children = children + 1
            self.match_r(child)

        if children > 0:
            self.input.insert(0, ')')

    def match(self, ast=None):
        if ast is None:
            ast = self.ast
        self.input = []
        self.match_r(ast)
        self.parse(self.input)
        return

    def resolve(self, list):
        return list[(-1)]


def _dump(tokens, states):
    for i in range(len(states)):
        print ('state', i)
        for ((lhs, rhs), pos, parent) in states[i]:
            print (
             '\t', lhs, '::='),
            print (' ').join(rhs[:pos]),
            print '.',
            print (' ').join(rhs[pos:]),
            print (',', parent, '.', pos)

        if i < len(tokens):
            print ''
            print ('token', str(tokens[i]))
            print ''