# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/lex.py
# Compiled at: 2019-08-18 21:39:20
# Size of source mod 2**32: 34322 bytes
__version__ = '2.2'
import re, sys, types, os.path
_is_identifier = re.compile('^[a-zA-Z0-9_]+$')
_INSTANCETYPE = object

class LexError(Exception):

    def __init__(self, message, s):
        self.args = (
         message,)
        self.text = s


class LexToken(object):

    def __str__(self):
        return 'LexToken(%s,%r,%d,%d)' % (self.type, self.value, self.lineno, self.lexpos)

    def __repr__(self):
        return str(self)

    def skip(self, n):
        self.lexer.skip(n)


class Lexer:

    def __init__(self):
        self.lexre = None
        self.lexretext = None
        self.lexstatere = {}
        self.lexstateretext = {}
        self.lexstate = 'INITIAL'
        self.lexstatestack = []
        self.lexstateinfo = None
        self.lexstateignore = {}
        self.lexstateerrorf = {}
        self.lexreflags = 0
        self.lexdata = None
        self.lexpos = 0
        self.lexlen = 0
        self.lexerrorf = None
        self.lextokens = None
        self.lexignore = ''
        self.lexliterals = ''
        self.lexmodule = None
        self.lineno = 1
        self.lexdebug = 0
        self.lexoptimize = 0

    def clone(self, object=None):
        c = Lexer()
        c.lexstatere = self.lexstatere
        c.lexstateinfo = self.lexstateinfo
        c.lexstateretext = self.lexstateretext
        c.lexstate = self.lexstate
        c.lexstatestack = self.lexstatestack
        c.lexstateignore = self.lexstateignore
        c.lexstateerrorf = self.lexstateerrorf
        c.lexreflags = self.lexreflags
        c.lexdata = self.lexdata
        c.lexpos = self.lexpos
        c.lexlen = self.lexlen
        c.lextokens = self.lextokens
        c.lexdebug = self.lexdebug
        c.lineno = self.lineno
        c.lexoptimize = self.lexoptimize
        c.lexliterals = self.lexliterals
        c.lexmodule = self.lexmodule
        if object:
            newtab = {}
            for key, ritem in self.lexstatere.items():
                newre = []
                for cre, findex in ritem:
                    newfindex = []
                    for f in findex:
                        if not (f and f[0]):
                            newfindex.append(f)
                            continue
                        newfindex.append((getattr(object, f[0].__name__), f[1]))

                newre.append((cre, newfindex))
                newtab[key] = newre

            c.lexstatere = newtab
            c.lexstateerrorf = {}
            for key, ef in self.lexstateerrorf.items():
                c.lexstateerrorf[key] = getattr(object, ef.__name__)

            c.lexmodule = object
        c.begin(c.lexstate)
        return c

    def writetab(self, tabfile, outputdir=''):
        tf = open(os.path.join(outputdir, tabfile) + '.py', 'w')
        tf.write("# %s.py. This file automatically created by PLY (version %s). Don't edit!\n" % (
         tabfile, __version__))
        tf.write('_lextokens    = %s\n' % repr(self.lextokens))
        tf.write('_lexreflags   = %s\n' % repr(self.lexreflags))
        tf.write('_lexliterals  = %s\n' % repr(self.lexliterals))
        tf.write('_lexstateinfo = %s\n' % repr(self.lexstateinfo))
        tabre = {}
        for key, lre in self.lexstatere.items():
            titem = []
            for i in range(len(lre)):
                titem.append((self.lexstateretext[key][i], _funcs_to_names(lre[i][1])))

            tabre[key] = titem

        tf.write('_lexstatere   = %s\n' % repr(tabre))
        tf.write('_lexstateignore = %s\n' % repr(self.lexstateignore))
        taberr = {}
        for key, ef in self.lexstateerrorf.items():
            if ef:
                taberr[key] = ef.__name__
            else:
                taberr[key] = None

        tf.write('_lexstateerrorf = %s\n' % repr(taberr))
        tf.close()

    def readtab(self, tabfile, fdict):
        exec('import %s as lextab' % tabfile)
        self.lextokens = lextab._lextokens
        self.lexreflags = lextab._lexreflags
        self.lexliterals = lextab._lexliterals
        self.lexstateinfo = lextab._lexstateinfo
        self.lexstateignore = lextab._lexstateignore
        self.lexstatere = {}
        self.lexstateretext = {}
        for key, lre in lextab._lexstatere.items():
            titem = []
            txtitem = []
            for i in range(len(lre)):
                titem.append((
                 re.compile(lre[i][0], lextab._lexreflags), _names_to_funcs(lre[i][1], fdict)))
                txtitem.append(lre[i][0])

            self.lexstatere[key] = titem
            self.lexstateretext[key] = txtitem

        self.lexstateerrorf = {}
        for key, ef in lextab._lexstateerrorf.items():
            self.lexstateerrorf[key] = fdict[ef]

        self.begin('INITIAL')

    def input(self, s):
        if not isinstance(s, bytes):
            if not isinstance(s, str):
                raise ValueError('Expected a string')
        self.lexdata = s
        self.lexpos = 0
        self.lexlen = len(s)

    def begin(self, state):
        if state not in self.lexstatere:
            raise ValueError('Undefined state')
        self.lexre = self.lexstatere[state]
        self.lexretext = self.lexstateretext[state]
        self.lexignore = self.lexstateignore.get(state, '')
        self.lexerrorf = self.lexstateerrorf.get(state, None)
        self.lexstate = state

    def push_state(self, state):
        self.lexstatestack.append(self.lexstate)
        self.begin(state)

    def pop_state(self):
        self.begin(self.lexstatestack.pop())

    def current_state(self):
        return self.lexstate

    def skip(self, n):
        self.lexpos += n

    def token(self):
        lexpos = self.lexpos
        lexlen = self.lexlen
        lexignore = self.lexignore
        lexdata = self.lexdata
        while lexpos < lexlen:
            if lexdata[lexpos] in lexignore:
                lexpos += 1
                continue
            for lexre, lexindexfunc in self.lexre:
                m = lexre.match(lexdata, lexpos)
                if not m:
                    continue
                self.lexmatch = m
                tok = LexToken()
                tok.value = m.group()
                tok.groups = m.groups()
                tok.lineno = self.lineno
                tok.lexpos = lexpos
                tok.lexer = self
                lexpos = m.end()
                i = m.lastindex
                func, tok.type = lexindexfunc[i]
                self.lexpos = lexpos
                if not func:
                    if tok.type:
                        return tok
                    break
                if not hasattr(func, '__call__'):
                    break
                newtok = func(tok)
                if not newtok:
                    lexpos = self.lexpos
                    lexdata = self.lexdata
                    break
                if not self.lexoptimize:
                    if newtok.type not in self.lextokens:
                        if len(newtok.type) > 1:
                            raise LexError("%s:%d: Rule '%s' returned an unknown token type '%s'" % (
                             func.__code__.co_filename,
                             func.__code__.co_firstlineno,
                             func.__name__,
                             newtok.type), lexdata[lexpos:])
                return newtok
            else:
                if lexdata[lexpos] in self.lexliterals:
                    tok = LexToken()
                    tok.value = lexdata[lexpos]
                    tok.lineno = self.lineno
                    tok.lexer = self
                    tok.type = tok.value
                    tok.lexpos = lexpos
                    self.lexpos = lexpos + 1
                    return tok
                if self.lexerrorf:
                    tok = LexToken()
                    tok.value = self.lexdata[lexpos:]
                    tok.lineno = self.lineno
                    tok.type = 'error'
                    tok.lexer = self
                    tok.lexpos = lexpos
                    self.lexpos = lexpos
                    newtok = self.lexerrorf(tok)
                    if lexpos == self.lexpos:
                        raise LexError("Scanning error. Illegal character '%s'" % lexdata[lexpos], lexdata[lexpos:])
                    lexpos = self.lexpos
                    if not newtok:
                        continue
                    return newtok
                self.lexpos = lexpos
                raise LexError("Illegal character '%s' at index %d" % (lexdata[lexpos], lexpos), lexdata[lexpos:])

        self.lexpos = lexpos + 1
        if self.lexdata is None:
            raise RuntimeError('No input string given with input()')


def _validate_file(filename):
    import os.path
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
        fre = re.compile('\\s*def\\s+(t_[a-zA-Z_0-9]*)\\(')
        sre = re.compile('\\s*(t_[a-zA-Z_0-9]*)\\s*=')
        counthash = {}
        linen = 1
        noerror = 1
        for l in lines:
            m = fre.match(l)
            if not m:
                m = sre.match(l)
            elif m:
                name = m.group(1)
                prev = counthash.get(name)
                if not prev:
                    counthash[name] = linen
                else:
                    print('%s:%d: Rule %s redefined. Previously defined on line %d' % (
                     filename, linen, name, prev))
                noerror = 0
            linen += 1

        return noerror


def _funcs_to_names(funclist):
    result = []
    for f in funclist:
        if f and f[0]:
            result.append((f[0].__name__, f[1]))
        else:
            result.append(f)

    return result


def _names_to_funcs(namelist, fdict):
    result = []
    for n in namelist:
        if n and n[0]:
            result.append((fdict[n[0]], n[1]))
        else:
            result.append(n)

    return result


def _form_master_re(relist, reflags, ldict):
    if not relist:
        return []
    regex = '|'.join(relist)
    try:
        lexre = re.compile(regex, re.VERBOSE | reflags)
        lexindexfunc = [
         None] * (max(lexre.groupindex.values()) + 1)
        for f, i in lexre.groupindex.items():
            handle = ldict.get(f, None)
            if type(handle) in (types.FunctionType, types.MethodType):
                lexindexfunc[i] = (
                 handle, handle.__name__[2:])
            elif handle is not None:
                if f.find('ignore_') > 0:
                    lexindexfunc[i] = (None, None)
                    print('IGNORE', f)
                else:
                    lexindexfunc[i] = (
                     None, f[2:])

        return (
         [
          (
           lexre, lexindexfunc)], [regex])
    except Exception as e:
        try:
            m = int(len(relist) / 2)
            if m == 0:
                m = 1
            llist, lre = _form_master_re(relist[:m], reflags, ldict)
            rlist, rre = _form_master_re(relist[m:], reflags, ldict)
            return (
             llist + rlist, lre + rre)
        finally:
            e = None
            del e


def _statetoken(s, names):
    nonstate = 1
    parts = s.split('_')
    for i in range(1, len(parts)):
        if parts[i] not in names and parts[i] != 'ANY':
            break

    if i > 1:
        states = tuple(parts[1:i])
    else:
        states = ('INITIAL', )
    if 'ANY' in states:
        states = tuple(names.keys())
    tokenname = '_'.join(parts[i:])
    return (
     states, tokenname)


def lex(module=None, object=None, debug=0, optimize=0, lextab='lextab', reflags=0, nowarn=0, outputdir='', cls=Lexer):
    global input
    global lexer
    global token
    ldict = None
    stateinfo = {'INITIAL': 'inclusive'}
    error = 0
    files = {}
    lexobj = cls()
    lexobj.lexdebug = debug
    lexobj.lexoptimize = optimize
    if nowarn:
        warn = 0
    else:
        warn = 1
    if object:
        module = object
    elif module:
        if isinstance(module, types.ModuleType):
            ldict = module.__dict__
        elif isinstance(module, _INSTANCETYPE):
            _items = [(k, getattr(module, k)) for k in dir(module)]
            ldict = {}
            for i, v in _items:
                ldict[i] = v

        else:
            raise ValueError('Expected a module or instance')
        lexobj.lexmodule = module
    else:
        try:
            raise RuntimeError
        except RuntimeError:
            e, b, t = sys.exc_info()
            f = t.tb_frame
            f = f.f_back
            ldict = f.f_globals

    if optimize:
        if lextab:
            try:
                lexobj.readtab(lextab, ldict)
                token = lexobj.token
                input = lexobj.input
                lexer = lexobj
                return lexobj
            except ImportError:
                pass

    if module and isinstance(module, _INSTANCETYPE):
        tokens = getattr(module, 'tokens', None)
        states = getattr(module, 'states', None)
        literals = getattr(module, 'literals', '')
    else:
        tokens = ldict.get('tokens', None)
        states = ldict.get('states', None)
        literals = ldict.get('literals', '')
    if not tokens:
        raise SyntaxError("lex: module does not define 'tokens'")
    if not isinstance(tokens, list):
        if not isinstance(tokens, tuple):
            raise SyntaxError('lex: tokens must be a list or tuple.')
        lexobj.lextokens = {}
        if not optimize:
            for n in tokens:
                if not _is_identifier.match(n):
                    print("lex: Bad token name '%s'" % n)
                    error = 1
                if warn:
                    if n in lexobj.lextokens:
                        print("lex: Warning. Token '%s' multiply defined." % n)
                lexobj.lextokens[n] = None

    else:
        for n in tokens:
            lexobj.lextokens[n] = None

    if debug:
        print("lex: tokens = '%s'" % list(lexobj.lextokens.keys()))
    else:
        try:
            for c in literals:
                if isinstance(c, bytes) or isinstance(c, str):
                    if len(c) > 1:
                        pass
                    print('lex: Invalid literal %s. Must be a single character' % repr(c))
                    error = 1
                    continue

        except TypeError:
            print('lex: Invalid literals specification. literals must be a sequence of characters.')
            error = 1

        lexobj.lexliterals = literals
        if states and not isinstance(states, tuple):
            if not isinstance(states, list):
                print('lex: states must be defined as a tuple or list.')
                error = 1
            else:
                for s in states:
                    if not isinstance(s, tuple) or len(s) != 2:
                        print("lex: invalid state specifier %s. Must be a tuple (statename,'exclusive|inclusive')" % repr(s))
                        error = 1
                        continue
                    name, statetype = s
                    if not isinstance(name, str):
                        print('lex: state name %s must be a string' % repr(name))
                        error = 1
                        continue
                    if not statetype == 'inclusive':
                        if not statetype == 'exclusive':
                            print("lex: state type for state %s must be 'inclusive' or 'exclusive'" % name)
                            error = 1
                            continue
                        if name in stateinfo:
                            print("lex: state '%s' already defined." % name)
                            error = 1
                            continue
                        stateinfo[name] = statetype

    tsymbols = [f for f in ldict.keys() if f[:2] == 't_']
    funcsym = {}
    strsym = {}
    toknames = {}
    for s in stateinfo.keys():
        funcsym[s] = []
        strsym[s] = []

    ignore = {}
    errorf = {}
    if len(tsymbols) == 0:
        raise SyntaxError('lex: no rules of the form t_rulename are defined.')
    for f in tsymbols:
        t = ldict[f]
        states, tokname = _statetoken(f, stateinfo)
        toknames[f] = tokname
        if hasattr(t, '__call__'):
            for s in states:
                funcsym[s].append((f, t))

        elif isinstance(t, bytes) or isinstance(t, str):
            for s in states:
                strsym[s].append((f, t))

        else:
            print('lex: %s not defined as a function or string' % f)
        error = 1

    for f in funcsym.values():
        f.sort(key=(lambda x: x[1].__code__.co_firstlineno))

    for s in strsym.values():
        s.sort(key=(lambda x: len(x[1])))

    regexs = {}
    for state in stateinfo.keys():
        regex_list = []
        for fname, f in funcsym[state]:
            line = f.__code__.co_firstlineno
            file = f.__code__.co_filename
            files[file] = None
            tokname = toknames[fname]
            ismethod = isinstance(f, types.MethodType)
            if not optimize:
                nargs = f.__code__.co_argcount
                if ismethod:
                    reqargs = 2
                else:
                    reqargs = 1
                if nargs > reqargs:
                    print("%s:%d: Rule '%s' has too many arguments." % (file, line, f.__name__))
                    error = 1
                    continue
                if nargs < reqargs:
                    print("%s:%d: Rule '%s' requires an argument." % (file, line, f.__name__))
                    error = 1
                    continue
                if tokname == 'ignore':
                    print("%s:%d: Rule '%s' must be defined as a string." % (file, line, f.__name__))
                    error = 1
                    continue
                if tokname == 'error':
                    errorf[state] = f
                    continue
                if f.__doc__ and not optimize:
                    try:
                        c = re.compile('(?P<%s>%s)' % (f.__name__, f.__doc__), re.VERBOSE | reflags)
                        if c.match(''):
                            print("%s:%d: Regular expression for rule '%s' matches empty string." % (
                             file, line, f.__name__))
                            error = 1
                            continue
                    except re.error as e:
                        try:
                            print("%s:%d: Invalid regular expression for rule '%s'. %s" % (
                             file, line, f.__name__, e))
                            if '#' in f.__doc__:
                                print("%s:%d. Make sure '#' in rule '%s' is escaped with '\\#'." % (
                                 file, line, f.__name__))
                            error = 1
                            continue
                        finally:
                            e = None
                            del e

                    if debug:
                        print("lex: Adding rule %s -> '%s' (state '%s')" % (
                         f.__name__, f.__doc__, state))
                    regex_list.append('(?P<%s>%s)' % (f.__name__, f.__doc__))
                else:
                    print("%s:%d: No regular expression defined for rule '%s'" % (file, line, f.__name__))

        for name, r in strsym[state]:
            tokname = toknames[name]
            if tokname == 'ignore':
                ignore[state] = r
                continue
            if not optimize:
                if tokname == 'error':
                    raise SyntaxError("lex: Rule '%s' must be defined as a function" % name)
                    error = 1
                    continue
                else:
                    if tokname not in lexobj.lextokens:
                        if tokname.find('ignore_') < 0:
                            print("lex: Rule '%s' defined for an unspecified token %s." % (name, tokname))
                            error = 1
                            continue
                    try:
                        c = re.compile('(?P<%s>%s)' % (name, r), re.VERBOSE | reflags)
                        if c.match(''):
                            print("lex: Regular expression for rule '%s' matches empty string." % name)
                            error = 1
                            continue
                    except re.error as e:
                        try:
                            print("lex: Invalid regular expression for rule '%s'. %s" % (name, e))
                            if '#' in r:
                                print("lex: Make sure '#' in rule '%s' is escaped with '\\#'." % name)
                            error = 1
                            continue
                        finally:
                            e = None
                            del e

                if debug:
                    print("lex: Adding rule %s -> '%s' (state '%s')" % (name, r, state))
                regex_list.append('(?P<%s>%s)' % (name, r))

        if not regex_list:
            print("lex: No rules defined for state '%s'" % state)
            error = 1
        regexs[state] = regex_list

    if not optimize:
        for f in files.keys():
            if not _validate_file(f):
                error = 1

    if error:
        raise SyntaxError('lex: Unable to build lexer.')
    for state in regexs.keys():
        lexre, re_text = _form_master_re(regexs[state], reflags, ldict)
        lexobj.lexstatere[state] = lexre
        lexobj.lexstateretext[state] = re_text
        if debug:
            for i in range(len(re_text)):
                print("lex: state '%s'. regex[%d] = '%s'" % (state, i, re_text[i]))

    for state, type in stateinfo.items():
        if state != 'INITIAL' and type == 'inclusive':
            lexobj.lexstatere[state].extend(lexobj.lexstatere['INITIAL'])
            lexobj.lexstateretext[state].extend(lexobj.lexstateretext['INITIAL'])

    lexobj.lexstateinfo = stateinfo
    lexobj.lexre = lexobj.lexstatere['INITIAL']
    lexobj.lexretext = lexobj.lexstateretext['INITIAL']
    lexobj.lexstateignore = ignore
    lexobj.lexignore = lexobj.lexstateignore.get('INITIAL', '')
    lexobj.lexstateerrorf = errorf
    lexobj.lexerrorf = errorf.get('INITIAL', None)
    if warn:
        if not lexobj.lexerrorf:
            print('lex: Warning. no t_error rule is defined.')
    for s, stype in stateinfo.items():
        if stype == 'exclusive':
            if warn:
                if s not in errorf:
                    print("lex: Warning. no error rule is defined for exclusive state '%s'" % s)
                if warn and s not in ignore and lexobj.lexignore:
                    print("lex: Warning. no ignore rule is defined for exclusive state '%s'" % s)
            elif stype == 'inclusive':
                if s not in errorf:
                    errorf[s] = errorf.get('INITIAL', None)
                if s not in ignore:
                    ignore[s] = ignore.get('INITIAL', '')

    token = lexobj.token
    input = lexobj.input
    lexer = lexobj
    if lextab:
        if optimize:
            lexobj.writetab(lextab, outputdir)
    return lexobj


def runmain(lexer=None, data=None):
    if not data:
        try:
            filename = sys.argv[1]
            f = open(filename)
            data = f.read()
            f.close()
        except IndexError:
            print('Reading from standard input (type EOF to end):')
            data = sys.stdin.read()

    else:
        if lexer:
            _input = lexer.input
        else:
            _input = input
        _input(data)
        if lexer:
            _token = lexer.token
        else:
            _token = token
    while True:
        tok = _token()
        if not tok:
            break
        print('(%s,%r,%d,%d)' % (tok.type, tok.value, tok.lineno, tok.lexpos))


def TOKEN(r):

    def set_doc(f):
        f.__doc__ = r
        return f

    return set_doc


Token = TOKEN