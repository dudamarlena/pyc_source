# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/yacc.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 84868 bytes
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

    class Dummy:
        pass


    hashlib = Dummy()
    hashlib.md5 = md5.new
    del Dummy
    del md5

class YaccError(Exception):
    pass


class YaccSymbol:
    filename = ''

    def __str__(self):
        return self.type

    def __repr__(self):
        return str(self)


class YaccProduction:

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
            return [s.value for s in self.slice[n.start:n.stop:n.step]]

    def __setitem__(self, n, v):
        self.slice[n].value = v

    def __len__(self):
        return len(self.slice)

    def lineno(self, n):
        return getattr(self.slice[n], 'lineno', 0)

    def linespan(self, n):
        startline = getattr(self.slice[n], 'lineno', 0)
        endline = getattr(self.slice[n], 'endlineno', startline)
        return (
         startline, endline)

    def lexpos(self, n):
        return getattr(self.slice[n], 'lexpos', 0)

    def lexspan(self, n):
        startpos = getattr(self.slice[n], 'lexpos', 0)
        endpos = getattr(self.slice[n], 'endlexpos', startpos)
        return (
         startpos, endpos)

    def pushback(self, n):
        if n <= 0:
            raise ValueError('Expected a positive value')
        if n > len(self.slice) - 1:
            raise ValueError("Can't push %d tokens. Only %d are available." % (n, len(self.slice) - 1))
        for i in range(0, n):
            self.pbstack.append(self.slice[(-i - 1)])


class Parser:

    def __init__(self):
        self.productions = None
        self.errorfunc = None
        self.action = {}
        self.goto = {}
        self.require = {}
        self.method = 'Unknown LR'
        self.statestackstack = []
        self.symstackstack = []

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
        while 1:
            if debug > 1:
                print('state', statestack[(-1)])
            else:
                if not lookahead:
                    if not lookaheadstack:
                        lookahead = get_token()
                    else:
                        lookahead = lookaheadstack.pop()
                else:
                    if not lookahead:
                        lookahead = YaccSymbol()
                        lookahead.type = '$end'
                        lookahead.parser = self
                    if debug:
                        errorlead = ('%s . %s' % (' '.join([xx.type for xx in symstack][1:]), str(lookahead))).lstrip()
                s = statestack[(-1)]
                ltype = lookahead.type
                t = actions.get((s, ltype), None)
                if debug > 1:
                    print('action', t)
            if t is not None:
                if t > 0:
                    if ltype == '$end':
                        sys.stderr.write('yacc: Parse error. EOF\n')
                        return
                    else:
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
                                if t == None:
                                    if debug:
                                        sys.stderr.write(errorlead + '\n')
                                    self.errorcount = self.errorcount or error_count
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
                                    else:
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
                        if len(statestack) <= 1:
                            if lookahead.type != '$end':
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
    else:
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
        if n[0:2] == 'p_':
            if type(v) in (types.FunctionType, types.MethodType):
                continue
            if n[0:2] == 't_':
                pass
            else:
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


class Production:

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
            s = '%s -> %s' % (self.name, ' '.join(self.prod))
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


class MiniProduction:
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
        elif not _is_identifier.match(prodname):
            sys.stderr.write("%s:%d: Illegal rule name '%s'\n" % (file, line, prodname))
            return -1
        else:
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

                    if not _is_identifier.match(s):
                        if s != '%prec':
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
                    else:
                        prec = Precedence.get(precname, None)
                        if not prec:
                            sys.stderr.write("%s:%d: Nothing known about the precedence of '%s'\n" % (
                             p.file, p.line, precname))
                            return -1
                        p.prec = prec
                        del p.prod[i]
                        del p.prod[i]
                else:
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
        else:
            if f.__doc__:
                pstrings = f.__doc__.splitlines()
                lastp = None
                dline = line
                for ps in pstrings:
                    dline += 1
                    p = ps.split()
                    if not p:
                        pass
                    else:
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
                                if assign != ':':
                                    if assign != '::=':
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

    while 1:
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
            if s not in Prodnames:
                if s not in Terminals:
                    if s != 'error':
                        continue
            sys.stderr.write("yacc: Infinite recursion detected for symbol '%s'.\n" % s)
            some_error = 1

    return some_error


def verify_productions(cycle_check=1):
    global yaccdebug
    error = 0
    for p in Productions:
        if not p:
            pass
        else:
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
        if s != 'error':
            if not v:
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
            _vf.write('%-20s : %s\n' % (k, ' '.join([str(s) for s in Terminals[k]])))

        _vf.write('\nNonterminals, with rules where they appear\n\n')
        ks = sorted(Nonterminals.keys())
        for k in ks:
            _vf.write('%-20s : %s\n' % (k, ' '.join([str(s) for s in Nonterminals[k]])))

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
            if prec != 'left':
                if prec != 'right':
                    if prec != 'nonassoc':
                        sys.stderr.write("yacc: Invalid precedence '%s'\n" % prec)
                        return -1
            for t in terms:
                if t in Precedence:
                    sys.stderr.write("yacc: Precedence already specified for terminal '%s'\n" % t)
                    error += 1
                else:
                    Precedence[t] = (
                     prec, plevel)

        except:
            sys.stderr.write('yacc: Invalid precedence table.\n')
            error += 1

    return error


def augment_grammar(start=None):
    if not start:
        start = Productions[1].name
    Productions[0] = Production(name="S'",
      prod=[start],
      number=0,
      len=1,
      prec=('right', 0),
      func=None)
    Productions[0].usyms = [
     start]
    Nonterminals[start].append(0)


def first(beta):
    result = []
    for x in beta:
        x_produces_empty = 0
        for f in First[x]:
            if f == '<empty>':
                x_produces_empty = 1
            else:
                if f not in result:
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
    while 1:
        didadd = 0
        for p in Productions[1:]:
            for i in range(len(p.prod)):
                B = p.prod[i]
                if B in Nonterminals:
                    fst = first(p.prod[i + 1:])
                    hasempty = 0
                    for f in fst:
                        if f != '<empty>':
                            if f not in Follow[B]:
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

    if 0:
        if yaccdebug:
            _vf.write('\nFollow:\n')
            for k in Nonterminals.keys():
                _vf.write('%-20s : %s\n' % (k, ' '.join([str(s) for s in Follow[k]])))


def compute_first1():
    for t in Terminals.keys():
        First[t] = [
         t]

    First['$end'] = ['$end']
    First['#'] = ['#']
    for n in Nonterminals.keys():
        First[n] = []

    while 1:
        some_change = 0
        for n in Nonterminals.keys():
            for p in Prodnames[n]:
                for f in first(p.prod):
                    if f not in First[n]:
                        First[n].append(f)
                        some_change = 1

        if not some_change:
            break

    if 0:
        if yaccdebug:
            _vf.write('\nFirst:\n')
            for k in Nonterminals.keys():
                _vf.write('%-20s : %s\n' % (k, ' '.join([str(s) for s in First[k]])))


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
                    pass
                else:
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
            if n:
                if n.lrbefore == x:
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
                pass
            else:
                if id(g) in _lr0_cidhash:
                    pass
                else:
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
            else:
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
                if t[1] in Nonterminals and t not in trans:
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
            if a in Terminals and a not in terms:
                terms.append(a)

    if state == 0:
        if N == Productions[0].prod[0]:
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
                pass
            else:
                lr_index = p.lr_index
                j = state
                while lr_index < p.len - 1:
                    lr_index = lr_index + 1
                    t = p.prod[lr_index]
                    if (
                     j, t) in dtrans:
                        li = lr_index + 1
                        while li < p.len:
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
                        pass
                    else:
                        if r.len != p.len:
                            pass
                        else:
                            i = 0
                            while i < r.lr_index:
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

    return (
     lookdict, includedict)


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


def lr_parse_table--- This code section failed: ---

 L.1776         0  LOAD_GLOBAL              _lr_goto
                2  STORE_FAST               'goto'

 L.1777         4  LOAD_GLOBAL              _lr_action
                6  STORE_FAST               'action'

 L.1778         8  BUILD_MAP_0           0 
               10  STORE_FAST               'actionp'

 L.1780        12  LOAD_FAST                'method'
               14  STORE_GLOBAL             _lr_method

 L.1782        16  LOAD_CONST               0
               18  STORE_FAST               'n_srconflict'

 L.1783        20  LOAD_CONST               0
               22  STORE_FAST               'n_rrconflict'

 L.1785        24  LOAD_GLOBAL              yaccdebug
               26  POP_JUMP_IF_FALSE    58  'to 58'

 L.1786        28  LOAD_GLOBAL              sys
               30  LOAD_ATTR                stderr
               32  LOAD_ATTR                write
               34  LOAD_STR                 'yacc: Generating %s parsing table...\n'
               36  LOAD_FAST                'method'
               38  BINARY_MODULO    
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          

 L.1787        44  LOAD_GLOBAL              _vf
               46  LOAD_ATTR                write
               48  LOAD_STR                 '\n\nParsing method: %s\n\n'
               50  LOAD_FAST                'method'
               52  BINARY_MODULO    
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          
             58_0  COME_FROM            26  '26'

 L.1792        58  LOAD_GLOBAL              lr0_items
               60  CALL_FUNCTION_0       0  ''
               62  STORE_FAST               'C'

 L.1794        64  LOAD_FAST                'method'
               66  LOAD_STR                 'LALR'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L.1795        72  LOAD_GLOBAL              add_lalr_lookaheads
               74  LOAD_FAST                'C'
               76  CALL_FUNCTION_1       1  ''
               78  POP_TOP          
             80_0  COME_FROM            70  '70'

 L.1798        80  LOAD_CONST               0
               82  STORE_FAST               'st'

 L.1799        84  SETUP_LOOP         1658  'to 1658'
               88  LOAD_FAST                'C'
               90  GET_ITER         
               92  FOR_ITER           1656  'to 1656'
               96  STORE_FAST               'I'

 L.1801        98  BUILD_LIST_0          0 
              100  STORE_FAST               'actlist'

 L.1803       102  LOAD_GLOBAL              yaccdebug
              104  POP_JUMP_IF_FALSE   168  'to 168'

 L.1804       106  LOAD_GLOBAL              _vf
              108  LOAD_ATTR                write
              110  LOAD_STR                 '\nstate %d\n\n'
              112  LOAD_FAST                'st'
              114  BINARY_MODULO    
              116  CALL_FUNCTION_1       1  ''
              118  POP_TOP          

 L.1805       120  SETUP_LOOP          158  'to 158'
              122  LOAD_FAST                'I'
              124  GET_ITER         
              126  FOR_ITER            156  'to 156'
              128  STORE_FAST               'p'

 L.1806       130  LOAD_GLOBAL              _vf
              132  LOAD_ATTR                write
              134  LOAD_STR                 '    (%d) %s\n'
              136  LOAD_FAST                'p'
              138  LOAD_ATTR                number
              140  LOAD_GLOBAL              str
              142  LOAD_FAST                'p'
              144  CALL_FUNCTION_1       1  ''
              146  BUILD_TUPLE_2         2 
              148  BINARY_MODULO    
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          
              154  JUMP_BACK           126  'to 126'
              156  POP_BLOCK        
            158_0  COME_FROM_LOOP      120  '120'

 L.1807       158  LOAD_GLOBAL              _vf
              160  LOAD_ATTR                write
              162  LOAD_STR                 '\n'
              164  CALL_FUNCTION_1       1  ''
              166  POP_TOP          
            168_0  COME_FROM           104  '104'

 L.1809       168  SETUP_LOOP         1280  'to 1280'
              172  LOAD_FAST                'I'
              174  GET_ITER         
              176  FOR_ITER           1278  'to 1278'
              180  STORE_FAST               'p'

 L.1810       182  SETUP_EXCEPT       1226  'to 1226'

 L.1811       186  LOAD_FAST                'p'
              188  LOAD_ATTR                prod
              190  LOAD_CONST               -1
              192  BINARY_SUBSCR    
              194  LOAD_STR                 '.'
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   792  'to 792'

 L.1812       202  LOAD_FAST                'p'
              204  LOAD_ATTR                name
              206  LOAD_STR                 "S'"
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   240  'to 240'

 L.1814       212  LOAD_CONST               0
              214  LOAD_FAST                'action'
              216  LOAD_FAST                'st'
              218  LOAD_STR                 '$end'
              220  BUILD_TUPLE_2         2 
              222  STORE_SUBSCR     

 L.1815       224  LOAD_FAST                'p'
              226  LOAD_FAST                'actionp'
              228  LOAD_FAST                'st'
              230  LOAD_STR                 '$end'
              232  BUILD_TUPLE_2         2 
              234  STORE_SUBSCR     
              236  JUMP_ABSOLUTE      1222  'to 1222'
              240  ELSE                     '788'

 L.1818       240  LOAD_FAST                'method'
              242  LOAD_STR                 'LALR'
              244  COMPARE_OP               ==
              246  POP_JUMP_IF_FALSE   262  'to 262'

 L.1819       250  LOAD_FAST                'p'
              252  LOAD_ATTR                lookaheads
              254  LOAD_FAST                'st'
              256  BINARY_SUBSCR    
              258  STORE_FAST               'laheads'
              260  JUMP_FORWARD        272  'to 272'
              262  ELSE                     '272'

 L.1821       262  LOAD_GLOBAL              Follow
              264  LOAD_FAST                'p'
              266  LOAD_ATTR                name
              268  BINARY_SUBSCR    
              270  STORE_FAST               'laheads'
            272_0  COME_FROM           260  '260'

 L.1822       272  SETUP_LOOP         1222  'to 1222'
              276  LOAD_FAST                'laheads'
              278  GET_ITER         
              280  FOR_ITER            786  'to 786'
              284  STORE_FAST               'a'

 L.1823       286  LOAD_FAST                'actlist'
              288  LOAD_ATTR                append
              290  LOAD_FAST                'a'
              292  LOAD_FAST                'p'
              294  LOAD_STR                 'reduce using rule %d (%s)'
              296  LOAD_FAST                'p'
              298  LOAD_ATTR                number
              300  LOAD_FAST                'p'
              302  BUILD_TUPLE_2         2 
              304  BINARY_MODULO    
              306  BUILD_TUPLE_3         3 
              308  CALL_FUNCTION_1       1  ''
              310  POP_TOP          

 L.1824       312  LOAD_FAST                'action'
              314  LOAD_ATTR                get
              316  LOAD_FAST                'st'
              318  LOAD_FAST                'a'
              320  BUILD_TUPLE_2         2 
              322  LOAD_CONST               None
              324  CALL_FUNCTION_2       2  ''
              326  STORE_FAST               'r'

 L.1825       328  LOAD_FAST                'r'
              330  LOAD_CONST               None
              332  COMPARE_OP               is-not
              334  POP_JUMP_IF_FALSE   754  'to 754'

 L.1827       338  LOAD_FAST                'r'
              340  LOAD_CONST               0
              342  COMPARE_OP               >
              344  POP_JUMP_IF_FALSE   578  'to 578'

 L.1831       348  LOAD_GLOBAL              Productions
              350  LOAD_FAST                'actionp'
              352  LOAD_FAST                'st'
              354  LOAD_FAST                'a'
              356  BUILD_TUPLE_2         2 
              358  BINARY_SUBSCR    
              360  LOAD_ATTR                number
              362  BINARY_SUBSCR    
              364  LOAD_ATTR                prec
              366  UNPACK_SEQUENCE_2     2 
              368  STORE_FAST               'sprec'
              370  STORE_FAST               'slevel'

 L.1832       372  LOAD_GLOBAL              Precedence
              374  LOAD_ATTR                get
              376  LOAD_FAST                'a'
              378  LOAD_CONST               ('right', 0)
              380  CALL_FUNCTION_2       2  ''
              382  UNPACK_SEQUENCE_2     2 
              384  STORE_FAST               'rprec'
              386  STORE_FAST               'rlevel'

 L.1833       388  LOAD_FAST                'slevel'
              390  LOAD_FAST                'rlevel'
              392  COMPARE_OP               <
              394  POP_JUMP_IF_TRUE    418  'to 418'

 L.1834       398  LOAD_FAST                'slevel'
              400  LOAD_FAST                'rlevel'
              402  COMPARE_OP               ==
              404  POP_JUMP_IF_FALSE   500  'to 500'
              408  LOAD_FAST                'rprec'
              410  LOAD_STR                 'left'
              412  COMPARE_OP               ==
            414_0  COME_FROM           404  '404'
            414_1  COME_FROM           394  '394'
              414  POP_JUMP_IF_FALSE   500  'to 500'

 L.1837       418  LOAD_FAST                'p'
              420  LOAD_ATTR                number
              422  UNARY_NEGATIVE   
              424  LOAD_FAST                'action'
              426  LOAD_FAST                'st'
              428  LOAD_FAST                'a'
              430  BUILD_TUPLE_2         2 
              432  STORE_SUBSCR     

 L.1838       434  LOAD_FAST                'p'
              436  LOAD_FAST                'actionp'
              438  LOAD_FAST                'st'
              440  LOAD_FAST                'a'
              442  BUILD_TUPLE_2         2 
              444  STORE_SUBSCR     

 L.1839       446  LOAD_FAST                'slevel'
              448  UNARY_NOT        
              450  POP_JUMP_IF_FALSE   576  'to 576'
              454  LOAD_FAST                'rlevel'
              456  UNARY_NOT        
              458  POP_JUMP_IF_FALSE   576  'to 576'

 L.1840       462  LOAD_GLOBAL              _vfc
              464  LOAD_ATTR                write

 L.1841       466  LOAD_STR                 'shift/reduce conflict in state %d resolved as reduce.\n'

 L.1842       468  LOAD_FAST                'st'
              470  BINARY_MODULO    
              472  CALL_FUNCTION_1       1  ''
              474  POP_TOP          

 L.1844       476  LOAD_GLOBAL              _vf
              478  LOAD_ATTR                write

 L.1845       480  LOAD_STR                 '  ! shift/reduce conflict for %s resolved as reduce.\n'

 L.1846       482  LOAD_FAST                'a'
              484  BINARY_MODULO    
              486  CALL_FUNCTION_1       1  ''
              488  POP_TOP          

 L.1848       490  LOAD_FAST                'n_srconflict'
              492  LOAD_CONST               1
              494  INPLACE_ADD      
              496  STORE_FAST               'n_srconflict'
              498  JUMP_FORWARD        576  'to 576'
              500  ELSE                     '576'

 L.1849       500  LOAD_FAST                'slevel'
              502  LOAD_FAST                'rlevel'
              504  COMPARE_OP               ==
              506  POP_JUMP_IF_FALSE   534  'to 534'
              510  LOAD_FAST                'rprec'
              512  LOAD_STR                 'nonassoc'
              514  COMPARE_OP               ==
              516  POP_JUMP_IF_FALSE   534  'to 534'

 L.1850       520  LOAD_CONST               None
              522  LOAD_FAST                'action'
              524  LOAD_FAST                'st'
              526  LOAD_FAST                'a'
              528  BUILD_TUPLE_2         2 
              530  STORE_SUBSCR     
              532  JUMP_FORWARD        576  'to 576'
            534_0  COME_FROM           506  '506'

 L.1853       534  LOAD_FAST                'rlevel'
              536  POP_JUMP_IF_TRUE    752  'to 752'

 L.1854       540  LOAD_GLOBAL              _vfc
              542  LOAD_ATTR                write

 L.1855       544  LOAD_STR                 'shift/reduce conflict in state %d resolved as shift.\n'

 L.1856       546  LOAD_FAST                'st'
              548  BINARY_MODULO    
              550  CALL_FUNCTION_1       1  ''
              552  POP_TOP          

 L.1858       554  LOAD_GLOBAL              _vf
              556  LOAD_ATTR                write

 L.1859       558  LOAD_STR                 '  ! shift/reduce conflict for %s resolved as shift.\n'

 L.1860       560  LOAD_FAST                'a'
              562  BINARY_MODULO    
              564  CALL_FUNCTION_1       1  ''
              566  POP_TOP          

 L.1862       568  LOAD_FAST                'n_srconflict'
              570  LOAD_CONST               1
              572  INPLACE_ADD      
              574  STORE_FAST               'n_srconflict'
            576_0  COME_FROM           532  '532'
            576_1  COME_FROM           498  '498'
            576_2  COME_FROM           458  '458'
            576_3  COME_FROM           450  '450'
              576  JUMP_FORWARD        752  'to 752'
              578  ELSE                     '752'

 L.1863       578  LOAD_FAST                'r'
              580  LOAD_CONST               0
              582  COMPARE_OP               <
              584  POP_JUMP_IF_FALSE   736  'to 736'

 L.1866       588  LOAD_GLOBAL              Productions
              590  LOAD_FAST                'r'
              592  UNARY_NEGATIVE   
              594  BINARY_SUBSCR    
              596  STORE_FAST               'oldp'

 L.1867       598  LOAD_GLOBAL              Productions
              600  LOAD_FAST                'p'
              602  LOAD_ATTR                number
              604  BINARY_SUBSCR    
              606  STORE_FAST               'pp'

 L.1868       608  LOAD_FAST                'oldp'
              610  LOAD_ATTR                line
              612  LOAD_FAST                'pp'
              614  LOAD_ATTR                line
              616  COMPARE_OP               >
              618  POP_JUMP_IF_FALSE   650  'to 650'

 L.1869       622  LOAD_FAST                'p'
              624  LOAD_ATTR                number
              626  UNARY_NEGATIVE   
              628  LOAD_FAST                'action'
              630  LOAD_FAST                'st'
              632  LOAD_FAST                'a'
              634  BUILD_TUPLE_2         2 
              636  STORE_SUBSCR     

 L.1870       638  LOAD_FAST                'p'
              640  LOAD_FAST                'actionp'
              642  LOAD_FAST                'st'
              644  LOAD_FAST                'a'
              646  BUILD_TUPLE_2         2 
              648  STORE_SUBSCR     
            650_0  COME_FROM           618  '618'

 L.1872       650  LOAD_FAST                'n_rrconflict'
              652  LOAD_CONST               1
              654  INPLACE_ADD      
              656  STORE_FAST               'n_rrconflict'

 L.1873       658  LOAD_GLOBAL              _vfc
              660  LOAD_ATTR                write

 L.1874       662  LOAD_STR                 'reduce/reduce conflict in state %d resolved using rule %d (%s).\n'

 L.1875       664  LOAD_FAST                'st'
              666  LOAD_FAST                'actionp'
              668  LOAD_FAST                'st'
              670  LOAD_FAST                'a'
              672  BUILD_TUPLE_2         2 
              674  BINARY_SUBSCR    
              676  LOAD_ATTR                number
              678  LOAD_FAST                'actionp'
              680  LOAD_FAST                'st'
              682  LOAD_FAST                'a'
              684  BUILD_TUPLE_2         2 
              686  BINARY_SUBSCR    
              688  BUILD_TUPLE_3         3 
              690  BINARY_MODULO    
              692  CALL_FUNCTION_1       1  ''
              694  POP_TOP          

 L.1877       696  LOAD_GLOBAL              _vf
              698  LOAD_ATTR                write

 L.1878       700  LOAD_STR                 '  ! reduce/reduce conflict for %s resolved using rule %d (%s).\n'

 L.1879       702  LOAD_FAST                'a'
              704  LOAD_FAST                'actionp'
              706  LOAD_FAST                'st'
              708  LOAD_FAST                'a'
              710  BUILD_TUPLE_2         2 
              712  BINARY_SUBSCR    
              714  LOAD_ATTR                number
              716  LOAD_FAST                'actionp'
              718  LOAD_FAST                'st'
              720  LOAD_FAST                'a'
              722  BUILD_TUPLE_2         2 
              724  BINARY_SUBSCR    
              726  BUILD_TUPLE_3         3 
              728  BINARY_MODULO    
              730  CALL_FUNCTION_1       1  ''
              732  POP_TOP          
              734  JUMP_FORWARD        752  'to 752'
              736  ELSE                     '752'

 L.1882       736  LOAD_GLOBAL              sys
              738  LOAD_ATTR                stderr
              740  LOAD_ATTR                write
              742  LOAD_STR                 'Unknown conflict in state %d\n'
              744  LOAD_FAST                'st'
              746  BINARY_MODULO    
              748  CALL_FUNCTION_1       1  ''
              750  POP_TOP          
            752_0  COME_FROM           734  '734'
            752_1  COME_FROM           576  '576'
            752_2  COME_FROM           536  '536'
              752  JUMP_FORWARD        782  'to 782'
              754  ELSE                     '782'

 L.1884       754  LOAD_FAST                'p'
              756  LOAD_ATTR                number
              758  UNARY_NEGATIVE   
              760  LOAD_FAST                'action'
              762  LOAD_FAST                'st'
              764  LOAD_FAST                'a'
              766  BUILD_TUPLE_2         2 
              768  STORE_SUBSCR     

 L.1885       770  LOAD_FAST                'p'
              772  LOAD_FAST                'actionp'
              774  LOAD_FAST                'st'
              776  LOAD_FAST                'a'
              778  BUILD_TUPLE_2         2 
              780  STORE_SUBSCR     
            782_0  COME_FROM           752  '752'
              782  JUMP_BACK           280  'to 280'
              786  POP_BLOCK        
            788_0  COME_FROM_LOOP      272  '272'
              788  JUMP_FORWARD       1222  'to 1222'
              792  ELSE                     '1222'

 L.1887       792  LOAD_FAST                'p'
              794  LOAD_ATTR                lr_index
              796  STORE_FAST               'i'

 L.1888       798  LOAD_FAST                'p'
              800  LOAD_ATTR                prod
              802  LOAD_FAST                'i'
              804  LOAD_CONST               1
              806  BINARY_ADD       
              808  BINARY_SUBSCR    
              810  STORE_FAST               'a'

 L.1889       812  LOAD_FAST                'a'
              814  LOAD_GLOBAL              Terminals
              816  COMPARE_OP               in
              818  POP_JUMP_IF_FALSE  1222  'to 1222'

 L.1890       822  LOAD_GLOBAL              lr0_goto
              824  LOAD_FAST                'I'
              826  LOAD_FAST                'a'
              828  CALL_FUNCTION_2       2  ''
              830  STORE_FAST               'g'

 L.1891       832  LOAD_GLOBAL              _lr0_cidhash
              834  LOAD_ATTR                get
              836  LOAD_GLOBAL              id
              838  LOAD_FAST                'g'
              840  CALL_FUNCTION_1       1  ''
              842  LOAD_CONST               -1
              844  CALL_FUNCTION_2       2  ''
              846  STORE_FAST               'j'

 L.1892       848  LOAD_FAST                'j'
              850  LOAD_CONST               0
              852  COMPARE_OP               >=
              854  POP_JUMP_IF_FALSE  1222  'to 1222'

 L.1894       858  LOAD_FAST                'actlist'
              860  LOAD_ATTR                append
              862  LOAD_FAST                'a'
              864  LOAD_FAST                'p'
              866  LOAD_STR                 'shift and go to state %d'
              868  LOAD_FAST                'j'
              870  BINARY_MODULO    
              872  BUILD_TUPLE_3         3 
              874  CALL_FUNCTION_1       1  ''
              876  POP_TOP          

 L.1895       878  LOAD_FAST                'action'
              880  LOAD_ATTR                get
              882  LOAD_FAST                'st'
              884  LOAD_FAST                'a'
              886  BUILD_TUPLE_2         2 
              888  LOAD_CONST               None
              890  CALL_FUNCTION_2       2  ''
              892  STORE_FAST               'r'

 L.1896       894  LOAD_FAST                'r'
              896  LOAD_CONST               None
              898  COMPARE_OP               is-not
              900  POP_JUMP_IF_FALSE  1198  'to 1198'

 L.1898       904  LOAD_FAST                'r'
              906  LOAD_CONST               0
              908  COMPARE_OP               >
              910  POP_JUMP_IF_FALSE   944  'to 944'

 L.1899       914  LOAD_FAST                'r'
              916  LOAD_FAST                'j'
              918  COMPARE_OP               !=
              920  POP_JUMP_IF_FALSE  1196  'to 1196'

 L.1900       924  LOAD_GLOBAL              sys
              926  LOAD_ATTR                stderr
              928  LOAD_ATTR                write
              930  LOAD_STR                 'Shift/shift conflict in state %d\n'
              932  LOAD_FAST                'st'
              934  BINARY_MODULO    
              936  CALL_FUNCTION_1       1  ''
              938  POP_TOP          
              940  JUMP_ABSOLUTE      1222  'to 1222'
              944  ELSE                     '1196'

 L.1901       944  LOAD_FAST                'r'
              946  LOAD_CONST               0
              948  COMPARE_OP               <
              950  POP_JUMP_IF_FALSE  1180  'to 1180'

 L.1906       954  LOAD_GLOBAL              Productions
              956  LOAD_FAST                'actionp'
              958  LOAD_FAST                'st'
              960  LOAD_FAST                'a'
              962  BUILD_TUPLE_2         2 
              964  BINARY_SUBSCR    
              966  LOAD_ATTR                number
              968  BINARY_SUBSCR    
              970  LOAD_ATTR                prec
              972  UNPACK_SEQUENCE_2     2 
              974  STORE_FAST               'rprec'
              976  STORE_FAST               'rlevel'

 L.1907       978  LOAD_GLOBAL              Precedence
              980  LOAD_ATTR                get
              982  LOAD_FAST                'a'
              984  LOAD_CONST               ('right', 0)
              986  CALL_FUNCTION_2       2  ''
              988  UNPACK_SEQUENCE_2     2 
              990  STORE_FAST               'sprec'
              992  STORE_FAST               'slevel'

 L.1908       994  LOAD_FAST                'slevel'
              996  LOAD_FAST                'rlevel'
              998  COMPARE_OP               >
             1000  POP_JUMP_IF_TRUE   1024  'to 1024'

 L.1909      1004  LOAD_FAST                'slevel'
             1006  LOAD_FAST                'rlevel'
             1008  COMPARE_OP               ==
             1010  POP_JUMP_IF_FALSE  1092  'to 1092'
             1014  LOAD_FAST                'rprec'
             1016  LOAD_STR                 'left'
             1018  COMPARE_OP               !=
           1020_0  COME_FROM          1010  '1010'
           1020_1  COME_FROM          1000  '1000'
             1020  POP_JUMP_IF_FALSE  1092  'to 1092'

 L.1912      1024  LOAD_FAST                'j'
             1026  LOAD_FAST                'action'
             1028  LOAD_FAST                'st'
             1030  LOAD_FAST                'a'
             1032  BUILD_TUPLE_2         2 
             1034  STORE_SUBSCR     

 L.1913      1036  LOAD_FAST                'p'
             1038  LOAD_FAST                'actionp'
             1040  LOAD_FAST                'st'
             1042  LOAD_FAST                'a'
             1044  BUILD_TUPLE_2         2 
             1046  STORE_SUBSCR     

 L.1914      1048  LOAD_FAST                'rlevel'
             1050  POP_JUMP_IF_TRUE   1178  'to 1178'

 L.1915      1054  LOAD_FAST                'n_srconflict'
             1056  LOAD_CONST               1
             1058  INPLACE_ADD      
             1060  STORE_FAST               'n_srconflict'

 L.1916      1062  LOAD_GLOBAL              _vfc
             1064  LOAD_ATTR                write

 L.1917      1066  LOAD_STR                 'shift/reduce conflict in state %d resolved as shift.\n'

 L.1918      1068  LOAD_FAST                'st'
             1070  BINARY_MODULO    
             1072  CALL_FUNCTION_1       1  ''
             1074  POP_TOP          

 L.1920      1076  LOAD_GLOBAL              _vf
             1078  LOAD_ATTR                write

 L.1921      1080  LOAD_STR                 '  ! shift/reduce conflict for %s resolved as shift.\n'

 L.1922      1082  LOAD_FAST                'a'
             1084  BINARY_MODULO    
             1086  CALL_FUNCTION_1       1  ''
             1088  POP_TOP          
             1090  JUMP_FORWARD       1178  'to 1178'
             1092  ELSE                     '1178'

 L.1924      1092  LOAD_FAST                'slevel'
             1094  LOAD_FAST                'rlevel'
             1096  COMPARE_OP               ==
             1098  POP_JUMP_IF_FALSE  1126  'to 1126'
             1102  LOAD_FAST                'rprec'
             1104  LOAD_STR                 'nonassoc'
             1106  COMPARE_OP               ==
             1108  POP_JUMP_IF_FALSE  1126  'to 1126'

 L.1925      1112  LOAD_CONST               None
             1114  LOAD_FAST                'action'
             1116  LOAD_FAST                'st'
             1118  LOAD_FAST                'a'
             1120  BUILD_TUPLE_2         2 
             1122  STORE_SUBSCR     
             1124  JUMP_FORWARD       1178  'to 1178'
           1126_0  COME_FROM          1098  '1098'

 L.1928      1126  LOAD_FAST                'slevel'
             1128  UNARY_NOT        
             1130  POP_JUMP_IF_FALSE  1196  'to 1196'
             1134  LOAD_FAST                'rlevel'
             1136  UNARY_NOT        
             1138  POP_JUMP_IF_FALSE  1196  'to 1196'

 L.1929      1142  LOAD_FAST                'n_srconflict'
             1144  LOAD_CONST               1
             1146  INPLACE_ADD      
             1148  STORE_FAST               'n_srconflict'

 L.1930      1150  LOAD_GLOBAL              _vfc
             1152  LOAD_ATTR                write

 L.1931      1154  LOAD_STR                 'shift/reduce conflict in state %d resolved as reduce.\n'

 L.1932      1156  LOAD_FAST                'st'
             1158  BINARY_MODULO    
             1160  CALL_FUNCTION_1       1  ''
             1162  POP_TOP          

 L.1934      1164  LOAD_GLOBAL              _vf
             1166  LOAD_ATTR                write

 L.1935      1168  LOAD_STR                 '  ! shift/reduce conflict for %s resolved as reduce.\n'

 L.1936      1170  LOAD_FAST                'a'
             1172  BINARY_MODULO    
             1174  CALL_FUNCTION_1       1  ''
             1176  POP_TOP          
           1178_0  COME_FROM          1124  '1124'
           1178_1  COME_FROM          1090  '1090'
           1178_2  COME_FROM          1050  '1050'
             1178  JUMP_FORWARD       1196  'to 1196'
             1180  ELSE                     '1196'

 L.1940      1180  LOAD_GLOBAL              sys
             1182  LOAD_ATTR                stderr
             1184  LOAD_ATTR                write
             1186  LOAD_STR                 'Unknown conflict in state %d\n'
             1188  LOAD_FAST                'st'
             1190  BINARY_MODULO    
             1192  CALL_FUNCTION_1       1  ''
             1194  POP_TOP          
           1196_0  COME_FROM          1178  '1178'
           1196_1  COME_FROM          1138  '1138'
           1196_2  COME_FROM          1130  '1130'
             1196  JUMP_FORWARD       1222  'to 1222'
             1198  ELSE                     '1222'

 L.1942      1198  LOAD_FAST                'j'
             1200  LOAD_FAST                'action'
             1202  LOAD_FAST                'st'
             1204  LOAD_FAST                'a'
             1206  BUILD_TUPLE_2         2 
             1208  STORE_SUBSCR     

 L.1943      1210  LOAD_FAST                'p'
             1212  LOAD_FAST                'actionp'
             1214  LOAD_FAST                'st'
             1216  LOAD_FAST                'a'
             1218  BUILD_TUPLE_2         2 
             1220  STORE_SUBSCR     
           1222_0  COME_FROM          1196  '1196'
           1222_1  COME_FROM           854  '854'
           1222_2  COME_FROM           818  '818'
           1222_3  COME_FROM           788  '788'
             1222  POP_BLOCK        
             1224  JUMP_BACK           176  'to 176'
           1226_0  COME_FROM_EXCEPT    182  '182'

 L.1945      1226  DUP_TOP          
             1228  LOAD_GLOBAL              Exception
             1230  COMPARE_OP               exception-match
             1232  POP_JUMP_IF_FALSE  1274  'to 1274'
             1236  POP_TOP          
             1238  STORE_FAST               'e'
             1240  POP_TOP          
             1242  SETUP_FINALLY      1264  'to 1264'

 L.1946      1244  LOAD_GLOBAL              YaccError
             1246  LOAD_STR                 'Hosed in lr_parse_table'
             1248  CALL_FUNCTION_1       1  ''
             1250  LOAD_ATTR                with_traceback
             1252  LOAD_FAST                'e'
             1254  CALL_FUNCTION_1       1  ''
             1256  RAISE_VARARGS_1       1  ''
             1258  POP_BLOCK        
             1260  POP_EXCEPT       
             1262  LOAD_CONST               None
           1264_0  COME_FROM_FINALLY  1242  '1242'
             1264  LOAD_CONST               None
             1266  STORE_FAST               'e'
             1268  DELETE_FAST              'e'
             1270  END_FINALLY      
             1272  JUMP_BACK           176  'to 176'
             1274  END_FINALLY      
             1276  JUMP_BACK           176  'to 176'
             1278  POP_BLOCK        
           1280_0  COME_FROM_LOOP      168  '168'

 L.1949      1280  LOAD_GLOBAL              yaccdebug
             1282  POP_JUMP_IF_FALSE  1482  'to 1482'

 L.1950      1286  BUILD_MAP_0           0 
             1288  STORE_FAST               '_actprint'

 L.1951      1290  SETUP_LOOP         1374  'to 1374'
             1292  LOAD_FAST                'actlist'
             1294  GET_ITER         
             1296  FOR_ITER           1372  'to 1372'
             1298  UNPACK_SEQUENCE_3     3 
             1300  STORE_FAST               'a'
             1302  STORE_FAST               'p'
             1304  STORE_FAST               'm'

 L.1952      1306  LOAD_FAST                'st'
             1308  LOAD_FAST                'a'
             1310  BUILD_TUPLE_2         2 
             1312  LOAD_FAST                'action'
             1314  COMPARE_OP               in
             1316  POP_JUMP_IF_FALSE  1296  'to 1296'

 L.1953      1320  LOAD_FAST                'p'
             1322  LOAD_FAST                'actionp'
             1324  LOAD_FAST                'st'
             1326  LOAD_FAST                'a'
             1328  BUILD_TUPLE_2         2 
             1330  BINARY_SUBSCR    
             1332  COMPARE_OP               is
             1334  POP_JUMP_IF_FALSE  1296  'to 1296'

 L.1954      1338  LOAD_GLOBAL              _vf
             1340  LOAD_ATTR                write
             1342  LOAD_STR                 '    %-15s %s\n'
             1344  LOAD_FAST                'a'
             1346  LOAD_FAST                'm'
             1348  BUILD_TUPLE_2         2 
             1350  BINARY_MODULO    
             1352  CALL_FUNCTION_1       1  ''
             1354  POP_TOP          

 L.1955      1356  LOAD_CONST               1
             1358  LOAD_FAST                '_actprint'
             1360  LOAD_FAST                'a'
             1362  LOAD_FAST                'm'
             1364  BUILD_TUPLE_2         2 
             1366  STORE_SUBSCR     
             1368  JUMP_BACK          1296  'to 1296'
             1372  POP_BLOCK        
           1374_0  COME_FROM_LOOP     1290  '1290'

 L.1956      1374  LOAD_GLOBAL              _vf
             1376  LOAD_ATTR                write
             1378  LOAD_STR                 '\n'
             1380  CALL_FUNCTION_1       1  ''
             1382  POP_TOP          

 L.1957      1384  SETUP_LOOP         1482  'to 1482'
             1386  LOAD_FAST                'actlist'
             1388  GET_ITER         
             1390  FOR_ITER           1480  'to 1480'
             1392  UNPACK_SEQUENCE_3     3 
             1394  STORE_FAST               'a'
             1396  STORE_FAST               'p'
             1398  STORE_FAST               'm'

 L.1958      1400  LOAD_FAST                'st'
             1402  LOAD_FAST                'a'
             1404  BUILD_TUPLE_2         2 
             1406  LOAD_FAST                'action'
             1408  COMPARE_OP               in
             1410  POP_JUMP_IF_FALSE  1390  'to 1390'

 L.1959      1414  LOAD_FAST                'p'
             1416  LOAD_FAST                'actionp'
             1418  LOAD_FAST                'st'
             1420  LOAD_FAST                'a'
             1422  BUILD_TUPLE_2         2 
             1424  BINARY_SUBSCR    
             1426  COMPARE_OP               is-not
             1428  POP_JUMP_IF_FALSE  1390  'to 1390'

 L.1960      1432  LOAD_FAST                'a'
             1434  LOAD_FAST                'm'
             1436  BUILD_TUPLE_2         2 
             1438  LOAD_FAST                '_actprint'
             1440  COMPARE_OP               not-in
             1442  POP_JUMP_IF_FALSE  1390  'to 1390'

 L.1961      1446  LOAD_GLOBAL              _vf
             1448  LOAD_ATTR                write
             1450  LOAD_STR                 '  ! %-15s [ %s ]\n'
             1452  LOAD_FAST                'a'
             1454  LOAD_FAST                'm'
             1456  BUILD_TUPLE_2         2 
             1458  BINARY_MODULO    
             1460  CALL_FUNCTION_1       1  ''
             1462  POP_TOP          

 L.1962      1464  LOAD_CONST               1
             1466  LOAD_FAST                '_actprint'
             1468  LOAD_FAST                'a'
             1470  LOAD_FAST                'm'
             1472  BUILD_TUPLE_2         2 
             1474  STORE_SUBSCR     
             1476  JUMP_BACK          1390  'to 1390'
             1480  POP_BLOCK        
           1482_0  COME_FROM_LOOP     1384  '1384'
           1482_1  COME_FROM          1282  '1282'

 L.1965      1482  LOAD_GLOBAL              yaccdebug
             1484  POP_JUMP_IF_FALSE  1498  'to 1498'

 L.1966      1488  LOAD_GLOBAL              _vf
             1490  LOAD_ATTR                write
             1492  LOAD_STR                 '\n'
             1494  CALL_FUNCTION_1       1  ''
             1496  POP_TOP          
           1498_0  COME_FROM          1484  '1484'

 L.1967      1498  BUILD_MAP_0           0 
             1500  STORE_FAST               'nkeys'

 L.1968      1502  SETUP_LOOP         1554  'to 1554'
             1504  LOAD_FAST                'I'
             1506  GET_ITER         
             1508  FOR_ITER           1552  'to 1552'
             1510  STORE_FAST               'ii'

 L.1969      1512  SETUP_LOOP         1548  'to 1548'
             1514  LOAD_FAST                'ii'
             1516  LOAD_ATTR                usyms
             1518  GET_ITER         
             1520  FOR_ITER           1546  'to 1546'
             1522  STORE_FAST               's'

 L.1970      1524  LOAD_FAST                's'
             1526  LOAD_GLOBAL              Nonterminals
             1528  COMPARE_OP               in
             1530  POP_JUMP_IF_FALSE  1520  'to 1520'

 L.1971      1534  LOAD_CONST               None
             1536  LOAD_FAST                'nkeys'
             1538  LOAD_FAST                's'
             1540  STORE_SUBSCR     
             1542  JUMP_BACK          1520  'to 1520'
             1546  POP_BLOCK        
           1548_0  COME_FROM_LOOP     1512  '1512'
             1548  JUMP_BACK          1508  'to 1508'
             1552  POP_BLOCK        
           1554_0  COME_FROM_LOOP     1502  '1502'

 L.1972      1554  SETUP_LOOP         1646  'to 1646'
             1556  LOAD_FAST                'nkeys'
             1558  LOAD_ATTR                keys
             1560  CALL_FUNCTION_0       0  ''
             1562  GET_ITER         
             1564  FOR_ITER           1644  'to 1644'
             1566  STORE_FAST               'n'

 L.1973      1568  LOAD_GLOBAL              lr0_goto
             1570  LOAD_FAST                'I'
             1572  LOAD_FAST                'n'
             1574  CALL_FUNCTION_2       2  ''
             1576  STORE_FAST               'g'

 L.1974      1578  LOAD_GLOBAL              _lr0_cidhash
             1580  LOAD_ATTR                get
             1582  LOAD_GLOBAL              id
             1584  LOAD_FAST                'g'
             1586  CALL_FUNCTION_1       1  ''
             1588  LOAD_CONST               -1
             1590  CALL_FUNCTION_2       2  ''
             1592  STORE_FAST               'j'

 L.1975      1594  LOAD_FAST                'j'
             1596  LOAD_CONST               0
             1598  COMPARE_OP               >=
             1600  POP_JUMP_IF_FALSE  1564  'to 1564'

 L.1976      1604  LOAD_FAST                'j'
             1606  LOAD_FAST                'goto'
             1608  LOAD_FAST                'st'
             1610  LOAD_FAST                'n'
             1612  BUILD_TUPLE_2         2 
             1614  STORE_SUBSCR     

 L.1977      1616  LOAD_GLOBAL              yaccdebug
             1618  POP_JUMP_IF_FALSE  1564  'to 1564'

 L.1978      1622  LOAD_GLOBAL              _vf
             1624  LOAD_ATTR                write
             1626  LOAD_STR                 '    %-30s shift and go to state %d\n'
             1628  LOAD_FAST                'n'
             1630  LOAD_FAST                'j'
             1632  BUILD_TUPLE_2         2 
             1634  BINARY_MODULO    
             1636  CALL_FUNCTION_1       1  ''
             1638  POP_TOP          
             1640  JUMP_BACK          1564  'to 1564'
             1644  POP_BLOCK        
           1646_0  COME_FROM_LOOP     1554  '1554'

 L.1980      1646  LOAD_FAST                'st'
             1648  LOAD_CONST               1
             1650  INPLACE_ADD      
             1652  STORE_FAST               'st'
             1654  JUMP_BACK            92  'to 92'
             1656  POP_BLOCK        
           1658_0  COME_FROM_LOOP       84  '84'

 L.1982      1658  LOAD_GLOBAL              yaccdebug
             1660  POP_JUMP_IF_FALSE  1768  'to 1768'

 L.1983      1664  LOAD_FAST                'n_srconflict'
             1666  LOAD_CONST               1
             1668  COMPARE_OP               ==
             1670  POP_JUMP_IF_FALSE  1690  'to 1690'

 L.1984      1674  LOAD_GLOBAL              sys
             1676  LOAD_ATTR                stderr
             1678  LOAD_ATTR                write
             1680  LOAD_STR                 'yacc: %d shift/reduce conflict\n'
             1682  LOAD_FAST                'n_srconflict'
             1684  BINARY_MODULO    
             1686  CALL_FUNCTION_1       1  ''
             1688  POP_TOP          
           1690_0  COME_FROM          1670  '1670'

 L.1985      1690  LOAD_FAST                'n_srconflict'
             1692  LOAD_CONST               1
             1694  COMPARE_OP               >
             1696  POP_JUMP_IF_FALSE  1716  'to 1716'

 L.1986      1700  LOAD_GLOBAL              sys
             1702  LOAD_ATTR                stderr
             1704  LOAD_ATTR                write
             1706  LOAD_STR                 'yacc: %d shift/reduce conflicts\n'
             1708  LOAD_FAST                'n_srconflict'
             1710  BINARY_MODULO    
             1712  CALL_FUNCTION_1       1  ''
             1714  POP_TOP          
           1716_0  COME_FROM          1696  '1696'

 L.1987      1716  LOAD_FAST                'n_rrconflict'
             1718  LOAD_CONST               1
             1720  COMPARE_OP               ==
             1722  POP_JUMP_IF_FALSE  1742  'to 1742'

 L.1988      1726  LOAD_GLOBAL              sys
             1728  LOAD_ATTR                stderr
             1730  LOAD_ATTR                write
             1732  LOAD_STR                 'yacc: %d reduce/reduce conflict\n'
             1734  LOAD_FAST                'n_rrconflict'
             1736  BINARY_MODULO    
             1738  CALL_FUNCTION_1       1  ''
             1740  POP_TOP          
           1742_0  COME_FROM          1722  '1722'

 L.1989      1742  LOAD_FAST                'n_rrconflict'
             1744  LOAD_CONST               1
             1746  COMPARE_OP               >
             1748  POP_JUMP_IF_FALSE  1768  'to 1768'

 L.1990      1752  LOAD_GLOBAL              sys
             1754  LOAD_ATTR                stderr
             1756  LOAD_ATTR                write
             1758  LOAD_STR                 'yacc: %d reduce/reduce conflicts\n'
             1760  LOAD_FAST                'n_rrconflict'
             1762  BINARY_MODULO    
             1764  CALL_FUNCTION_1       1  ''
             1766  POP_TOP          
           1768_0  COME_FROM          1748  '1748'
           1768_1  COME_FROM          1660  '1660'

Parse error at or near `POP_BLOCK' instruction at offset 1222


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
        print("Unable to create '%s'" % filename)
        print(e)
        return


def lr_read_tables(module=tab_module, optimize=0):
    global _lr_action
    global _lr_goto
    global _lr_method
    global _lr_productions
    try:
        L = dict()
        exec('from . import %s as parsetab' % module, globals(), L)
        parsetab = L['parsetab']
        if optimize or Signature.digest() == parsetab._lr_signature:
            _lr_action = parsetab._lr_action
            _lr_goto = parsetab._lr_goto
            _lr_productions = parsetab._lr_productions
            _lr_method = parsetab._lr_method
            return 1
        else:
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
        else:
            if isinstance(module, _INSTANCETYPE):
                _items = [(k, getattr(module, k)) for k in dir(module)]
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
        if module:
            if isinstance(module, _INSTANCETYPE):
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
                        v1 = [x.split('.') for x in v]
                        Requires[r] = v1
                    except Exception:
                        print("Invalid specification for rule '%s' in require. Expected a list of strings" % r)

            if 'error' in tokens:
                print("yacc: Illegal token 'error'.  Is a reserved word.")
                raise YaccError('Illegal token name')
        else:
            for n in tokens:
                if n in Terminals:
                    print("yacc: Warning. Token '%s' multiply defined." % n)
                Terminals[n] = []

            Terminals['error'] = []
            prec = ldict.get('precedence', None)
            if prec:
                if not (isinstance(prec, list) or isinstance(prec, tuple)):
                    raise YaccError('precedence must be a list or tuple.')
                add_precedence(prec)
                Signature.update(repr(prec).encode())
            for n in tokens:
                if n not in Precedence:
                    Precedence[n] = ('right', 0)

            ef = ldict.get('p_error', None)
            if ef:
                if isinstance(ef, types.FunctionType):
                    ismethod = 0
                else:
                    if isinstance(ef, types.MethodType):
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
                print('yacc: Warning. no p_error() function is defined.')
        symbols = [ldict[f] for f in ldict.keys() if type(ldict[f]) in (types.FunctionType, types.MethodType) if ldict[f].__name__[:2] == 'p_' if ldict[f].__name__ != 'p_error']
        if len(symbols) == 0:
            raise YaccError('no rules of the form p_rulename are defined.')
        symbols.sort(key=(lambda x: x.__code__.co_firstlineno))
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
        if start:
            if start not in Prodnames:
                raise YaccError("Bad starting symbol '%s'" % start)
        augment_grammar(start)
        error = verify_productions(cycle_check=check_recursion)
        otherfunc = [ldict[f] for f in ldict.keys() if type(f) in (types.FunctionType, types.MethodType) if ldict[f].__name__[:2] != 'p_']
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
                print("yacc: can't create '%s'" % debugfile, e)

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