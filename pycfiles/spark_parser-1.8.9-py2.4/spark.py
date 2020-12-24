# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spark_parser/spark.py
# Compiled at: 2019-11-16 21:02:41
"""
Copyright (c) 2015-2017 Rocky Bernstein
Copyright (c) 1998-2002 John Aycock

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os, pickle, re, sys
if sys.version[0:3] <= '2.3':
    from sets import Set as set

    def sorted(iterable):
        temp = [ x for x in iterable ]
        temp.sort()
        return temp


def _namelist(instance):
    namelist, namedict, classlist = [], {}, [instance.__class__]
    for c in classlist:
        for b in c.__bases__:
            classlist.append(b)

        for name in list(c.__dict__.keys()):
            if name not in namedict:
                namelist.append(name)
                namedict[name] = 1

    return namelist


def rule2str(rule):
    return ('%s ::= %s' % (rule[0], (' ').join(rule[1]))).rstrip()


class _State:
    """
    Extracted from GenericParser and made global so that [un]picking works.
    """
    __module__ = __name__

    def __init__(self, stateno, items):
        self.T, self.complete, self.items = [], [], items
        self.stateno = stateno


DEFAULT_DEBUG = {'rules': False, 'transition': False, 'reduce': False, 'errorstack': None, 'context': True, 'dups': False}

class GenericParser(object):
    """
    An Earley parser, as per J. Earley, "An Efficient Context-Free
    Parsing Algorithm", CACM 13(2), pp. 94-102.  Also J. C. Earley,
    "An Efficient Context-Free Parsing Algorithm", Ph.D. thesis,
    Carnegie-Mellon University, August 1968.  New formulation of
    the parser according to J. Aycock, "Practical Earley Parsing
    and the SPARK Toolkit", Ph.D. thesis, University of Victoria,
    2001, and J. Aycock and R. N. Horspool, "Practical Earley
    Parsing", unpublished paper, 2001.
    """
    __module__ = __name__

    def __init__(self, start, debug=DEFAULT_DEBUG, coverage_path=None):
        """_start_ : grammar start symbol;
           _debug_ : produce optional parsing debug information
           _profile_ : if not None should be a file path to open
           with where to store profile is stored
        """
        self.rules = {}
        self.rule2func = {}
        self.rule2name = {}
        self.coverage_path = coverage_path
        if coverage_path:
            self.profile_info = {}
            if isinstance(coverage_path, str):
                if os.path.exists(coverage_path):
                    self.profile_info = pickle.load(open(coverage_path, 'rb'))
        else:
            self.profile_info = None
        self.debug = debug
        self.list_like_nt = set()
        self.optional_nt = set()
        self.collectRules()
        if start not in self.rules:
            raise TypeError('Start symbol "%s" is not in LHS of any rule' % start)
        self.augment(start)
        self.ruleschanged = True
        self.check_reduce = {}
        return

    _NULLABLE = '\\e_'
    _START = 'START'
    _BOF = '|-'

    def __getstate__(self):
        if self.ruleschanged:
            self.computeNull()
            self.newrules = {}
            self.new2old = {}
            self.makeNewRules()
            self.ruleschanged = False
            self.edges, self.cores = {}, {}
            self.states = {0: self.makeState0()}
            self.makeState(0, self._BOF)
        changes = True
        while changes:
            changes = False
            for (k, v) in list(self.edges.items()):
                if v is None:
                    (state, sym) = k
                    if state in self.states:
                        self.goto(state, sym)
                        changes = True

        rv = self.__dict__.copy()
        for s in list(self.states.values()):
            del s.items

        del rv['rule2func']
        del rv['nullable']
        del rv['cores']
        return rv

    def __setstate__(self, D):
        self.rules = {}
        self.rule2func = {}
        self.rule2name = {}
        self.collectRules()
        start = D['rules'][self._START][0][1][1]
        self.augment(start)
        D['rule2func'] = self.rule2func
        D['makeSet'] = self.makeSet_fast
        self.__dict__ = D

    def preprocess(self, rule, func):
        return (
         rule, func)

    def addRule(self, doc, func, _preprocess=True):
        """Add a grammar rules to _self.rules_, _self.rule2func_,
            and _self.rule2name_

        Comments, lines starting with # and blank lines are stripped from
        doc. We also allow limited form of * and + when there it is of
        the RHS has a single item, e.g.
               stmts ::= stmt+
        """
        fn = func
        doc = os.linesep.join([ s for s in doc.splitlines() if s if not re.match('^\\s*#', s) ])
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
            if _preprocess:
                (rule, fn) = self.preprocess(rule, func)
            if len(rule[1]) == 1:
                if rule[1][0] == rule[0]:
                    raise TypeError('Complete recursive rule %s' % rule2str(rule))
                repeat = rule[1][(-1)][(-1)]
                if repeat in ('*', '+', '?'):
                    nt = rule[1][(-1)][:-1]
                    if repeat == '?':
                        new_rule_pair = [
                         rule[0], list((nt,))]
                        self.optional_nt.add(rule[0])
                    else:
                        self.list_like_nt.add(rule[0])
                        new_rule_pair = [rule[0], [rule[0]] + list((nt,))]
                    new_rule = rule2str(new_rule_pair)
                    self.addRule(new_rule, func, _preprocess)
                    if repeat == '+':
                        second_rule_pair = (
                         lhs, (nt,))
                    else:
                        second_rule_pair = (
                         lhs, tuple())
                    new_rule = rule2str(second_rule_pair)
                    self.addRule(new_rule, func, _preprocess)
                    continue
            if lhs in self.rules:
                if rule in self.rules[lhs]:
                    if 'dups' in self.debug and self.debug['dups']:
                        self.duplicate_rule(rule)
                    continue
                self.rules[lhs].append(rule)
            else:
                self.rules[lhs] = [
                 rule]
            self.rule2func[rule] = fn
            self.rule2name[rule] = func.__name__[2:]
            self.ruleschanged = True
            if self.profile_info is not None and len(rule[1]) > 0:
                rule_str = self.reduce_string(rule)
                if rule_str not in self.profile_info:
                    self.profile_info[rule_str] = 0

        return

    def remove_rules(self, doc):
        """Remove a grammar rules from  _self.rules_, _self.rule2func_,
            and _self.rule2name_
        """
        doc = os.linesep.join([ s for s in doc.splitlines() if s if not re.match('^\\s*#', s) ])
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
            if lhs not in self.rules:
                return
            if rule in self.rules[lhs]:
                self.rules[lhs].remove(rule)
                del self.rule2func[rule]
                del self.rule2name[rule]
                self.ruleschanged = True
                if self.profile_info is not None and len(rule[1]) > 0:
                    rule_str = self.reduce_string(rule)
                    if rule_str and rule_str in self.profile_info:
                        del self.profile_info[rule_str]

        return

    remove_rule = remove_rules

    def collectRules(self):
        for name in _namelist(self):
            if name[:2] == 'p_':
                func = getattr(self, name)
                doc = func.__doc__
                self.addRule(doc, func)

    def augment(self, start):
        rule = '%s ::= %s %s' % (self._START, self._BOF, start)
        self.addRule(rule, lambda args: args[1], False)

    def computeNull(self):
        self.nullable = {}
        tbd = []
        for rulelist in list(self.rules.values()):
            if not rulelist:
                continue
            lhs = rulelist[0][0]
            self.nullable[lhs] = 0
            for rule in rulelist:
                rhs = rule[1]
                if len(rhs) == 0:
                    self.nullable[lhs] = 1
                    continue
                for sym in rhs:
                    if sym not in self.rules:
                        break
                else:
                    tbd.append(rule)

        changes = 1
        while changes:
            changes = 0
            for (lhs, rhs) in tbd:
                if self.nullable[lhs]:
                    continue
                for sym in rhs:
                    if not self.nullable[sym]:
                        break
                else:
                    self.nullable[lhs] = 1
                    changes = 1

    def makeState0(self):
        s0 = _State(0, [])
        for rule in self.newrules[self._START]:
            s0.items.append((rule, 0))

        return s0

    def finalState(self, tokens):
        if len(self.newrules[self._START]) == 2 and len(tokens) == 0:
            return 1
        start = self.rules[self._START][0][1][1]
        return self.goto(1, start)

    def makeNewRules(self):
        worklist = []
        for rulelist in list(self.rules.values()):
            for rule in rulelist:
                worklist.append((rule, 0, 1, rule))

        for (rule, i, candidate, oldrule) in worklist:
            (lhs, rhs) = rule
            n = len(rhs)
            while i < n:
                sym = rhs[i]
                if sym not in self.rules or not (sym in self.nullable and self.nullable[sym]):
                    candidate = 0
                    i += 1
                    continue
                newrhs = list(rhs)
                newrhs[i] = self._NULLABLE + sym
                newrule = (lhs, tuple(newrhs))
                worklist.append((newrule, i + 1, candidate, oldrule))
                candidate = 0
                i = i + 1
            else:
                if candidate:
                    lhs = self._NULLABLE + lhs
                    rule = (lhs, rhs)
                if lhs in self.newrules:
                    self.newrules[lhs].append(rule)
                else:
                    self.newrules[lhs] = [
                     rule]
                self.new2old[rule] = oldrule

    def typestring(self, token):
        return

    def duplicate_rule(self, rule):
        print 'Duplicate rule:\n\t%s' % rule2str(rule)

    def error(self, tokens, index):
        print "Syntax error at or near token %d: `%s'" % (index, tokens[index])
        if 'context' in self.debug and self.debug['context']:
            if index - 2 >= 0:
                start = index - 2
            else:
                start = 0
            tokens = [ str(tokens[i]) for i in range(start, index + 1) ]
            print 'Token context:\n\t%s' % ('\n\t').join(tokens)
        raise SystemExit

    def errorstack(self, tokens, i, full=False):
        """Show the stacks of completed symbols.
        We get this by inspecting the current transitions
        possible and from that extracting the set of states
        we are in, and from there we look at the set of
        symbols before the "dot". If full is True, we
        show the entire rule with the dot placement.
        Otherwise just the rule up to the dot.
        """
        print '\n-- Stacks of completed symbols:'
        states = [ s for s in self.edges.values() if s ]
        state_stack = set()
        for state in states:
            for (rule, dot) in self.states[state].items:
                (lhs, rhs) = rule
                if dot > 0:
                    if full:
                        state_stack.add('%s ::= %s . %s' % (lhs, (' ').join(rhs[:dot]), (' ').join(rhs[dot:])))
                    else:
                        state_stack.add('%s ::= %s' % (lhs, (' ').join(rhs[:dot])))

        for stack in sorted(state_stack):
            print stack

    def parse(self, tokens, debug=None):
        """This is the main entry point from outside.

        Passing in a debug dictionary changes the default debug
        setting.
        """
        self.tokens = tokens
        if debug:
            self.debug = debug
        sets = [[(1, 0), (2, 0)]]
        self.links = {}
        if self.ruleschanged:
            self.computeNull()
            self.newrules = {}
            self.new2old = {}
            self.makeNewRules()
            self.ruleschanged = False
            self.edges, self.cores = {}, {}
            self.states = {0: self.makeState0()}
            self.makeState(0, self._BOF)
        for i in range(len(tokens)):
            sets.append([])
            if sets[i] == []:
                break
            self.makeSet(tokens, sets, i)
        else:
            sets.append([])
            self.makeSet(None, sets, len(tokens))

        finalitem = (self.finalState(tokens), 0)
        if finalitem not in sets[(-2)]:
            if len(tokens) > 0:
                if self.debug.get('errorstack', False):
                    self.errorstack(tokens, i - 1, str(self.debug['errorstack']) == 'full')
                self.error(tokens, i - 1)
            else:
                self.error(None, None)
        if self.profile_info is not None:
            self.dump_profile_info()
        return self.buildTree(self._START, finalitem, tokens, len(sets) - 2)

    def isnullable(self, sym):
        return sym.startswith(self._NULLABLE)

    def skip(self, xxx_todo_changeme, pos=0):
        (lhs, rhs) = xxx_todo_changeme
        n = len(rhs)
        while pos < n:
            if not self.isnullable(rhs[pos]):
                break
            pos = pos + 1

        return pos

    def makeState(self, state, sym):
        assert sym is not None
        kitems = []
        for (rule, pos) in self.states[state].items:
            (lhs, rhs) = rule
            if rhs[pos:pos + 1] == (sym,):
                kitems.append((rule, self.skip(rule, pos + 1)))

        tcore = tuple(sorted(kitems))
        if tcore in self.cores:
            return self.cores[tcore]
        k = self.cores[tcore] = len(self.states)
        K, NK = _State(k, kitems), _State(k + 1, [])
        self.states[k] = K
        predicted = {}
        edges = self.edges
        rules = self.newrules
        for X in (K, NK):
            worklist = X.items
            for item in worklist:
                (rule, pos) = item
                (lhs, rhs) = rule
                if pos == len(rhs):
                    X.complete.append(rule)
                    continue
                nextSym = rhs[pos]
                key = (X.stateno, nextSym)
                if nextSym not in rules:
                    if key not in edges:
                        edges[key] = None
                        X.T.append(nextSym)
                else:
                    edges[key] = None
                    if nextSym not in predicted:
                        predicted[nextSym] = 1
                        for prule in rules[nextSym]:
                            ppos = self.skip(prule)
                            new = (prule, ppos)
                            NK.items.append(new)

            if X is K:
                edges = {}

        if NK.items == []:
            return k
        tcore = tuple(sorted(predicted.keys()))
        if tcore in self.cores:
            self.edges[(k, None)] = self.cores[tcore]
            return k
        nk = self.cores[tcore] = self.edges[(k, None)] = NK.stateno
        self.edges.update(edges)
        self.states[nk] = NK
        return k

    def goto(self, state, sym):
        key = (
         state, sym)
        if key not in self.edges:
            return
        rv = self.edges[key]
        if rv is None:
            rv = self.makeState(state, sym)
            self.edges[key] = rv
        return rv

    def gotoT(self, state, t):
        if self.debug['rules']:
            print (
             'Terminal', t, state)
        return [
         self.goto(state, t)]

    def gotoST(self, state, st):
        if self.debug['transition']:
            print (
             'GotoST', st, state)
        rv = []
        for t in self.states[state].T:
            if st == t:
                rv.append(self.goto(state, t))

        return rv

    def add(self, set, item, i=None, predecessor=None, causal=None):
        if predecessor is None:
            if item not in set:
                set.append(item)
        else:
            key = (
             item, i)
            if item not in set:
                self.links[key] = []
                set.append(item)
            self.links[key].append((predecessor, causal))
        return

    def makeSet(self, tokens, sets, i):
        cur, next = sets[i], sets[(i + 1)]
        if tokens is not None:
            token = tokens[i]
            ttype = self.typestring(token)
        else:
            ttype = None
            token = None
        if ttype is not None:
            fn, arg = self.gotoT, ttype
        else:
            fn, arg = self.gotoST, token
        for item in cur:
            ptr = (
             item, i)
            (state, parent) = item
            add = fn(state, arg)
            for k in add:
                if k is not None:
                    self.add(next, (k, parent), i + 1, ptr)
                    nk = self.goto(k, None)
                    if nk is not None:
                        self.add(next, (nk, i + 1))

            if parent == i:
                continue
            for rule in self.states[state].complete:
                (lhs, rhs) = rule
                if self.debug['reduce']:
                    self.debug_reduce(rule, tokens, parent, i)
                if self.profile_info is not None:
                    self.profile_rule(rule)
                if lhs in self.check_reduce:
                    if self.check_reduce[lhs] == 'AST':
                        if tokens or hasattr(self, 'tokens'):
                            if hasattr(self, 'tokens'):
                                tokens = self.tokens
                            ast = self.reduce_ast(rule, self.tokens, item, i, sets)
                        else:
                            ast = None
                        invalid = self.reduce_is_invalid(rule, ast, self.tokens, parent, i)
                        if ast:
                            del ast
                        if invalid:
                            pass
                        elif self.debug['reduce']:
                            print 'Reduce %s invalid by check' % lhs
                        continue
                for pitem in sets[parent]:
                    (pstate, pparent) = pitem
                    k = self.goto(pstate, lhs)
                    if k is not None:
                        why = (
                         item, i, rule)
                        pptr = (pitem, parent)
                        self.add(cur, (k, pparent), i, pptr, why)
                        nk = self.goto(k, None)
                        if nk is not None:
                            self.add(cur, (nk, i))

        return

    def makeSet_fast(self, token, sets, i):
        cur, next = sets[i], sets[(i + 1)]
        ttype = token is not None and self.typestring(token) or None
        for item in cur:
            ptr = (item, i)
            (state, parent) = item
            if ttype is not None:
                k = self.edges.get((state, ttype), None)
                if k is not None:
                    new = (
                     k, parent)
                    key = (new, i + 1)
                    if new not in next:
                        self.links[key] = []
                        next.append(new)
                    self.links[key].append((ptr, None))
                    nk = self.edges.get((k, None), None)
                    if nk is not None:
                        new = (
                         nk, i + 1)
                        if new not in next:
                            next.append(new)
            add = self.gotoST(state, token)
            for k in add:
                if k is not None:
                    self.add(next, (k, parent), i + 1, ptr)
                    nk = self.edges.get((k, None), None)
                    if nk is not None:
                        self.add(next, (nk, i + 1))

            if parent == i:
                continue
            for rule in self.states[state].complete:
                (lhs, rhs) = rule
                for pitem in sets[parent]:
                    (pstate, pparent) = pitem
                    k = self.edges.get((pstate, lhs), None)
                    if k is not None:
                        why = (
                         item, i, rule)
                        pptr = (pitem, parent)
                        new = (
                         k, pparent)
                        key = (new, i)
                        if new not in cur:
                            self.links[key] = []
                            cur.append(new)
                        self.links[key].append((pptr, why))
                        nk = self.edges.get((k, None), None)
                        if nk is not None:
                            new = (
                             nk, i)
                            if new not in cur:
                                cur.append(new)

        return

    def predecessor(self, key, causal):
        for (p, c) in self.links[key]:
            if c == causal:
                return p

        assert 0

    def causal(self, key):
        links = self.links[key]
        if len(links) == 1:
            return links[0][1]
        choices = []
        rule2cause = {}
        for (p, c) in links:
            rule = c[2]
            choices.append(rule)
            rule2cause[rule] = c

        return rule2cause[self.ambiguity(choices)]

    def deriveEpsilon(self, nt):
        if len(self.newrules[nt]) > 1:
            rule = self.ambiguity(self.newrules[nt])
        else:
            rule = self.newrules[nt][0]
        rhs = rule[1]
        attr = [None] * len(rhs)
        for i in range(len(rhs) - 1, -1, -1):
            attr[i] = self.deriveEpsilon(rhs[i])

        return self.rule2func[self.new2old[rule]](attr)

    def buildTree(self, nt, item, tokens, k):
        if self.debug['rules']:
            print (
             'NT', nt)
        (state, parent) = item
        choices = []
        for rule in self.states[state].complete:
            if rule[0] == nt:
                choices.append(rule)

        rule = choices[0]
        if len(choices) > 1:
            rule = self.ambiguity(choices)
        rhs = rule[1]
        attr = [None] * len(rhs)
        for i in range(len(rhs) - 1, -1, -1):
            sym = rhs[i]
            if sym not in self.newrules:
                if sym != self._BOF:
                    attr[i] = tokens[(k - 1)]
                    key = (item, k)
                    (item, k) = self.predecessor(key, None)
            elif self._NULLABLE == sym[0:len(self._NULLABLE)]:
                attr[i] = self.deriveEpsilon(sym)
            else:
                key = (
                 item, k)
                why = self.causal(key)
                attr[i] = self.buildTree(sym, why[0], tokens, why[1])
                (item, k) = self.predecessor(key, why)

        return self.rule2func[self.new2old[rule]](attr)

    def ambiguity(self, rules):
        sortlist = []
        name2index = {}
        for i in range(len(rules)):
            (lhs, rhs) = rule = rules[i]
            name = self.rule2name[self.new2old[rule]]
            sortlist.append((len(rhs), name))
            name2index[name] = i

        sortlist.sort()
        list = [ a_b[1] for a_b in sortlist ]
        return rules[name2index[self.resolve(list)]]

    def resolve(self, list):
        """
        Resolve ambiguity in favor of the shortest RHS.
        Since we walk the tree from the top down, this
        should effectively resolve in favor of a "shift".
        """
        return list[0]

    def dump_grammar(self, out=sys.stdout):
        """
        Print grammar rules
        """
        for rule in sorted(self.rule2name.items()):
            out.write('%s\n' % rule2str(rule[0]))

    def check_grammar(self, ok_start_symbols=set(), out=sys.stderr):
        """
        Check grammar for:
        -  unused left-hand side nonterminals that are neither start symbols
           or listed in ok_start_symbols
        -  unused right-hand side nonterminals, i.e. not tokens
        -  right-recursive rules. These can slow down parsing.
        """
        warnings = 0
        (lhs, rhs, tokens, right_recursive, dup_rhs) = self.check_sets()
        if lhs - ok_start_symbols:
            warnings += 1
            out.write('LHS symbols not used on the RHS:\n')
            out.write('  ' + ((', ').join(sorted(lhs)) + '\n'))
        if rhs:
            warnings += 1
            out.write('RHS symbols not used on the LHS:\n')
            out.write((', ').join(sorted(rhs)) + '\n')
        if right_recursive:
            warnings += 1
            out.write('Right recursive rules:\n')
            for rule in sorted(right_recursive):
                out.write('  %s ::= %s\n' % (rule[0], (' ').join(rule[1])))

        if dup_rhs:
            warnings += 1
            out.write('Nonterminals with the same RHS\n')
            for rhs in sorted(dup_rhs.keys()):
                out.write('  RHS: %s\n' % (' ').join(rhs))
                out.write('  LHS: %s\n' % (', ').join(dup_rhs[rhs]))
                out.write('  ---\n')

        return warnings

    def check_sets(self):
        """
        Check grammar
        """
        lhs_set = set()
        rhs_set = set()
        rhs_rules_set = {}
        token_set = set()
        right_recursive = set()
        dup_rhs = {}
        for lhs in self.rules:
            rules_for_lhs = self.rules[lhs]
            lhs_set.add(lhs)
            for rule in rules_for_lhs:
                rhs = rule[1]
                if len(rhs) > 0 and rhs in rhs_rules_set:
                    li = dup_rhs.get(rhs, [])
                    li.append(lhs)
                    dup_rhs[rhs] = li
                else:
                    rhs_rules_set[rhs] = lhs
                for sym in rhs:
                    if re.match('^[A-Z]', sym):
                        token_set.add(sym)
                    else:
                        rhs_set.add(sym)

                if len(rhs) > 0 and lhs == rhs[(-1)]:
                    right_recursive.add((lhs, rhs))

        lhs_set.remove(self._START)
        rhs_set.remove(self._BOF)
        missing_lhs = lhs_set - rhs_set
        missing_rhs = rhs_set - lhs_set
        for rhs in dup_rhs:
            dup_rhs[rhs].append(rhs_rules_set[rhs])

        return (
         missing_lhs, missing_rhs, token_set, right_recursive, dup_rhs)

    def reduce_string(self, rule, last_token_pos=-1):
        if last_token_pos >= 0:
            return '%s ::= %s (%d)' % (rule[0], (' ').join(rule[1]), last_token_pos)
        else:
            return '%s ::= %s' % (rule[0], (' ').join(rule[1]))

    def debug_reduce(self, rule, tokens, parent, i):
        print self.reduce_string(rule, i)

    def profile_rule(self, rule):
        """Bump count of the number of times _rule_ was used"""
        rule_str = self.reduce_string(rule)
        if rule_str not in self.profile_info:
            self.profile_info[rule_str] = 1
        else:
            self.profile_info[rule_str] += 1

    def get_profile_info(self):
        """Show the accumulated results of how many times each rule was used"""
        return sorted(self.profile_info.items(), key=lambda kv: kv[1], reverse=False)

    def dump_profile_info(self):
        if isinstance(self.coverage_path, str):
            fp = open(self.coverage_path, 'wb')
            pickle.dump(self.profile_info, fp)
            fp.close()
        else:
            for (rule, count) in self.get_profile_info():
                self.coverage_path.write('%s -- %d\n' % (rule, count))

            self.coverage_path.write('-' * 40 + '\n')

    def reduce_ast(self, rule, tokens, item, k, sets):
        rhs = rule[1]
        ast = [None] * len(rhs)
        for i in range(len(rhs) - 1, -1, -1):
            sym = rhs[i]
            if sym not in self.newrules:
                if sym != self._BOF:
                    ast[i] = tokens[(k - 1)]
                    key = (item, k)
                    (item, k) = self.predecessor(key, None)
            elif self._NULLABLE == sym[0:len(self._NULLABLE)]:
                ast[i] = self.deriveEpsilon(sym)
            else:
                key = (
                 item, k)
                why = self.causal(key)
                ast[i] = self.buildTree(sym, why[0], tokens, why[1])
                (item, k) = self.predecessor(key, why)

        return ast


class GenericASTBuilder(GenericParser):
    __module__ = __name__

    def __init__(self, AST, start, debug=DEFAULT_DEBUG):
        if 'SPARK_PARSER_COVERAGE' in os.environ:
            coverage_path = os.environ['SPARK_PARSER_COVERAGE']
        else:
            coverage_path = None
        GenericParser.__init__(self, start, debug=debug, coverage_path=coverage_path)
        self.AST = AST
        return

    def preprocess(self, rule, func):
        rebind = lambda lhs, self=self: lambda args, lhs=lhs, self=self: self.buildASTNode(args, lhs)
        (lhs, rhs) = rule
        return (rule, rebind(lhs))

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