# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/yacc.py
# Compiled at: 2019-08-18 21:39:21
__version__ = '2.2'
yaccdebug = 1
debug_file = 'parser.out'
tab_module = 'parsetab'
default_lr = 'LALR'
error_count = 3
import re, types, sys, io, os.path
try:
    import hashlib
except ImportError:
    import md5

    class Dummy():
        pass


    hashlib = Dummy()
    hashlib.md5 = md5.new
    del Dummy
    del md5

class YaccError(Exception):
    pass


class YaccSymbol():
    filename = ''

    def __str__(self):
        return self.type

    def __repr__(self):
        return str(self)


class YaccProduction():

    def __init__(self, s, stack=None):
        self.slice = s
        self.pbstack = []
        self.stack = stack

    def __getitem__(self, n):
        if type(n) == int:
            if n >= 0:
                return self.slice[n].value
            else:
                return self.stack[n].value

        else:
            return [ s.value for s in self.slice[n.start:n.stop:n.step] ]

    def __setitem__(self, n, v):
        self.slice[n].value = v

    def __len__(self):
        return len(self.slice)

    def lineno(self, n):
        return getattr(self.slice[n], 'lineno', 0)

    def linespan(self, n):
        startline = getattr(self.slice[n], 'lineno', 0)
        endline = getattr(self.slice[n], 'endlineno', startline)
        return (startline, endline)

    def lexpos(self, n):
        return getattr(self.slice[n], 'lexpos', 0)

    def lexspan(self, n):
        startpos = getattr(self.slice[n], 'lexpos', 0)
        endpos = getattr(self.slice[n], 'endlexpos', startpos)
        return (startpos, endpos)

    def pushback(self, n):
        if n <= 0:
            raise ValueError('Expected a positive value')
        if n > len(self.slice) - 1:
            raise ValueError("Can't push %d tokens. Only %d are available." % (n, len(self.slice) - 1))
        for i in range(0, n):
            self.pbstack.append(self.slice[(-i - 1)])


class Parser():

    def __init__(self):
        self.productions = None
        self.errorfunc = None
        self.action = {}
        self.goto = {}
        self.require = {}
        self.method = 'Unknown LR'
        self.statestackstack = []
        self.symstackstack = []
        return

    def errok(self):
        self.errorcount = 0

    def restart(self):
        del self.statestack[:]
        del self.symstack[:]
        sym = YaccSymbol()
        sym.type = '$end'
        sym.parser = self
        self.symstack.append(sym)
        self.statestack.append(0)

    def push_state(self):
        """Save parser state and restart it."""
        self.statestackstack.append(self.statestack[:])
        self.symstackstack.append(self.symstack[:])
        self.restart()

    def pop_state(self):
        """Restore saved parser state."""
        self.statestack[:] = self.statestackstack.pop()
        self.symstack[:] = self.symstackstack.pop()

    def parse(self, input=None, lexer=None, debug=0):
        global errok
        global restart
        global token
        lookahead = None
        lookaheadstack = []
        actions = self.action
        goto = self.goto
        prod = self.productions
        pslice = YaccProduction(None)
        pslice.parser = self
        self.errorcount = 0
        if not lexer:
            from . import lex
            lexer = lex.lexer
        pslice.lexer = lexer
        if input:
            lexer.input(input)
        get_token = lexer.token
        statestack = []
        self.statestack = statestack
        symstack = []
        self.symstack = symstack
        pslice.stack = symstack
        errtoken = None
        statestack.append(0)
        sym = YaccSymbol()
        sym.type = '$end'
        sym.parser = self
        symstack.append(sym)
        while True:
            if debug > 1:
                print (
                 'state', statestack[(-1)])
            if not lookahead:
                if not lookaheadstack:
                    lookahead = get_token()
                else:
                    lookahead = lookaheadstack.pop()
                if not lookahead:
                    lookahead = YaccSymbol()
                    lookahead.type = '$end'
                    lookahead.parser = self
            if debug:
                errorlead = ('%s . %s' % ((' ').join([ xx.type for xx in symstack ][1:]), str(lookahead))).lstrip()
            s = statestack[(-1)]
            ltype = lookahead.type
            t = actions.get((s, ltype), None)
            if debug > 1:
                print (
                 'action', t)
            if t is not None:
                if t > 0:
                    if ltype == '$end':
                        sys.stderr.write('yacc: Parse error. EOF\n')
                        return
                    statestack.append(t)
                    if debug > 1:
                        sys.stderr.write('%-60s shift state %s\n' % (errorlead, t))
                    symstack.append(lookahead)
                    lookahead = None
                    if self.errorcount > 0:
                        self.errorcount -= 1
                    continue
                if t < 0:
                    p = prod[(-t)]
                    pname = p.name
                    plen = p.len
                    sym = YaccSymbol()
                    sym.type = pname
                    sym.value = None
                    if debug > 1:
                        sys.stderr.write('%-60s reduce %d\n' % (errorlead, -t))
                    if plen:
                        targ = symstack[-plen - 1:]
                        targ[0] = sym
                        try:
                            sym.lineno = targ[1].lineno
                            sym.filename = targ[1].filename
                            sym.endlineno = getattr(targ[(-1)], 'endlineno', targ[(-1)].lineno)
                            sym.lexpos = targ[1].lexpos
                            sym.endlexpos = getattr(targ[(-1)], 'endlexpos', targ[(-1)].lexpos)
                        except AttributeError:
                            sym.lineno = 0

                        del symstack[-plen:]
                        del statestack[-plen:]
                    else:
                        sym.lineno = 0
                        targ = [sym]
                    pslice.slice = targ
                    pslice.pbstack = []
                    p.func(pslice)
                    if pslice.pbstack:
                        lookaheadstack.append(lookahead)
                        for _t in pslice.pbstack:
                            lookaheadstack.append(_t)

                        lookahead = None
                    symstack.append(sym)
                    statestack.append(goto[(statestack[(-1)], pname)])
                    continue
                if t == 0:
                    n = symstack[(-1)]
                    return getattr(n, 'value', None)
                    sys.stderr.write(errorlead, '\n')
            if t == None:
                if debug:
                    sys.stderr.write(errorlead + '\n')
                if not self.errorcount:
                    self.errorcount = error_count
                    errtoken = lookahead
                    if self.errorfunc:
                        errok = self.errok
                        token = get_token
                        restart = self.restart
                        tok = self.errorfunc(errtoken)
                        del errok
                        del token
                        del restart
                        if not self.errorcount:
                            lookahead = tok
                            errtoken = None
                            continue
                    elif errtoken:
                        if hasattr(errtoken, 'lineno'):
                            lineno = lookahead.lineno
                        else:
                            lineno = 0
                        if lineno:
                            sys.stderr.write('yacc: Syntax error at line %d, token=%s\n' % (
                             lineno, errtoken.type))
                        else:
                            sys.stderr.write('yacc: Syntax error, token=%s' % errtoken.type)
                    else:
                        sys.stderr.write('yacc: Parse error in input. EOF\n')
                        return
                else:
                    self.errorcount = error_count
                if len(statestack) <= 1 and lookahead.type != '$end':
                    lookahead = None
                    errtoken = None
                    del lookaheadstack[:]
                    continue
                if lookahead.type == '$end':
                    return
                if lookahead.type != 'error':
                    sym = symstack[(-1)]
                    if sym.type == 'error':
                        lookahead = None
                        continue
                    t = YaccSymbol()
                    t.type = 'error'
                    if hasattr(lookahead, 'lineno'):
                        t.lineno = lookahead.lineno
                    t.value = lookahead
                    lookaheadstack.append(lookahead)
                    lookahead = t
                else:
                    symstack.pop()
                    statestack.pop()
                continue
            raise RuntimeError('yacc: internal parser error!!!\n')

        return


def validate_file(filename):
    base, ext = os.path.splitext(filename)
    if ext != '.py':
        return 1
    try:
        f = open(filename)
        lines = f.readlines()
        f.close()
    except IOError:
        return 1

    fre = re.compile('\\s*def\\s+(p_[a-zA-Z_0-9]*)\\(')
    counthash = {}
    linen = 1
    noerror = 1
    for l in lines:
        m = fre.match(l)
        if m:
            name = m.group(1)
            prev = counthash.get(name)
            if not prev:
                counthash[name] = linen
            else:
                sys.stderr.write('%s:%d: Function %s redefined. Previously defined on line %d\n' % (
                 filename, linen, name, prev))
                noerror = 0
        linen += 1

    return noerror


def validate_dict(d):
    for n, v in d.items():
        if n[0:2] == 'p_' and type(v) in (types.FunctionType, types.MethodType):
            continue
        if n[0:2] == 't_':
            continue
        if n[0:2] == 'p_':
            sys.stderr.write("yacc: Warning. '%s' not defined as a function\n" % n)
        if 1 and isinstance(v, types.FunctionType) and v.__code__.co_argcount == 1:
            try:
                doc = v.__doc__.split(' ')
                if doc[1] == ':':
                    sys.stderr.write("%s:%d: Warning. Possible grammar rule '%s' defined without p_ prefix.\n" % (
                     v.__code__.co_filename, v.__code__.co_firstlineno, n))
            except Exception:
                pass


def initialize_vars():
    global Errorfunc
    global First
    global Follow
    global LRitems
    global Nonterminals
    global Precedence
    global Prodmap
    global Prodnames
    global Productions
    global Requires
    global Signature
    global Terminals
    global _vf
    global _vfc
    Productions = [
     None]
    Prodnames = {}
    Prodmap = {}
    Terminals = {}
    Nonterminals = {}
    First = {}
    Follow = {}
    Precedence = {}
    LRitems = []
    Errorfunc = None
    Signature = hashlib.md5()
    Requires = {}
    _vf = io.StringIO()
    _vfc = io.StringIO()
    return


class Production():

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

        self.lr_index = -1
        self.lr0_added = 0
        self.lr1_added = 0
        self.usyms = []
        self.lookaheads = {}
        self.lk_added = {}
        self.setnumbers = []

    def __str__(self):
        if self.prod:
            s = '%s -> %s' % (self.name, (' ').join(self.prod))
        else:
            s = '%s -> <empty>' % self.name
        return s

    def __repr__(self):
        return str(self)

    def lr_item(self, n):
        if n > len(self.prod):
            return
        else:
            p = Production()
            p.name = self.name
            p.prod = list(self.prod)
            p.number = self.number
            p.lr_index = n
            p.lookaheads = {}
            p.setnumbers = self.setnumbers
            p.prod.insert(n, '.')
            p.prod = tuple(p.prod)
            p.len = len(p.prod)
            p.usyms = self.usyms
            try:
                p.lrafter = Prodnames[p.prod[(n + 1)]]
            except (IndexError, KeyError) as e:
                p.lrafter = []

            try:
                p.lrbefore = p.prod[(n - 1)]
            except IndexError:
                p.lrbefore = None

            return p


class MiniProduction():
    pass


_is_identifier = re.compile('^[a-zA-Z0-9_-]+$')

def add_production(f, file, line, prodname, syms):
    if prodname in Terminals:
        sys.stderr.write("%s:%d: Illegal rule name '%s'. Already defined as a token.\n" % (file, line, prodname))
        return -1
    else:
        if prodname == 'error':
            sys.stderr.write("%s:%d: Illegal rule name '%s'. error is a reserved word.\n" % (file, line, prodname))
            return -1
        if not _is_identifier.match(prodname):
            sys.stderr.write("%s:%d: Illegal rule name '%s'\n" % (file, line, prodname))
            return -1
        for x in range(len(syms)):
            s = syms[x]
            if s[0] in '\'"':
                try:
                    c = eval(s)
                    if len(c) > 1:
                        sys.stderr.write("%s:%d: Literal token %s in rule '%s' may only be a single character\n" % (
                         file, line, s, prodname))
                        return -1
                    if c not in Terminals:
                        Terminals[c] = []
                    syms[x] = c
                    continue
                except SyntaxError:
                    pass

            if not _is_identifier.match(s) and s != '%prec':
                sys.stderr.write("%s:%d: Illegal name '%s' in rule '%s'\n" % (file, line, s, prodname))
                return -1

        map = '%s -> %s' % (prodname, syms)
        if map in Prodmap:
            m = Prodmap[map]
            sys.stderr.write('%s:%d: Duplicate rule %s.\n' % (file, line, m))
            sys.stderr.write('%s:%d: Previous definition at %s:%d\n' % (file, line, m.file, m.line))
            return -1
        p = Production()
        p.name = prodname
        p.prod = syms
        p.file = file
        p.line = line
        p.func = f
        p.number = len(Productions)
        Productions.append(p)
        Prodmap[map] = p
        if prodname not in Nonterminals:
            Nonterminals[prodname] = []
        i = 0
        while i < len(p.prod):
            t = p.prod[i]
            if t == '%prec':
                try:
                    precname = p.prod[(i + 1)]
                except IndexError:
                    sys.stderr.write('%s:%d: Syntax error. Nothing follows %%prec.\n' % (p.file, p.line))
                    return -1

                prec = Precedence.get(precname, None)
                if not prec:
                    sys.stderr.write("%s:%d: Nothing known about the precedence of '%s'\n" % (
                     p.file, p.line, precname))
                    return -1
                p.prec = prec
                del p.prod[i]
                del p.prod[i]
                continue
            if t in Terminals:
                Terminals[t].append(p.number)
                if not hasattr(p, 'prec'):
                    p.prec = Precedence.get(t, ('right', 0))
            else:
                if t not in Nonterminals:
                    Nonterminals[t] = []
                Nonterminals[t].append(p.number)
            i += 1

        if not hasattr(p, 'prec'):
            p.prec = ('right', 0)
        p.len = len(p.prod)
        p.prod = tuple(p.prod)
        p.usyms = []
        for s in p.prod:
            if s not in p.usyms:
                p.usyms.append(s)

        try:
            Prodnames[p.name].append(p)
        except KeyError:
            Prodnames[p.name] = [
             p]

        return 0


def add_function(f):
    line = f.__code__.co_firstlineno
    file = f.__code__.co_filename
    error = 0
    if isinstance(f, types.MethodType):
        reqdargs = 2
    else:
        reqdargs = 1
    if f.__code__.co_argcount > reqdargs:
        sys.stderr.write("%s:%d: Rule '%s' has too many arguments.\n" % (file, line, f.__name__))
        return -1
    else:
        if f.__code__.co_argcount < reqdargs:
            sys.stderr.write("%s:%d: Rule '%s' requires an argument.\n" % (file, line, f.__name__))
            return -1
        if f.__doc__:
            pstrings = f.__doc__.splitlines()
            lastp = None
            dline = line
            for ps in pstrings:
                dline += 1
                p = ps.split()
                if not p:
                    continue
                try:
                    if p[0] == '|':
                        if not lastp:
                            sys.stderr.write("%s:%d: Misplaced '|'.\n" % (file, dline))
                            return -1
                        prodname = lastp
                        if len(p) > 1:
                            syms = p[1:]
                        else:
                            syms = []
                    else:
                        prodname = p[0]
                        lastp = prodname
                        assign = p[1]
                        if len(p) > 2:
                            syms = p[2:]
                        else:
                            syms = []
                        if assign != ':' and assign != '::=':
                            sys.stderr.write("%s:%d: Syntax error. Expected ':'\n" % (file, dline))
                            return -1
                    e = add_production(f, file, dline, prodname, syms)
                    error += e
                except Exception:
                    sys.stderr.write("%s:%d: Syntax error in rule '%s'\n" % (file, dline, ps))
                    error -= 1

        else:
            sys.stderr.write("%s:%d: No documentation string specified in function '%s'\n" % (file, line, f.__name__))
        return error


def compute_reachable():
    """
    Find each symbol that can be reached from the start symbol.
    Print a warning for any nonterminals that can't be reached.
    (Unused terminals have already had their warning.)
    """
    Reachable = {}
    for s in list(Terminals.keys()) + list(Nonterminals.keys()):
        Reachable[s] = 0

    mark_reachable_from(Productions[0].prod[0], Reachable)
    for s in Nonterminals.keys():
        if not Reachable[s]:
            sys.stderr.write("yacc: Symbol '%s' is unreachable.\n" % s)


def mark_reachable_from(s, Reachable):
    """
    Mark all symbols that are reachable from symbol s.
    """
    if Reachable[s]:
        return
    Reachable[s] = 1
    for p in Prodnames.get(s, []):
        for r in p.prod:
            mark_reachable_from(r, Reachable)


def compute_terminates():
    """
    Raise an error for any symbols that don't terminate.
    """
    Terminates = {}
    for t in Terminals.keys():
        Terminates[t] = 1

    Terminates['$end'] = 1
    for n in Nonterminals.keys():
        Terminates[n] = 0

    while True:
        some_change = 0
        for n, pl in Prodnames.items():
            for p in pl:
                for s in p.prod:
                    if not Terminates[s]:
                        p_terminates = 0
                        break
                else:
                    p_terminates = 1

                if p_terminates:
                    if not Terminates[n]:
                        Terminates[n] = 1
                        some_change = 1
                    break

        if not some_change:
            break

    some_error = 0
    for s, terminates in Terminates.items():
        if not terminates:
            if s not in Prodnames and s not in Terminals and s != 'error':
                pass
            else:
                sys.stderr.write("yacc: Infinite recursion detected for symbol '%s'.\n" % s)
                some_error = 1

    return some_error


def verify_productions(cycle_check=1):
    global yaccdebug
    error = 0
    for p in Productions:
        if not p:
            continue
        for s in p.prod:
            if s not in Prodnames and s not in Terminals and s != 'error':
                sys.stderr.write("%s:%d: Symbol '%s' used, but not defined as a token or a rule.\n" % (
                 p.file, p.line, s))
                error = 1
                continue

    unused_tok = 0
    if yaccdebug:
        _vf.write('Unused terminals:\n\n')
    for s, v in Terminals.items():
        if s != 'error' and not v:
            sys.stderr.write("yacc: Warning. Token '%s' defined, but not used.\n" % s)
            if yaccdebug:
                _vf.write('   %s\n' % s)
            unused_tok += 1

    if yaccdebug:
        _vf.write('\nGrammar\n\n')
        for i in range(1, len(Productions)):
            _vf.write('Rule %-5d %s\n' % (i, Productions[i]))

    unused_prod = 0
    for s, v in Nonterminals.items():
        if not v:
            p = Prodnames[s][0]
            sys.stderr.write("%s:%d: Warning. Rule '%s' defined, but not used.\n" % (p.file, p.line, s))
            unused_prod += 1

    if unused_tok == 1:
        sys.stderr.write('yacc: Warning. There is 1 unused token.\n')
    if unused_tok > 1:
        sys.stderr.write('yacc: Warning. There are %d unused tokens.\n' % unused_tok)
    if unused_prod == 1:
        sys.stderr.write('yacc: Warning. There is 1 unused rule.\n')
    if unused_prod > 1:
        sys.stderr.write('yacc: Warning. There are %d unused rules.\n' % unused_prod)
    if yaccdebug:
        _vf.write('\nTerminals, with rules where they appear\n\n')
        ks = sorted(Terminals.keys())
        for k in ks:
            _vf.write('%-20s : %s\n' % (k, (' ').join([ str(s) for s in Terminals[k] ])))

        _vf.write('\nNonterminals, with rules where they appear\n\n')
        ks = sorted(Nonterminals.keys())
        for k in ks:
            _vf.write('%-20s : %s\n' % (k, (' ').join([ str(s) for s in Nonterminals[k] ])))

    if cycle_check:
        compute_reachable()
        error += compute_terminates()
    return error


def build_lritems():
    for p in Productions:
        lastlri = p
        lri = p.lr_item(0)
        i = 0
        while True:
            lri = p.lr_item(i)
            lastlri.lr_next = lri
            if not lri:
                break
            lri.lr_num = len(LRitems)
            LRitems.append(lri)
            lastlri = lri
            i += 1


def add_precedence(plist):
    plevel = 0
    error = 0
    for p in plist:
        plevel += 1
        try:
            prec = p[0]
            terms = p[1:]
            if prec != 'left' and prec != 'right' and prec != 'nonassoc':
                sys.stderr.write("yacc: Invalid precedence '%s'\n" % prec)
                return -1
            for t in terms:
                if t in Precedence:
                    sys.stderr.write("yacc: Precedence already specified for terminal '%s'\n" % t)
                    error += 1
                    continue
                Precedence[t] = (
                 prec, plevel)

        except:
            sys.stderr.write('yacc: Invalid precedence table.\n')
            error += 1

    return error


def augment_grammar(start=None):
    if not start:
        start = Productions[1].name
    Productions[0] = Production(name="S'", prod=[start], number=0, len=1, prec=('right',
                                                                                0), func=None)
    Productions[0].usyms = [
     start]
    Nonterminals[start].append(0)
    return


def first(beta):
    result = []
    for x in beta:
        x_produces_empty = 0
        for f in First[x]:
            if f == '<empty>':
                x_produces_empty = 1
            elif f not in result:
                result.append(f)

        if x_produces_empty:
            pass
        else:
            break
    else:
        result.append('<empty>')

    return result


def compute_follow(start=None):
    for k in Nonterminals.keys():
        Follow[k] = []

    if not start:
        start = Productions[1].name
    Follow[start] = ['$end']
    while True:
        didadd = 0
        for p in Productions[1:]:
            for i in range(len(p.prod)):
                B = p.prod[i]
                if B in Nonterminals:
                    fst = first(p.prod[i + 1:])
                    hasempty = 0
                    for f in fst:
                        if f != '<empty>' and f not in Follow[B]:
                            Follow[B].append(f)
                            didadd = 1
                        if f == '<empty>':
                            hasempty = 1

                    if hasempty or i == len(p.prod) - 1:
                        for f in Follow[p.name]:
                            if f not in Follow[B]:
                                Follow[B].append(f)
                                didadd = 1

        if not didadd:
            break

    if 0 and yaccdebug:
        _vf.write('\nFollow:\n')
        for k in Nonterminals.keys():
            _vf.write('%-20s : %s\n' % (k, (' ').join([ str(s) for s in Follow[k] ])))


def compute_first1():
    for t in Terminals.keys():
        First[t] = [
         t]

    First['$end'] = ['$end']
    First['#'] = ['#']
    for n in Nonterminals.keys():
        First[n] = []

    while True:
        some_change = 0
        for n in Nonterminals.keys():
            for p in Prodnames[n]:
                for f in first(p.prod):
                    if f not in First[n]:
                        First[n].append(f)
                        some_change = 1

        if not some_change:
            break

    if 0 and yaccdebug:
        _vf.write('\nFirst:\n')
        for k in Nonterminals.keys():
            _vf.write('%-20s : %s\n' % (k, (' ').join([ str(s) for s in First[k] ])))


def lr_init_vars():
    global _lr0_cidhash
    global _lr_action
    global _lr_goto
    global _lr_goto_cache
    global _lr_method
    _lr_action = {}
    _lr_goto = {}
    _lr_method = 'Unknown'
    _lr_goto_cache = {}
    _lr0_cidhash = {}


_add_count = 0

def lr0_closure(I):
    global _add_count
    _add_count += 1
    prodlist = Productions
    J = I[:]
    didadd = 1
    while didadd:
        didadd = 0
        for j in J:
            for x in j.lrafter:
                if x.lr0_added == _add_count:
                    continue
                J.append(x.lr_next)
                x.lr0_added = _add_count
                didadd = 1

    return J


def lr0_goto(I, x):
    g = _lr_goto_cache.get((id(I), x), None)
    if g:
        return g
    else:
        s = _lr_goto_cache.get(x, None)
        if not s:
            s = {}
            _lr_goto_cache[x] = s
        gs = []
        for p in I:
            n = p.lr_next
            if n and n.lrbefore == x:
                s1 = s.get(id(n), None)
                if not s1:
                    s1 = {}
                    s[id(n)] = s1
                gs.append(n)
                s = s1

        g = s.get('$end', None)
        if not g:
            if gs:
                g = lr0_closure(gs)
                s['$end'] = g
            else:
                s['$end'] = gs
        _lr_goto_cache[(id(I), x)] = g
        return g


_lr0_cidhash = {}

def lr0_items():
    C = [
     lr0_closure([Productions[0].lr_next])]
    i = 0
    for I in C:
        _lr0_cidhash[id(I)] = i
        i += 1

    i = 0
    while i < len(C):
        I = C[i]
        i += 1
        asyms = {}
        for ii in I:
            for s in ii.usyms:
                asyms[s] = None

        for x in asyms.keys():
            g = lr0_goto(I, x)
            if not g:
                continue
            if id(g) in _lr0_cidhash:
                continue
            _lr0_cidhash[id(g)] = len(C)
            C.append(g)

    return C


def compute_nullable_nonterminals():
    nullable = {}
    num_nullable = 0
    while True:
        for p in Productions[1:]:
            if p.len == 0:
                nullable[p.name] = 1
                continue
            for t in p.prod:
                if t not in nullable:
                    break
            else:
                nullable[p.name] = 1

        if len(nullable) == num_nullable:
            break
        num_nullable = len(nullable)

    return nullable


def find_nonterminal_transitions(C):
    trans = []
    for state in range(len(C)):
        for p in C[state]:
            if p.lr_index < p.len - 1:
                t = (
                 state, p.prod[(p.lr_index + 1)])
                if t[1] in Nonterminals:
                    if t not in trans:
                        trans.append(t)

        state = state + 1

    return trans


def dr_relation(C, trans, nullable):
    dr_set = {}
    state, N = trans
    terms = []
    g = lr0_goto(C[state], N)
    for p in g:
        if p.lr_index < p.len - 1:
            a = p.prod[(p.lr_index + 1)]
            if a in Terminals:
                if a not in terms:
                    terms.append(a)

    if state == 0 and N == Productions[0].prod[0]:
        terms.append('$end')
    return terms


def reads_relation(C, trans, empty):
    rel = []
    state, N = trans
    g = lr0_goto(C[state], N)
    j = _lr0_cidhash.get(id(g), -1)
    for p in g:
        if p.lr_index < p.len - 1:
            a = p.prod[(p.lr_index + 1)]
            if a in empty:
                rel.append((j, a))

    return rel


def compute_lookback_includes(C, trans, nullable):
    lookdict = {}
    includedict = {}
    dtrans = {}
    for t in trans:
        dtrans[t] = 1

    for state, N in trans:
        lookb = []
        includes = []
        for p in C[state]:
            if p.name != N:
                continue
            lr_index = p.lr_index
            j = state
            while lr_index < p.len - 1:
                lr_index = lr_index + 1
                t = p.prod[lr_index]
                if (
                 j, t) in dtrans:
                    li = lr_index + 1
                    while 1:
                        if li < p.len:
                            if p.prod[li] in Terminals:
                                break
                            if p.prod[li] not in nullable:
                                break
                            li = li + 1
                    else:
                        includes.append((j, t))

                g = lr0_goto(C[j], t)
                j = _lr0_cidhash.get(id(g), -1)

            for r in C[j]:
                if r.name != p.name:
                    continue
                if r.len != p.len:
                    continue
                i = 0
                while 1:
                    if i < r.lr_index:
                        if r.prod[i] != p.prod[(i + 1)]:
                            break
                        i = i + 1
                else:
                    lookb.append((j, r))

        for i in includes:
            if i not in includedict:
                includedict[i] = []
            includedict[i].append((state, N))

        lookdict[(state, N)] = lookb

    return (lookdict, includedict)


def digraph(X, R, FP):
    N = {}
    for x in X:
        N[x] = 0

    stack = []
    F = {}
    for x in X:
        if N[x] == 0:
            traverse(x, N, stack, F, X, R, FP)

    return F


def traverse(x, N, stack, F, X, R, FP):
    stack.append(x)
    d = len(stack)
    N[x] = d
    F[x] = FP(x)
    rel = R(x)
    for y in rel:
        if N[y] == 0:
            traverse(y, N, stack, F, X, R, FP)
        N[x] = min(N[x], N[y])
        for a in F.get(y, []):
            if a not in F[x]:
                F[x].append(a)

    if N[x] == d:
        N[stack[(-1)]] = sys.maxsize
        F[stack[(-1)]] = F[x]
        element = stack.pop()
        while element != x:
            N[stack[(-1)]] = sys.maxsize
            F[stack[(-1)]] = F[x]
            element = stack.pop()


def compute_read_sets(C, ntrans, nullable):
    FP = lambda x: dr_relation(C, x, nullable)
    R = lambda x: reads_relation(C, x, nullable)
    F = digraph(ntrans, R, FP)
    return F


def compute_follow_sets(ntrans, readsets, inclsets):
    FP = lambda x: readsets[x]
    R = lambda x: inclsets.get(x, [])
    F = digraph(ntrans, R, FP)
    return F


def add_lookaheads(lookbacks, followset):
    for trans, lb in lookbacks.items():
        for state, p in lb:
            if state not in p.lookaheads:
                p.lookaheads[state] = []
            f = followset.get(trans, [])
            for a in f:
                if a not in p.lookaheads[state]:
                    p.lookaheads[state].append(a)


def add_lalr_lookaheads(C):
    nullable = compute_nullable_nonterminals()
    trans = find_nonterminal_transitions(C)
    readsets = compute_read_sets(C, trans, nullable)
    lookd, included = compute_lookback_includes(C, trans, nullable)
    followsets = compute_follow_sets(trans, readsets, included)
    add_lookaheads(lookd, followsets)


def lr_parse_table(method):
    global _lr_method
    goto = _lr_goto
    action = _lr_action
    actionp = {}
    _lr_method = method
    n_srconflict = 0
    n_rrconflict = 0
    if yaccdebug:
        sys.stderr.write('yacc: Generating %s parsing table...\n' % method)
        _vf.write('\n\nParsing method: %s\n\n' % method)
    C = lr0_items()
    if method == 'LALR':
        add_lalr_lookaheads(C)
    st = 0
    for I in C:
        actlist = []
        if yaccdebug:
            _vf.write('\nstate %d\n\n' % st)
            for p in I:
                _vf.write('    (%d) %s\n' % (p.number, str(p)))

            _vf.write('\n')
        for p in I:
            try:
                if p.prod[(-1)] == '.':
                    if p.name == "S'":
                        action[(st, '$end')] = 0
                        actionp[(st, '$end')] = p
                    else:
                        if method == 'LALR':
                            laheads = p.lookaheads[st]
                        else:
                            laheads = Follow[p.name]
                        for a in laheads:
                            actlist.append((a, p, 'reduce using rule %d (%s)' % (p.number, p)))
                            r = action.get((st, a), None)
                            if r is not None:
                                if r > 0:
                                    sprec, slevel = Productions[actionp[(st, a)].number].prec
                                    rprec, rlevel = Precedence.get(a, ('right', 0))
                                    if slevel < rlevel or slevel == rlevel and rprec == 'left':
                                        action[(st, a)] = -p.number
                                        actionp[(st, a)] = p
                                        if not slevel and not rlevel:
                                            _vfc.write('shift/reduce conflict in state %d resolved as reduce.\n' % st)
                                            _vf.write('  ! shift/reduce conflict for %s resolved as reduce.\n' % a)
                                            n_srconflict += 1
                                    elif slevel == rlevel and rprec == 'nonassoc':
                                        action[(st, a)] = None
                                    elif not rlevel:
                                        _vfc.write('shift/reduce conflict in state %d resolved as shift.\n' % st)
                                        _vf.write('  ! shift/reduce conflict for %s resolved as shift.\n' % a)
                                        n_srconflict += 1
                                elif r < 0:
                                    oldp = Productions[(-r)]
                                    pp = Productions[p.number]
                                    if oldp.line > pp.line:
                                        action[(st, a)] = -p.number
                                        actionp[(st, a)] = p
                                    n_rrconflict += 1
                                    _vfc.write('reduce/reduce conflict in state %d resolved using rule %d (%s).\n' % (
                                     st, actionp[(st, a)].number, actionp[(st, a)]))
                                    _vf.write('  ! reduce/reduce conflict for %s resolved using rule %d (%s).\n' % (
                                     a, actionp[(st, a)].number, actionp[(st, a)]))
                                else:
                                    sys.stderr.write('Unknown conflict in state %d\n' % st)
                            else:
                                action[(st, a)] = -p.number
                                actionp[(st, a)] = p

                else:
                    i = p.lr_index
                    a = p.prod[(i + 1)]
                    if a in Terminals:
                        g = lr0_goto(I, a)
                        j = _lr0_cidhash.get(id(g), -1)
                        if j >= 0:
                            actlist.append((a, p, 'shift and go to state %d' % j))
                            r = action.get((st, a), None)
                            if r is not None:
                                if r > 0:
                                    if r != j:
                                        sys.stderr.write('Shift/shift conflict in state %d\n' % st)
                                elif r < 0:
                                    rprec, rlevel = Productions[actionp[(st, a)].number].prec
                                    sprec, slevel = Precedence.get(a, ('right', 0))
                                    if slevel > rlevel or slevel == rlevel and rprec != 'left':
                                        action[(st, a)] = j
                                        actionp[(st, a)] = p
                                        if not rlevel:
                                            n_srconflict += 1
                                            _vfc.write('shift/reduce conflict in state %d resolved as shift.\n' % st)
                                            _vf.write('  ! shift/reduce conflict for %s resolved as shift.\n' % a)
                                    elif slevel == rlevel and rprec == 'nonassoc':
                                        action[(st, a)] = None
                                    elif not slevel and not rlevel:
                                        n_srconflict += 1
                                        _vfc.write('shift/reduce conflict in state %d resolved as reduce.\n' % st)
                                        _vf.write('  ! shift/reduce conflict for %s resolved as reduce.\n' % a)
                                else:
                                    sys.stderr.write('Unknown conflict in state %d\n' % st)
                            else:
                                action[(st, a)] = j
                                actionp[(st, a)] = p
            except Exception as e:
                raise YaccError('Hosed in lr_parse_table').with_traceback(e)

        if yaccdebug:
            _actprint = {}
            for a, p, m in actlist:
                if (
                 st, a) in action:
                    if p is actionp[(st, a)]:
                        _vf.write('    %-15s %s\n' % (a, m))
                        _actprint[(a, m)] = 1

            _vf.write('\n')
            for a, p, m in actlist:
                if (
                 st, a) in action:
                    if p is not actionp[(st, a)]:
                        if (
                         a, m) not in _actprint:
                            _vf.write('  ! %-15s [ %s ]\n' % (a, m))
                            _actprint[(a, m)] = 1

        if yaccdebug:
            _vf.write('\n')
        nkeys = {}
        for ii in I:
            for s in ii.usyms:
                if s in Nonterminals:
                    nkeys[s] = None

        for n in nkeys.keys():
            g = lr0_goto(I, n)
            j = _lr0_cidhash.get(id(g), -1)
            if j >= 0:
                goto[(st, n)] = j
                if yaccdebug:
                    _vf.write('    %-30s shift and go to state %d\n' % (n, j))

        st += 1

    if yaccdebug:
        if n_srconflict == 1:
            sys.stderr.write('yacc: %d shift/reduce conflict\n' % n_srconflict)
        if n_srconflict > 1:
            sys.stderr.write('yacc: %d shift/reduce conflicts\n' % n_srconflict)
        if n_rrconflict == 1:
            sys.stderr.write('yacc: %d reduce/reduce conflict\n' % n_rrconflict)
        if n_rrconflict > 1:
            sys.stderr.write('yacc: %d reduce/reduce conflicts\n' % n_rrconflict)
    return


def lr_write_tables(modulename=tab_module, outputdir=''):
    filename = os.path.join(outputdir, modulename) + '.py'
    try:
        f = open(filename, 'w')
        f.write('\n# %s\n# This file is automatically generated. Do not edit.\n\n_lr_method = %s\n\n_lr_signature = %s\n' % (
         filename, repr(_lr_method), repr(Signature.digest())))
        smaller = 1
        if smaller:
            items = {}
            for k, v in _lr_action.items():
                i = items.get(k[1])
                if not i:
                    i = ([], [])
                    items[k[1]] = i
                i[0].append(k[0])
                i[1].append(v)

            f.write('\n_lr_action_items = {')
            for k, v in items.items():
                f.write('%r:([' % k)
                for i in v[0]:
                    f.write('%r,' % i)

                f.write('],[')
                for i in v[1]:
                    f.write('%r,' % i)

                f.write(']),')

            f.write('}\n')
            f.write('\n_lr_action = { }\nfor _k, _v in _lr_action_items.items():\n   for _x,_y in zip(_v[0],_v[1]):\n       _lr_action[(_x,_k)] = _y\ndel _lr_action_items\n')
        else:
            f.write('\n_lr_action = { ')
            for k, v in _lr_action.items():
                f.write('(%r,%r):%r,' % (k[0], k[1], v))

            f.write('}\n')
        if smaller:
            items = {}
            for k, v in _lr_goto.items():
                i = items.get(k[1])
                if not i:
                    i = ([], [])
                    items[k[1]] = i
                i[0].append(k[0])
                i[1].append(v)

            f.write('\n_lr_goto_items = {')
            for k, v in items.items():
                f.write('%r:([' % k)
                for i in v[0]:
                    f.write('%r,' % i)

                f.write('],[')
                for i in v[1]:
                    f.write('%r,' % i)

                f.write(']),')

            f.write('}\n')
            f.write('\n_lr_goto = { }\nfor _k, _v in _lr_goto_items.items():\n   for _x,_y in zip(_v[0],_v[1]):\n       _lr_goto[(_x,_k)] = _y\ndel _lr_goto_items\n')
        else:
            f.write('\n_lr_goto = { ')
            for k, v in _lr_goto.items():
                f.write('(%r,%r):%r,' % (k[0], k[1], v))

            f.write('}\n')
        f.write('_lr_productions = [\n')
        for p in Productions:
            if p:
                if p.func:
                    f.write('  (%r,%d,%r,%r,%d),\n' % (p.name, p.len, p.func.__name__, p.file, p.line))
                else:
                    f.write('  (%r,%d,None,None,None),\n' % (p.name, p.len))
            else:
                f.write('  None,\n')

        f.write(']\n')
        f.close()
    except IOError as e:
        print "Unable to create '%s'" % filename
        print e
        return


def lr_read_tables(module=tab_module, optimize=0):
    global _lr_action
    global _lr_goto
    global _lr_method
    global _lr_productions
    try:
        L = dict()
        exec 'from . import %s as parsetab' % module in globals(), L
        parsetab = L['parsetab']
        if optimize or Signature.digest() == parsetab._lr_signature:
            _lr_action = parsetab._lr_action
            _lr_goto = parsetab._lr_goto
            _lr_productions = parsetab._lr_productions
            _lr_method = parsetab._lr_method
            return 1
        return 0
    except (ImportError, AttributeError):
        return 0


_INSTANCETYPE = object

def yacc(method=default_lr, debug=yaccdebug, module=None, tabmodule=tab_module, start=None, check_recursion=1, optimize=0, write_tables=1, debugfile=debug_file, outputdir='', parserclass=Parser):
    global Errorfunc
    global parse
    global parser
    global yaccdebug
    yaccdebug = debug
    initialize_vars()
    files = {}
    error = 0
    Signature.update(method.encode())
    if module:
        if isinstance(module, types.ModuleType):
            ldict = module.__dict__
        elif isinstance(module, _INSTANCETYPE):
            _items = [ (k, getattr(module, k)) for k in dir(module) ]
            ldict = {}
            for i in _items:
                ldict[i[0]] = i[1]

        else:
            raise ValueError('Expected a module')
    else:
        try:
            raise RuntimeError
        except RuntimeError:
            e, b, t = sys.exc_info()
            f = t.tb_frame
            f = f.f_back
            ldict = f.f_globals

        if not start:
            start = ldict.get('start', None)
        if start:
            Signature.update(start)
        if optimize and lr_read_tables(tabmodule, 1):
            del Productions[:]
            for p in _lr_productions:
                if not p:
                    Productions.append(None)
                else:
                    m = MiniProduction()
                    m.name = p[0]
                    m.len = p[1]
                    m.file = p[3]
                    m.line = p[4]
                    if p[2]:
                        m.func = ldict[p[2]]
                    Productions.append(m)

        else:
            if module and isinstance(module, _INSTANCETYPE):
                tokens = getattr(module, 'tokens', None)
            else:
                tokens = ldict.get('tokens', None)
            if not tokens:
                raise YaccError("module does not define a list 'tokens'")
            if not (isinstance(tokens, list) or isinstance(tokens, tuple)):
                raise YaccError('tokens must be a list or tuple.')
            requires = ldict.get('require', None)
            if requires:
                if not isinstance(requires, dict):
                    raise YaccError('require must be a dictionary.')
                for r, v in requires.items():
                    try:
                        if not isinstance(v, list):
                            raise TypeError
                        v1 = [ x.split('.') for x in v ]
                        Requires[r] = v1
                    except Exception:
                        print "Invalid specification for rule '%s' in require. Expected a list of strings" % r

            if 'error' in tokens:
                print "yacc: Illegal token 'error'.  Is a reserved word."
                raise YaccError('Illegal token name')
            for n in tokens:
                if n in Terminals:
                    print "yacc: Warning. Token '%s' multiply defined." % n
                Terminals[n] = []

            Terminals['error'] = []
            prec = ldict.get('precedence', None)
            if prec:
                if not (isinstance(prec, list) or isinstance(prec, tuple)):
                    raise YaccError('precedence must be a list or tuple.')
                add_precedence(prec)
                Signature.update(repr(prec))
            for n in tokens:
                if n not in Precedence:
                    Precedence[n] = ('right', 0)

            ef = ldict.get('p_error', None)
            if ef:
                if isinstance(ef, types.FunctionType):
                    ismethod = 0
                elif isinstance(ef, types.MethodType):
                    ismethod = 1
                else:
                    raise YaccError("'p_error' defined, but is not a function or method.")
                eline = ef.__code__.co_firstlineno
                efile = ef.__code__.co_filename
                files[efile] = None
                if ef.__code__.co_argcount != 1 + ismethod:
                    raise YaccError('%s:%d: p_error() requires 1 argument.' % (efile, eline))
                Errorfunc = ef
            else:
                print 'yacc: Warning. no p_error() function is defined.'
            symbols = [ ldict[f] for f in ldict.keys() if type(ldict[f]) in (types.FunctionType, types.MethodType) and ldict[f].__name__[:2] == 'p_' and ldict[f].__name__ != 'p_error'
                      ]
            if len(symbols) == 0:
                raise YaccError('no rules of the form p_rulename are defined.')
            symbols.sort(key=lambda x: x.__code__.co_firstlineno)
            for f in symbols:
                if add_function(f) < 0:
                    error += 1
                else:
                    files[f.__code__.co_filename] = None

        for f in symbols:
            if f.__doc__:
                Signature.update(f.__doc__.encode())

    lr_init_vars()
    if error:
        raise YaccError('Unable to construct parser.')
    if not lr_read_tables(tabmodule):
        for filename in files.keys():
            if not validate_file(filename):
                error = 1

        validate_dict(ldict)
        if start and start not in Prodnames:
            raise YaccError("Bad starting symbol '%s'" % start)
        augment_grammar(start)
        error = verify_productions(cycle_check=check_recursion)
        otherfunc = [ ldict[f] for f in ldict.keys() if type(f) in (types.FunctionType, types.MethodType) and ldict[f].__name__[:2] != 'p_'
                    ]
        if error:
            raise YaccError('Unable to construct parser.')
        build_lritems()
        compute_first1()
        compute_follow(start)
        if method in ('SLR', 'LALR'):
            lr_parse_table(method)
        else:
            raise YaccError("Unknown parsing method '%s'" % method)
        if write_tables:
            lr_write_tables(tabmodule, outputdir)
        if yaccdebug:
            try:
                f = open(os.path.join(outputdir, debugfile), 'w')
                f.write(_vfc.getvalue())
                f.write('\n\n')
                f.write(_vf.getvalue())
                f.close()
            except IOError as e:
                print (
                 "yacc: can't create '%s'" % debugfile, e)

    g = ParserPrototype('xyzzy')
    g.productions = Productions
    g.errorfunc = Errorfunc
    g.action = _lr_action
    g.goto = _lr_goto
    g.method = _lr_method
    g.require = Requires
    parser = g.init_parser()
    parse = parser.parse
    if not optimize:
        yacc_cleanup()
    return g


class ParserPrototype(object):

    def __init__(self, magic=None):
        if magic != 'xyzzy':
            raise YaccError('Use yacc()')

    def init_parser(self, parser=None):
        if not parser:
            parser = Parser()
        parser.productions = self.productions
        parser.errorfunc = self.errorfunc
        parser.action = self.action
        parser.goto = self.goto
        parser.method = self.method
        parser.require = self.require
        return parser


def yacc_cleanup():
    global Errorfunc
    global First
    global Follow
    global LRitems
    global Nonterminals
    global Precedence
    global Prodmap
    global Prodnames
    global Productions
    global Requires
    global Signature
    global Terminals
    global _lr_action
    global _lr_goto
    global _lr_goto_cache
    global _lr_method
    global _vf
    global _vfc
    del _lr_action
    del _lr_goto
    del _lr_method
    del _lr_goto_cache
    del Productions
    del Prodnames
    del Prodmap
    del Terminals
    del Nonterminals
    del First
    del Follow
    del Precedence
    del LRitems
    del Errorfunc
    del Signature
    del Requires
    del _vf
    del _vfc


def parse(*args, **kwargs):
    raise YaccError('yacc: No parser built with yacc()')