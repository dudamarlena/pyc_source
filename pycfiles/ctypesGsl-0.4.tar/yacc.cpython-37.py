# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
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
            if not lookahead:
                if not lookaheadstack:
                    lookahead = get_token()
                else:
                    lookahead = lookaheadstack.pop()
                if not lookahead:
                    lookahead = YaccSymbol()
                    lookahead.type = '$end'
                    lookahead.parser = self
                else:
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
                    else:
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
            continue
        if n[0:2] == 'p_':
            sys.stderr.write("yacc: Warning. '%s' not defined as a function\n" % n)
        if isinstance(v, types.FunctionType) and v.__code__.co_argcount == 1:
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
            try:
                p.lrafter = []
            finally:
                e = None
                del e

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

                if _is_identifier.match(s) or s != '%prec':
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
    else:
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
                        else:
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
        if s != 'error':
            v or sys.stderr.write("yacc: Warning. Token '%s' defined, but not used.\n" % s)
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

        if x_produces_empty:
            continue
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
                    continue
                J.append(x.lr_next)
                x.lr0_added = _add_count
                didadd = 1

    return J


def lr0_goto(I, x):
    g = _lr_goto_cache.get((id(I), x), None)
    if g:
        return g
    s = _lr_goto_cache.get(x, None)
    if not s:
        s = {}
        _lr_goto_cache[x] = s
    else:
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
                continue
            if id(g) in _lr0_cidhash:
                continue
            _lr0_cidhash[id(g)] = len(C)
            C.append(g)

    return C


def compute_nullable_nonterminals():
    nullable = {}
    num_nullable = 0
    while 1:
        for p in Productions[1:]:
            if p.len == 0:
                nullable[p.name] = 1
                continue
            for t in p.prod:
                if t not in nullable:
                    break
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
                                    if not slevel < rlevel:
                                        if not slevel == rlevel or rprec == 'left':
                                            action[(st, a)] = -p.number
                                            actionp[(st, a)] = p
                                            if not slevel:
                                                if not rlevel:
                                                    _vfc.write('shift/reduce conflict in state %d resolved as reduce.\n' % st)
                                                    _vf.write('  ! shift/reduce conflict for %s resolved as reduce.\n' % a)
                                                    n_srconflict += 1
                                                elif slevel == rlevel and rprec == 'nonassoc':
                                                    action[(st, a)] = None
                                                else:
                                                    rlevel or _vfc.write('shift/reduce conflict in state %d resolved as shift.\n' % st)
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
                                    if not (slevel > rlevel or slevel) == rlevel or rprec != 'left':
                                        action[(st, a)] = j
                                        actionp[(st, a)] = p
                                        if not rlevel:
                                            n_srconflict += 1
                                            _vfc.write('shift/reduce conflict in state %d resolved as shift.\n' % st)
                                            _vf.write('  ! shift/reduce conflict for %s resolved as shift.\n' % a)
                                        elif slevel == rlevel and rprec == 'nonassoc':
                                            action[(st, a)] = None
                                        else:
                                            slevel or rlevel or n_srconflict += 1
                                            _vfc.write('shift/reduce conflict in state %d resolved as reduce.\n' % st)
                                            _vf.write('  ! shift/reduce conflict for %s resolved as reduce.\n' % a)
                                else:
                                    sys.stderr.write('Unknown conflict in state %d\n' % st)
                            else:
                                action[(st, a)] = j
                                actionp[(st, a)] = p
            except Exception as e:
                try:
                    raise YaccError('Hosed in lr_parse_table').with_traceback(e)
                finally:
                    e = None
                    del e

        if yaccdebug:
            _actprint = {}
            for a, p, m in actlist:
                if (
                 st, a) in action and p is actionp[(st, a)]:
                    _vf.write('    %-15s %s\n' % (a, m))
                    _actprint[(a, m)] = 1

            _vf.write('\n')
            for a, p, m in actlist:
                if (
                 st, a) in action and p is not actionp[(st, a)] and (
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
        try:
            print("Unable to create '%s'" % filename)
            print(e)
            return
        finally:
            e = None
            del e


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
        return 0
    except (ImportError, AttributeError):
        return 0


_INSTANCETYPE = object

def yacc--- This code section failed: ---

 L.2168         0  LOAD_FAST                'debug'
                2  STORE_GLOBAL             yaccdebug

 L.2170         4  LOAD_GLOBAL              initialize_vars
                6  CALL_FUNCTION_0       0  ''
                8  POP_TOP          

 L.2171        10  BUILD_MAP_0           0 
               12  STORE_FAST               'files'

 L.2172        14  LOAD_CONST               0
               16  STORE_FAST               'error'

 L.2175        18  LOAD_GLOBAL              Signature
               20  LOAD_METHOD              update
               22  LOAD_FAST                'method'
               24  LOAD_METHOD              encode
               26  CALL_METHOD_0         0  ''
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2180        32  LOAD_DEREF               'module'
               34  POP_JUMP_IF_FALSE   134  'to 134'

 L.2182        36  LOAD_GLOBAL              isinstance
               38  LOAD_DEREF               'module'
               40  LOAD_GLOBAL              types
               42  LOAD_ATTR                ModuleType
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.2183        48  LOAD_DEREF               'module'
               50  LOAD_ATTR                __dict__
               52  STORE_DEREF              'ldict'
               54  JUMP_ABSOLUTE       196  'to 196'
             56_0  COME_FROM            46  '46'

 L.2184        56  LOAD_GLOBAL              isinstance
               58  LOAD_DEREF               'module'
               60  LOAD_GLOBAL              _INSTANCETYPE
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE   124  'to 124'

 L.2185        66  LOAD_CLOSURE             'module'
               68  BUILD_TUPLE_1         1 
               70  LOAD_LISTCOMP            '<code_object <listcomp>>'
               72  LOAD_STR                 'yacc.<locals>.<listcomp>'
               74  MAKE_FUNCTION_8          'closure'
               76  LOAD_GLOBAL              dir
               78  LOAD_DEREF               'module'
               80  CALL_FUNCTION_1       1  ''
               82  GET_ITER         
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               '_items'

 L.2186        88  BUILD_MAP_0           0 
               90  STORE_DEREF              'ldict'

 L.2187        92  SETUP_LOOP          132  'to 132'
               94  LOAD_FAST                '_items'
               96  GET_ITER         
               98  FOR_ITER            120  'to 120'
              100  STORE_FAST               'i'

 L.2188       102  LOAD_FAST                'i'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_DEREF               'ldict'
              110  LOAD_FAST                'i'
              112  LOAD_CONST               0
              114  BINARY_SUBSCR    
              116  STORE_SUBSCR     
              118  JUMP_BACK            98  'to 98'
              120  POP_BLOCK        
              122  JUMP_ABSOLUTE       196  'to 196'
            124_0  COME_FROM            64  '64'

 L.2190       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'Expected a module'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  ''
            132_0  COME_FROM_LOOP       92  '92'
              132  JUMP_FORWARD        196  'to 196'
            134_0  COME_FROM            34  '34'

 L.2196       134  SETUP_EXCEPT        144  'to 144'

 L.2197       136  LOAD_GLOBAL              RuntimeError
              138  RAISE_VARARGS_1       1  ''
              140  POP_BLOCK        
              142  JUMP_FORWARD        196  'to 196'
            144_0  COME_FROM_EXCEPT    134  '134'

 L.2198       144  DUP_TOP          
              146  LOAD_GLOBAL              RuntimeError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   194  'to 194'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L.2199       158  LOAD_GLOBAL              sys
              160  LOAD_METHOD              exc_info
              162  CALL_METHOD_0         0  ''
              164  UNPACK_SEQUENCE_3     3 
              166  STORE_FAST               'e'
              168  STORE_FAST               'b'
              170  STORE_FAST               't'

 L.2200       172  LOAD_FAST                't'
              174  LOAD_ATTR                tb_frame
              176  STORE_FAST               'f'

 L.2201       178  LOAD_FAST                'f'
              180  LOAD_ATTR                f_back
              182  STORE_FAST               'f'

 L.2202       184  LOAD_FAST                'f'
              186  LOAD_ATTR                f_globals
              188  STORE_DEREF              'ldict'
              190  POP_EXCEPT       
              192  JUMP_FORWARD        196  'to 196'
            194_0  COME_FROM           150  '150'
              194  END_FINALLY      
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           142  '142'
            196_2  COME_FROM           132  '132'

 L.2205       196  LOAD_FAST                'start'
              198  POP_JUMP_IF_TRUE    212  'to 212'

 L.2206       200  LOAD_DEREF               'ldict'
              202  LOAD_METHOD              get
              204  LOAD_STR                 'start'
              206  LOAD_CONST               None
              208  CALL_METHOD_2         2  ''
              210  STORE_FAST               'start'
            212_0  COME_FROM           198  '198'

 L.2207       212  LOAD_FAST                'start'
              214  POP_JUMP_IF_FALSE   226  'to 226'

 L.2208       216  LOAD_GLOBAL              Signature
              218  LOAD_METHOD              update
              220  LOAD_FAST                'start'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
            226_0  COME_FROM           214  '214'

 L.2212       226  LOAD_FAST                'optimize'
          228_230  POP_JUMP_IF_FALSE   372  'to 372'
              232  LOAD_GLOBAL              lr_read_tables
              234  LOAD_FAST                'tabmodule'
              236  LOAD_CONST               1
              238  CALL_FUNCTION_2       2  ''
          240_242  POP_JUMP_IF_FALSE   372  'to 372'

 L.2214       244  LOAD_GLOBAL              Productions
              246  LOAD_CONST               None
              248  LOAD_CONST               None
              250  BUILD_SLICE_2         2 
              252  DELETE_SUBSCR    

 L.2215       254  SETUP_LOOP          368  'to 368'
              256  LOAD_GLOBAL              _lr_productions
              258  GET_ITER         
              260  FOR_ITER            366  'to 366'
              262  STORE_FAST               'p'

 L.2216       264  LOAD_FAST                'p'
          266_268  POP_JUMP_IF_TRUE    282  'to 282'

 L.2217       270  LOAD_GLOBAL              Productions
              272  LOAD_METHOD              append
              274  LOAD_CONST               None
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
              280  JUMP_BACK           260  'to 260'
            282_0  COME_FROM           266  '266'

 L.2219       282  LOAD_GLOBAL              MiniProduction
              284  CALL_FUNCTION_0       0  ''
              286  STORE_FAST               'm'

 L.2220       288  LOAD_FAST                'p'
              290  LOAD_CONST               0
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'm'
              296  STORE_ATTR               name

 L.2221       298  LOAD_FAST                'p'
              300  LOAD_CONST               1
              302  BINARY_SUBSCR    
              304  LOAD_FAST                'm'
              306  STORE_ATTR               len

 L.2222       308  LOAD_FAST                'p'
              310  LOAD_CONST               3
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'm'
              316  STORE_ATTR               file

 L.2223       318  LOAD_FAST                'p'
              320  LOAD_CONST               4
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'm'
              326  STORE_ATTR               line

 L.2224       328  LOAD_FAST                'p'
              330  LOAD_CONST               2
              332  BINARY_SUBSCR    
          334_336  POP_JUMP_IF_FALSE   352  'to 352'

 L.2225       338  LOAD_DEREF               'ldict'
              340  LOAD_FAST                'p'
              342  LOAD_CONST               2
              344  BINARY_SUBSCR    
              346  BINARY_SUBSCR    
              348  LOAD_FAST                'm'
              350  STORE_ATTR               func
            352_0  COME_FROM           334  '334'

 L.2226       352  LOAD_GLOBAL              Productions
              354  LOAD_METHOD              append
              356  LOAD_FAST                'm'
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
          362_364  JUMP_BACK           260  'to 260'
              366  POP_BLOCK        
            368_0  COME_FROM_LOOP      254  '254'
          368_370  JUMP_FORWARD       1432  'to 1432'
            372_0  COME_FROM           240  '240'
            372_1  COME_FROM           228  '228'

 L.2230       372  LOAD_DEREF               'module'
          374_376  POP_JUMP_IF_FALSE   404  'to 404'
              378  LOAD_GLOBAL              isinstance
              380  LOAD_DEREF               'module'
              382  LOAD_GLOBAL              _INSTANCETYPE
              384  CALL_FUNCTION_2       2  ''
          386_388  POP_JUMP_IF_FALSE   404  'to 404'

 L.2231       390  LOAD_GLOBAL              getattr
              392  LOAD_DEREF               'module'
              394  LOAD_STR                 'tokens'
              396  LOAD_CONST               None
              398  CALL_FUNCTION_3       3  ''
              400  STORE_FAST               'tokens'
              402  JUMP_FORWARD        416  'to 416'
            404_0  COME_FROM           386  '386'
            404_1  COME_FROM           374  '374'

 L.2233       404  LOAD_DEREF               'ldict'
              406  LOAD_METHOD              get
              408  LOAD_STR                 'tokens'
              410  LOAD_CONST               None
              412  CALL_METHOD_2         2  ''
              414  STORE_FAST               'tokens'
            416_0  COME_FROM           402  '402'

 L.2235       416  LOAD_FAST                'tokens'
          418_420  POP_JUMP_IF_TRUE    430  'to 430'

 L.2236       422  LOAD_GLOBAL              YaccError
              424  LOAD_STR                 "module does not define a list 'tokens'"
              426  CALL_FUNCTION_1       1  ''
              428  RAISE_VARARGS_1       1  ''
            430_0  COME_FROM           418  '418'

 L.2237       430  LOAD_GLOBAL              isinstance
              432  LOAD_FAST                'tokens'
              434  LOAD_GLOBAL              list
              436  CALL_FUNCTION_2       2  ''
          438_440  POP_JUMP_IF_TRUE    462  'to 462'
              442  LOAD_GLOBAL              isinstance
              444  LOAD_FAST                'tokens'
              446  LOAD_GLOBAL              tuple
              448  CALL_FUNCTION_2       2  ''
          450_452  POP_JUMP_IF_TRUE    462  'to 462'

 L.2238       454  LOAD_GLOBAL              YaccError
              456  LOAD_STR                 'tokens must be a list or tuple.'
              458  CALL_FUNCTION_1       1  ''
              460  RAISE_VARARGS_1       1  ''
            462_0  COME_FROM           450  '450'
            462_1  COME_FROM           438  '438'

 L.2241       462  LOAD_DEREF               'ldict'
              464  LOAD_METHOD              get
              466  LOAD_STR                 'require'
              468  LOAD_CONST               None
              470  CALL_METHOD_2         2  ''
              472  STORE_FAST               'requires'

 L.2242       474  LOAD_FAST                'requires'
          476_478  POP_JUMP_IF_FALSE   602  'to 602'

 L.2243       480  LOAD_GLOBAL              isinstance
              482  LOAD_FAST                'requires'
              484  LOAD_GLOBAL              dict
              486  CALL_FUNCTION_2       2  ''
          488_490  POP_JUMP_IF_TRUE    500  'to 500'

 L.2244       492  LOAD_GLOBAL              YaccError
              494  LOAD_STR                 'require must be a dictionary.'
              496  CALL_FUNCTION_1       1  ''
              498  RAISE_VARARGS_1       1  ''
            500_0  COME_FROM           488  '488'

 L.2246       500  SETUP_LOOP          602  'to 602'
              502  LOAD_FAST                'requires'
              504  LOAD_METHOD              items
              506  CALL_METHOD_0         0  ''
              508  GET_ITER         
              510  FOR_ITER            600  'to 600'
              512  UNPACK_SEQUENCE_2     2 
              514  STORE_FAST               'r'
              516  STORE_FAST               'v'

 L.2247       518  SETUP_EXCEPT        562  'to 562'

 L.2248       520  LOAD_GLOBAL              isinstance
              522  LOAD_FAST                'v'
              524  LOAD_GLOBAL              list
              526  CALL_FUNCTION_2       2  ''
          528_530  POP_JUMP_IF_TRUE    536  'to 536'

 L.2249       532  LOAD_GLOBAL              TypeError
              534  RAISE_VARARGS_1       1  ''
            536_0  COME_FROM           528  '528'

 L.2250       536  LOAD_LISTCOMP            '<code_object <listcomp>>'
              538  LOAD_STR                 'yacc.<locals>.<listcomp>'
              540  MAKE_FUNCTION_0          ''
              542  LOAD_FAST                'v'
              544  GET_ITER         
              546  CALL_FUNCTION_1       1  ''
              548  STORE_FAST               'v1'

 L.2251       550  LOAD_FAST                'v1'
              552  LOAD_GLOBAL              Requires
              554  LOAD_FAST                'r'
              556  STORE_SUBSCR     
              558  POP_BLOCK        
              560  JUMP_BACK           510  'to 510'
            562_0  COME_FROM_EXCEPT    518  '518'

 L.2252       562  DUP_TOP          
              564  LOAD_GLOBAL              Exception
              566  COMPARE_OP               exception-match
          568_570  POP_JUMP_IF_FALSE   594  'to 594'
              572  POP_TOP          
              574  POP_TOP          
              576  POP_TOP          

 L.2253       578  LOAD_GLOBAL              print

 L.2254       580  LOAD_STR                 "Invalid specification for rule '%s' in require. Expected a list of strings"

 L.2255       582  LOAD_FAST                'r'
              584  BINARY_MODULO    
              586  CALL_FUNCTION_1       1  ''
              588  POP_TOP          
              590  POP_EXCEPT       
              592  JUMP_BACK           510  'to 510'
            594_0  COME_FROM           568  '568'
              594  END_FINALLY      
          596_598  JUMP_BACK           510  'to 510'
              600  POP_BLOCK        
            602_0  COME_FROM_LOOP      500  '500'
            602_1  COME_FROM           476  '476'

 L.2262       602  LOAD_STR                 'error'
              604  LOAD_FAST                'tokens'
              606  COMPARE_OP               in
          608_610  POP_JUMP_IF_FALSE   628  'to 628'

 L.2263       612  LOAD_GLOBAL              print
              614  LOAD_STR                 "yacc: Illegal token 'error'.  Is a reserved word."
              616  CALL_FUNCTION_1       1  ''
              618  POP_TOP          

 L.2264       620  LOAD_GLOBAL              YaccError
              622  LOAD_STR                 'Illegal token name'
              624  CALL_FUNCTION_1       1  ''
              626  RAISE_VARARGS_1       1  ''
            628_0  COME_FROM           608  '608'

 L.2266       628  SETUP_LOOP          674  'to 674'
              630  LOAD_FAST                'tokens'
              632  GET_ITER         
              634  FOR_ITER            672  'to 672'
              636  STORE_FAST               'n'

 L.2267       638  LOAD_FAST                'n'
              640  LOAD_GLOBAL              Terminals
              642  COMPARE_OP               in
          644_646  POP_JUMP_IF_FALSE   660  'to 660'

 L.2268       648  LOAD_GLOBAL              print
              650  LOAD_STR                 "yacc: Warning. Token '%s' multiply defined."
              652  LOAD_FAST                'n'
              654  BINARY_MODULO    
              656  CALL_FUNCTION_1       1  ''
              658  POP_TOP          
            660_0  COME_FROM           644  '644'

 L.2269       660  BUILD_LIST_0          0 
              662  LOAD_GLOBAL              Terminals
              664  LOAD_FAST                'n'
              666  STORE_SUBSCR     
          668_670  JUMP_BACK           634  'to 634'
              672  POP_BLOCK        
            674_0  COME_FROM_LOOP      628  '628'

 L.2271       674  BUILD_LIST_0          0 
              676  LOAD_GLOBAL              Terminals
              678  LOAD_STR                 'error'
              680  STORE_SUBSCR     

 L.2274       682  LOAD_DEREF               'ldict'
              684  LOAD_METHOD              get
              686  LOAD_STR                 'precedence'
              688  LOAD_CONST               None
              690  CALL_METHOD_2         2  ''
              692  STORE_FAST               'prec'

 L.2275       694  LOAD_FAST                'prec'
          696_698  POP_JUMP_IF_FALSE   758  'to 758'

 L.2276       700  LOAD_GLOBAL              isinstance
              702  LOAD_FAST                'prec'
              704  LOAD_GLOBAL              list
              706  CALL_FUNCTION_2       2  ''
          708_710  POP_JUMP_IF_TRUE    732  'to 732'
              712  LOAD_GLOBAL              isinstance
              714  LOAD_FAST                'prec'
              716  LOAD_GLOBAL              tuple
              718  CALL_FUNCTION_2       2  ''
          720_722  POP_JUMP_IF_TRUE    732  'to 732'

 L.2277       724  LOAD_GLOBAL              YaccError
              726  LOAD_STR                 'precedence must be a list or tuple.'
              728  CALL_FUNCTION_1       1  ''
              730  RAISE_VARARGS_1       1  ''
            732_0  COME_FROM           720  '720'
            732_1  COME_FROM           708  '708'

 L.2278       732  LOAD_GLOBAL              add_precedence
              734  LOAD_FAST                'prec'
              736  CALL_FUNCTION_1       1  ''
              738  POP_TOP          

 L.2279       740  LOAD_GLOBAL              Signature
              742  LOAD_METHOD              update
              744  LOAD_GLOBAL              repr
              746  LOAD_FAST                'prec'
              748  CALL_FUNCTION_1       1  ''
              750  LOAD_METHOD              encode
              752  CALL_METHOD_0         0  ''
              754  CALL_METHOD_1         1  ''
              756  POP_TOP          
            758_0  COME_FROM           696  '696'

 L.2281       758  SETUP_LOOP          792  'to 792'
              760  LOAD_FAST                'tokens'
              762  GET_ITER         
            764_0  COME_FROM           774  '774'
              764  FOR_ITER            790  'to 790'
              766  STORE_FAST               'n'

 L.2282       768  LOAD_FAST                'n'
              770  LOAD_GLOBAL              Precedence
              772  COMPARE_OP               not-in
          774_776  POP_JUMP_IF_FALSE   764  'to 764'

 L.2283       778  LOAD_CONST               ('right', 0)
              780  LOAD_GLOBAL              Precedence
              782  LOAD_FAST                'n'
              784  STORE_SUBSCR     
          786_788  JUMP_BACK           764  'to 764'
              790  POP_BLOCK        
            792_0  COME_FROM_LOOP      758  '758'

 L.2286       792  LOAD_DEREF               'ldict'
              794  LOAD_METHOD              get
              796  LOAD_STR                 'p_error'
              798  LOAD_CONST               None
              800  CALL_METHOD_2         2  ''
              802  STORE_FAST               'ef'

 L.2287       804  LOAD_FAST                'ef'
          806_808  POP_JUMP_IF_FALSE   922  'to 922'

 L.2288       810  LOAD_GLOBAL              isinstance
              812  LOAD_FAST                'ef'
              814  LOAD_GLOBAL              types
              816  LOAD_ATTR                FunctionType
              818  CALL_FUNCTION_2       2  ''
          820_822  POP_JUMP_IF_FALSE   830  'to 830'

 L.2289       824  LOAD_CONST               0
              826  STORE_FAST               'ismethod'
              828  JUMP_FORWARD        858  'to 858'
            830_0  COME_FROM           820  '820'

 L.2290       830  LOAD_GLOBAL              isinstance
              832  LOAD_FAST                'ef'
              834  LOAD_GLOBAL              types
              836  LOAD_ATTR                MethodType
              838  CALL_FUNCTION_2       2  ''
          840_842  POP_JUMP_IF_FALSE   850  'to 850'

 L.2291       844  LOAD_CONST               1
              846  STORE_FAST               'ismethod'
              848  JUMP_FORWARD        858  'to 858'
            850_0  COME_FROM           840  '840'

 L.2293       850  LOAD_GLOBAL              YaccError
              852  LOAD_STR                 "'p_error' defined, but is not a function or method."
              854  CALL_FUNCTION_1       1  ''
              856  RAISE_VARARGS_1       1  ''
            858_0  COME_FROM           848  '848'
            858_1  COME_FROM           828  '828'

 L.2294       858  LOAD_FAST                'ef'
              860  LOAD_ATTR                __code__
              862  LOAD_ATTR                co_firstlineno
              864  STORE_FAST               'eline'

 L.2295       866  LOAD_FAST                'ef'
              868  LOAD_ATTR                __code__
              870  LOAD_ATTR                co_filename
              872  STORE_FAST               'efile'

 L.2296       874  LOAD_CONST               None
              876  LOAD_FAST                'files'
              878  LOAD_FAST                'efile'
              880  STORE_SUBSCR     

 L.2298       882  LOAD_FAST                'ef'
              884  LOAD_ATTR                __code__
              886  LOAD_ATTR                co_argcount
              888  LOAD_CONST               1
              890  LOAD_FAST                'ismethod'
              892  BINARY_ADD       
              894  COMPARE_OP               !=
          896_898  POP_JUMP_IF_FALSE   916  'to 916'

 L.2299       900  LOAD_GLOBAL              YaccError
              902  LOAD_STR                 '%s:%d: p_error() requires 1 argument.'
              904  LOAD_FAST                'efile'
              906  LOAD_FAST                'eline'
              908  BUILD_TUPLE_2         2 
              910  BINARY_MODULO    
              912  CALL_FUNCTION_1       1  ''
              914  RAISE_VARARGS_1       1  ''
            916_0  COME_FROM           896  '896'

 L.2301       916  LOAD_FAST                'ef'
              918  STORE_GLOBAL             Errorfunc
              920  JUMP_FORWARD        930  'to 930'
            922_0  COME_FROM           806  '806'

 L.2303       922  LOAD_GLOBAL              print
              924  LOAD_STR                 'yacc: Warning. no p_error() function is defined.'
              926  CALL_FUNCTION_1       1  ''
              928  POP_TOP          
            930_0  COME_FROM           920  '920'

 L.2307       930  LOAD_CLOSURE             'ldict'
              932  BUILD_TUPLE_1         1 
              934  LOAD_LISTCOMP            '<code_object <listcomp>>'
              936  LOAD_STR                 'yacc.<locals>.<listcomp>'
              938  MAKE_FUNCTION_8          'closure'

 L.2308       940  LOAD_DEREF               'ldict'
              942  LOAD_METHOD              keys
              944  CALL_METHOD_0         0  ''
              946  GET_ITER         
              948  CALL_FUNCTION_1       1  ''
              950  STORE_FAST               'symbols'

 L.2317       952  LOAD_GLOBAL              len
              954  LOAD_FAST                'symbols'
              956  CALL_FUNCTION_1       1  ''
              958  LOAD_CONST               0
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE   974  'to 974'

 L.2318       966  LOAD_GLOBAL              YaccError
              968  LOAD_STR                 'no rules of the form p_rulename are defined.'
              970  CALL_FUNCTION_1       1  ''
              972  RAISE_VARARGS_1       1  ''
            974_0  COME_FROM           962  '962'

 L.2321       974  LOAD_FAST                'symbols'
              976  LOAD_ATTR                sort
              978  LOAD_LAMBDA              '<code_object <lambda>>'
              980  LOAD_STR                 'yacc.<locals>.<lambda>'
              982  MAKE_FUNCTION_0          ''
              984  LOAD_CONST               ('key',)
              986  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              988  POP_TOP          

 L.2324       990  SETUP_LOOP         1042  'to 1042'
              992  LOAD_FAST                'symbols'
              994  GET_ITER         
              996  FOR_ITER           1040  'to 1040'
              998  STORE_FAST               'f'

 L.2325      1000  LOAD_GLOBAL              add_function
             1002  LOAD_FAST                'f'
             1004  CALL_FUNCTION_1       1  ''
             1006  LOAD_CONST               0
             1008  COMPARE_OP               <
         1010_1012  POP_JUMP_IF_FALSE  1024  'to 1024'

 L.2326      1014  LOAD_FAST                'error'
             1016  LOAD_CONST               1
             1018  INPLACE_ADD      
             1020  STORE_FAST               'error'
             1022  JUMP_BACK           996  'to 996'
           1024_0  COME_FROM          1010  '1010'

 L.2328      1024  LOAD_CONST               None
             1026  LOAD_FAST                'files'
             1028  LOAD_FAST                'f'
             1030  LOAD_ATTR                __code__
             1032  LOAD_ATTR                co_filename
             1034  STORE_SUBSCR     
         1036_1038  JUMP_BACK           996  'to 996'
             1040  POP_BLOCK        
           1042_0  COME_FROM_LOOP      990  '990'

 L.2331      1042  SETUP_LOOP         1082  'to 1082'
             1044  LOAD_FAST                'symbols'
             1046  GET_ITER         
           1048_0  COME_FROM          1056  '1056'
             1048  FOR_ITER           1080  'to 1080'
             1050  STORE_FAST               'f'

 L.2332      1052  LOAD_FAST                'f'
             1054  LOAD_ATTR                __doc__
         1056_1058  POP_JUMP_IF_FALSE  1048  'to 1048'

 L.2333      1060  LOAD_GLOBAL              Signature
             1062  LOAD_METHOD              update
             1064  LOAD_FAST                'f'
             1066  LOAD_ATTR                __doc__
             1068  LOAD_METHOD              encode
             1070  CALL_METHOD_0         0  ''
             1072  CALL_METHOD_1         1  ''
             1074  POP_TOP          
         1076_1078  JUMP_BACK          1048  'to 1048'
             1080  POP_BLOCK        
           1082_0  COME_FROM_LOOP     1042  '1042'

 L.2335      1082  LOAD_GLOBAL              lr_init_vars
             1084  CALL_FUNCTION_0       0  ''
             1086  POP_TOP          

 L.2337      1088  LOAD_FAST                'error'
         1090_1092  POP_JUMP_IF_FALSE  1102  'to 1102'

 L.2338      1094  LOAD_GLOBAL              YaccError
             1096  LOAD_STR                 'Unable to construct parser.'
             1098  CALL_FUNCTION_1       1  ''
             1100  RAISE_VARARGS_1       1  ''
           1102_0  COME_FROM          1090  '1090'

 L.2340      1102  LOAD_GLOBAL              lr_read_tables
             1104  LOAD_FAST                'tabmodule'
             1106  CALL_FUNCTION_1       1  ''
         1108_1110  POP_JUMP_IF_TRUE   1432  'to 1432'

 L.2343      1112  SETUP_LOOP         1146  'to 1146'
             1114  LOAD_FAST                'files'
             1116  LOAD_METHOD              keys
             1118  CALL_METHOD_0         0  ''
             1120  GET_ITER         
           1122_0  COME_FROM          1132  '1132'
             1122  FOR_ITER           1144  'to 1144'
             1124  STORE_FAST               'filename'

 L.2344      1126  LOAD_GLOBAL              validate_file
             1128  LOAD_FAST                'filename'
             1130  CALL_FUNCTION_1       1  ''
         1132_1134  POP_JUMP_IF_TRUE   1122  'to 1122'

 L.2345      1136  LOAD_CONST               1
             1138  STORE_FAST               'error'
         1140_1142  JUMP_BACK          1122  'to 1122'
             1144  POP_BLOCK        
           1146_0  COME_FROM_LOOP     1112  '1112'

 L.2348      1146  LOAD_GLOBAL              validate_dict
             1148  LOAD_DEREF               'ldict'
             1150  CALL_FUNCTION_1       1  ''
             1152  POP_TOP          

 L.2350      1154  LOAD_FAST                'start'
         1156_1158  POP_JUMP_IF_FALSE  1182  'to 1182'
             1160  LOAD_FAST                'start'
             1162  LOAD_GLOBAL              Prodnames
             1164  COMPARE_OP               not-in
         1166_1168  POP_JUMP_IF_FALSE  1182  'to 1182'

 L.2351      1170  LOAD_GLOBAL              YaccError
             1172  LOAD_STR                 "Bad starting symbol '%s'"
             1174  LOAD_FAST                'start'
             1176  BINARY_MODULO    
             1178  CALL_FUNCTION_1       1  ''
             1180  RAISE_VARARGS_1       1  ''
           1182_0  COME_FROM          1166  '1166'
           1182_1  COME_FROM          1156  '1156'

 L.2353      1182  LOAD_GLOBAL              augment_grammar
             1184  LOAD_FAST                'start'
             1186  CALL_FUNCTION_1       1  ''
             1188  POP_TOP          

 L.2354      1190  LOAD_GLOBAL              verify_productions
             1192  LOAD_FAST                'check_recursion'
             1194  LOAD_CONST               ('cycle_check',)
             1196  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1198  STORE_FAST               'error'

 L.2356      1200  LOAD_CLOSURE             'ldict'
             1202  BUILD_TUPLE_1         1 
             1204  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1206  LOAD_STR                 'yacc.<locals>.<listcomp>'
             1208  MAKE_FUNCTION_8          'closure'

 L.2357      1210  LOAD_DEREF               'ldict'
             1212  LOAD_METHOD              keys
             1214  CALL_METHOD_0         0  ''
             1216  GET_ITER         
             1218  CALL_FUNCTION_1       1  ''
             1220  STORE_FAST               'otherfunc'

 L.2364      1222  LOAD_FAST                'error'
         1224_1226  POP_JUMP_IF_FALSE  1236  'to 1236'

 L.2365      1228  LOAD_GLOBAL              YaccError
             1230  LOAD_STR                 'Unable to construct parser.'
             1232  CALL_FUNCTION_1       1  ''
             1234  RAISE_VARARGS_1       1  ''
           1236_0  COME_FROM          1224  '1224'

 L.2367      1236  LOAD_GLOBAL              build_lritems
             1238  CALL_FUNCTION_0       0  ''
             1240  POP_TOP          

 L.2368      1242  LOAD_GLOBAL              compute_first1
             1244  CALL_FUNCTION_0       0  ''
             1246  POP_TOP          

 L.2369      1248  LOAD_GLOBAL              compute_follow
             1250  LOAD_FAST                'start'
             1252  CALL_FUNCTION_1       1  ''
             1254  POP_TOP          

 L.2371      1256  LOAD_FAST                'method'
             1258  LOAD_CONST               ('SLR', 'LALR')
             1260  COMPARE_OP               in
         1262_1264  POP_JUMP_IF_FALSE  1276  'to 1276'

 L.2372      1266  LOAD_GLOBAL              lr_parse_table
             1268  LOAD_FAST                'method'
             1270  CALL_FUNCTION_1       1  ''
             1272  POP_TOP          
             1274  JUMP_FORWARD       1288  'to 1288'
           1276_0  COME_FROM          1262  '1262'

 L.2374      1276  LOAD_GLOBAL              YaccError
             1278  LOAD_STR                 "Unknown parsing method '%s'"
             1280  LOAD_FAST                'method'
             1282  BINARY_MODULO    
             1284  CALL_FUNCTION_1       1  ''
             1286  RAISE_VARARGS_1       1  ''
           1288_0  COME_FROM          1274  '1274'

 L.2376      1288  LOAD_FAST                'write_tables'
         1290_1292  POP_JUMP_IF_FALSE  1304  'to 1304'

 L.2377      1294  LOAD_GLOBAL              lr_write_tables
             1296  LOAD_FAST                'tabmodule'
             1298  LOAD_FAST                'outputdir'
             1300  CALL_FUNCTION_2       2  ''
             1302  POP_TOP          
           1304_0  COME_FROM          1290  '1290'

 L.2379      1304  LOAD_GLOBAL              yaccdebug
         1306_1308  POP_JUMP_IF_FALSE  1432  'to 1432'

 L.2380      1310  SETUP_EXCEPT       1382  'to 1382'

 L.2381      1312  LOAD_GLOBAL              open
             1314  LOAD_GLOBAL              os
             1316  LOAD_ATTR                path
             1318  LOAD_METHOD              join
             1320  LOAD_FAST                'outputdir'
             1322  LOAD_FAST                'debugfile'
             1324  CALL_METHOD_2         2  ''
             1326  LOAD_STR                 'w'
             1328  CALL_FUNCTION_2       2  ''
             1330  STORE_FAST               'f'

 L.2382      1332  LOAD_FAST                'f'
             1334  LOAD_METHOD              write
             1336  LOAD_GLOBAL              _vfc
             1338  LOAD_METHOD              getvalue
             1340  CALL_METHOD_0         0  ''
             1342  CALL_METHOD_1         1  ''
             1344  POP_TOP          

 L.2383      1346  LOAD_FAST                'f'
             1348  LOAD_METHOD              write
             1350  LOAD_STR                 '\n\n'
             1352  CALL_METHOD_1         1  ''
             1354  POP_TOP          

 L.2384      1356  LOAD_FAST                'f'
             1358  LOAD_METHOD              write
             1360  LOAD_GLOBAL              _vf
             1362  LOAD_METHOD              getvalue
             1364  CALL_METHOD_0         0  ''
             1366  CALL_METHOD_1         1  ''
             1368  POP_TOP          

 L.2385      1370  LOAD_FAST                'f'
             1372  LOAD_METHOD              close
             1374  CALL_METHOD_0         0  ''
             1376  POP_TOP          
             1378  POP_BLOCK        
             1380  JUMP_FORWARD       1432  'to 1432'
           1382_0  COME_FROM_EXCEPT   1310  '1310'

 L.2386      1382  DUP_TOP          
             1384  LOAD_GLOBAL              IOError
             1386  COMPARE_OP               exception-match
         1388_1390  POP_JUMP_IF_FALSE  1430  'to 1430'
             1392  POP_TOP          
             1394  STORE_FAST               'e'
             1396  POP_TOP          
             1398  SETUP_FINALLY      1418  'to 1418'

 L.2387      1400  LOAD_GLOBAL              print
             1402  LOAD_STR                 "yacc: can't create '%s'"
             1404  LOAD_FAST                'debugfile'
             1406  BINARY_MODULO    
             1408  LOAD_FAST                'e'
             1410  CALL_FUNCTION_2       2  ''
             1412  POP_TOP          
             1414  POP_BLOCK        
             1416  LOAD_CONST               None
           1418_0  COME_FROM_FINALLY  1398  '1398'
             1418  LOAD_CONST               None
             1420  STORE_FAST               'e'
             1422  DELETE_FAST              'e'
             1424  END_FINALLY      
             1426  POP_EXCEPT       
             1428  JUMP_FORWARD       1432  'to 1432'
           1430_0  COME_FROM          1388  '1388'
             1430  END_FINALLY      
           1432_0  COME_FROM          1428  '1428'
           1432_1  COME_FROM          1380  '1380'
           1432_2  COME_FROM          1306  '1306'
           1432_3  COME_FROM          1108  '1108'
           1432_4  COME_FROM           368  '368'

 L.2392      1432  LOAD_GLOBAL              ParserPrototype
             1434  LOAD_STR                 'xyzzy'
             1436  CALL_FUNCTION_1       1  ''
             1438  STORE_FAST               'g'

 L.2393      1440  LOAD_GLOBAL              Productions
             1442  LOAD_FAST                'g'
             1444  STORE_ATTR               productions

 L.2394      1446  LOAD_GLOBAL              Errorfunc
             1448  LOAD_FAST                'g'
             1450  STORE_ATTR               errorfunc

 L.2395      1452  LOAD_GLOBAL              _lr_action
             1454  LOAD_FAST                'g'
             1456  STORE_ATTR               action

 L.2396      1458  LOAD_GLOBAL              _lr_goto
             1460  LOAD_FAST                'g'
             1462  STORE_ATTR               goto

 L.2397      1464  LOAD_GLOBAL              _lr_method
             1466  LOAD_FAST                'g'
             1468  STORE_ATTR               method

 L.2398      1470  LOAD_GLOBAL              Requires
             1472  LOAD_FAST                'g'
             1474  STORE_ATTR               require

 L.2401      1476  LOAD_FAST                'g'
             1478  LOAD_METHOD              init_parser
             1480  CALL_METHOD_0         0  ''
             1482  STORE_GLOBAL             parser

 L.2404      1484  LOAD_GLOBAL              parser
             1486  LOAD_ATTR                parse
             1488  STORE_GLOBAL             parse

 L.2407      1490  LOAD_FAST                'optimize'
         1492_1494  POP_JUMP_IF_TRUE   1502  'to 1502'

 L.2408      1496  LOAD_GLOBAL              yacc_cleanup
             1498  CALL_FUNCTION_0       0  ''
             1500  POP_TOP          
           1502_0  COME_FROM          1492  '1492'

 L.2409      1502  LOAD_FAST                'g'
             1504  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 132_0


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


# global parse ## Warning: Unused global