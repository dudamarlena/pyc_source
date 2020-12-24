# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lpabon/git/golang/porx/src/github.com/libopenstorage/openstorage-sdk-clients/sdk/python/build/lib/python3.6/site-packages/pycparser/ply/cpp.py
# Compiled at: 2018-07-25 08:51:15
# Size of source mod 2**32: 33282 bytes
import sys
if sys.version_info.major < 3:
    STRING_TYPES = (
     str, unicode)
else:
    STRING_TYPES = str
    xrange = range
tokens = ('CPP_ID', 'CPP_INTEGER', 'CPP_FLOAT', 'CPP_STRING', 'CPP_CHAR', 'CPP_WS',
          'CPP_COMMENT1', 'CPP_COMMENT2', 'CPP_POUND', 'CPP_DPOUND')
literals = '+-*/%|&~^<>=!?()[]{}.,;:\\\'"'

def t_CPP_WS(t):
    r"""\s+"""
    t.lexer.lineno += t.value.count('\n')
    return t


t_CPP_POUND = '\\#'
t_CPP_DPOUND = '\\#\\#'
t_CPP_ID = '[A-Za-z_][\\w_]*'

def CPP_INTEGER(t):
    r"""(((((0x)|(0X))[0-9a-fA-F]+)|(\d+))([uU][lL]|[lL][uU]|[uU]|[lL])?)"""
    return t


t_CPP_INTEGER = CPP_INTEGER
t_CPP_FLOAT = '((\\d+)(\\.\\d+)(e(\\+|-)?(\\d+))? | (\\d+)e(\\+|-)?(\\d+))([lL]|[fF])?'

def t_CPP_STRING(t):
    r"""\"([^\\\n]|(\\(.|\n)))*?\""""
    t.lexer.lineno += t.value.count('\n')
    return t


def t_CPP_CHAR(t):
    r"""(L)?\'([^\\\n]|(\\(.|\n)))*?\'"""
    t.lexer.lineno += t.value.count('\n')
    return t


def t_CPP_COMMENT1(t):
    r"""(/\*(.|\n)*?\*/)"""
    ncr = t.value.count('\n')
    t.lexer.lineno += ncr
    t.type = 'CPP_WS'
    t.value = '\n' * ncr if ncr else ' '
    return t


def t_CPP_COMMENT2(t):
    r"""(//.*?(\n|$))"""
    t.type = 'CPP_WS'
    t.value = '\n'
    return t


def t_error(t):
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t


import re, copy, time, os.path
_trigraph_pat = re.compile("\\?\\?[=/\\'\\(\\)\\!<>\\-]")
_trigraph_rep = {'=':'#', 
 '/':'\\', 
 "'":'^', 
 '(':'[', 
 ')':']', 
 '!':'|', 
 '<':'{', 
 '>':'}', 
 '-':'~'}

def trigraph(input):
    return _trigraph_pat.sub(lambda g: _trigraph_rep[g.group()[(-1)]], input)


class Macro(object):

    def __init__(self, name, value, arglist=None, variadic=False):
        self.name = name
        self.value = value
        self.arglist = arglist
        self.variadic = variadic
        if variadic:
            self.vararg = arglist[(-1)]
        self.source = None


class Preprocessor(object):

    def __init__(self, lexer=None):
        if lexer is None:
            lexer = lex.lexer
        self.lexer = lexer
        self.macros = {}
        self.path = []
        self.temp_path = []
        self.lexprobe()
        tm = time.localtime()
        self.define('__DATE__ "%s"' % time.strftime('%b %d %Y', tm))
        self.define('__TIME__ "%s"' % time.strftime('%H:%M:%S', tm))
        self.parser = None

    def tokenize(self, text):
        tokens = []
        self.lexer.input(text)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)

        return tokens

    def error(self, file, line, msg):
        print('%s:%d %s' % (file, line, msg))

    def lexprobe(self):
        self.lexer.input('identifier')
        tok = self.lexer.token()
        if not tok or tok.value != 'identifier':
            print("Couldn't determine identifier type")
        else:
            self.t_ID = tok.type
        self.lexer.input('12345')
        tok = self.lexer.token()
        if not tok or int(tok.value) != 12345:
            print("Couldn't determine integer type")
        else:
            self.t_INTEGER = tok.type
            self.t_INTEGER_TYPE = type(tok.value)
        self.lexer.input('"filename"')
        tok = self.lexer.token()
        if not tok or tok.value != '"filename"':
            print("Couldn't determine string type")
        else:
            self.t_STRING = tok.type
        self.lexer.input('  ')
        tok = self.lexer.token()
        if not tok or tok.value != '  ':
            self.t_SPACE = None
        else:
            self.t_SPACE = tok.type
        self.lexer.input('\n')
        tok = self.lexer.token()
        if not tok or tok.value != '\n':
            self.t_NEWLINE = None
            print("Couldn't determine token for newlines")
        else:
            self.t_NEWLINE = tok.type
        self.t_WS = (self.t_SPACE, self.t_NEWLINE)
        chars = [
         '<', '>', '#', '##', '\\', '(', ')', ',', '.']
        for c in chars:
            self.lexer.input(c)
            tok = self.lexer.token()
            if not tok or tok.value != c:
                print("Unable to lex '%s' required for preprocessor" % c)

    def add_path(self, path):
        self.path.append(path)

    def group_lines(self, input):
        lex = self.lexer.clone()
        lines = [x.rstrip() for x in input.splitlines()]
        for i in xrange(len(lines)):
            j = i + 1
            while lines[i].endswith('\\') and j < len(lines):
                lines[i] = lines[i][:-1] + lines[j]
                lines[j] = ''
                j += 1

        input = '\n'.join(lines)
        lex.input(input)
        lex.lineno = 1
        current_line = []
        while 1:
            tok = lex.token()
            if not tok:
                break
            current_line.append(tok)
            if tok.type in self.t_WS and '\n' in tok.value:
                yield current_line
                current_line = []

        if current_line:
            yield current_line

    def tokenstrip(self, tokens):
        i = 0
        while i < len(tokens) and tokens[i].type in self.t_WS:
            i += 1

        del tokens[:i]
        i = len(tokens) - 1
        while i >= 0 and tokens[i].type in self.t_WS:
            i -= 1

        del tokens[i + 1:]
        return tokens

    def collect_args(self, tokenlist):
        args = []
        positions = []
        current_arg = []
        nesting = 1
        tokenlen = len(tokenlist)
        i = 0
        while i < tokenlen and tokenlist[i].type in self.t_WS:
            i += 1

        if i < tokenlen:
            if tokenlist[i].value == '(':
                positions.append(i + 1)
        else:
            self.error(self.source, tokenlist[0].lineno, "Missing '(' in macro arguments")
            return (0, [], [])
        i += 1
        while i < tokenlen:
            t = tokenlist[i]
            if t.value == '(':
                current_arg.append(t)
                nesting += 1
            else:
                if t.value == ')':
                    nesting -= 1
                    if nesting == 0:
                        if current_arg:
                            args.append(self.tokenstrip(current_arg))
                            positions.append(i)
                        return (
                         i + 1, args, positions)
                    current_arg.append(t)
                elif t.value == ',':
                    if nesting == 1:
                        args.append(self.tokenstrip(current_arg))
                        positions.append(i + 1)
                        current_arg = []
                else:
                    current_arg.append(t)
            i += 1

        self.error(self.source, tokenlist[(-1)].lineno, "Missing ')' in macro arguments")
        return (0, [], [])

    def macro_prescan(self, macro):
        macro.patch = []
        macro.str_patch = []
        macro.var_comma_patch = []
        i = 0
        while i < len(macro.value):
            if macro.value[i].type == self.t_ID and macro.value[i].value in macro.arglist:
                argnum = macro.arglist.index(macro.value[i].value)
                if i > 0:
                    if macro.value[(i - 1)].value == '#':
                        macro.value[i] = copy.copy(macro.value[i])
                        macro.value[i].type = self.t_STRING
                        del macro.value[i - 1]
                        macro.str_patch.append((argnum, i - 1))
                        continue
                if i > 0 and macro.value[(i - 1)].value == '##':
                    macro.patch.append(('c', argnum, i - 1))
                    del macro.value[i - 1]
                    continue
                elif i + 1 < len(macro.value):
                    if macro.value[(i + 1)].value == '##':
                        macro.patch.append(('c', argnum, i))
                        i += 1
                        continue
                else:
                    macro.patch.append(('e', argnum, i))
            else:
                if macro.value[i].value == '##':
                    if macro.variadic:
                        if i > 0:
                            if macro.value[(i - 1)].value == ',':
                                if i + 1 < len(macro.value):
                                    if macro.value[(i + 1)].type == self.t_ID:
                                        if macro.value[(i + 1)].value == macro.vararg:
                                            macro.var_comma_patch.append(i - 1)
                i += 1

        macro.patch.sort(key=(lambda x: x[2]), reverse=True)

    def macro_expand_args(self, macro, args):
        rep = [copy.copy(_x) for _x in macro.value]
        str_expansion = {}
        for argnum, i in macro.str_patch:
            if argnum not in str_expansion:
                str_expansion[argnum] = ('"%s"' % ''.join([x.value for x in args[argnum]])).replace('\\', '\\\\')
            rep[i] = copy.copy(rep[i])
            rep[i].value = str_expansion[argnum]

        comma_patch = False
        if macro.variadic:
            if not args[(-1)]:
                for i in macro.var_comma_patch:
                    rep[i] = None
                    comma_patch = True

        expanded = {}
        for ptype, argnum, i in macro.patch:
            if ptype == 'c':
                rep[i:i + 1] = args[argnum]
            else:
                if ptype == 'e':
                    if argnum not in expanded:
                        expanded[argnum] = self.expand_macros(args[argnum])
                    rep[i:i + 1] = expanded[argnum]

        if comma_patch:
            rep = [_i for _i in rep if _i]
        return rep

    def expand_macros(self, tokens, expanded=None):
        if expanded is None:
            expanded = {}
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.type == self.t_ID:
                if t.value in self.macros and t.value not in expanded:
                    expanded[t.value] = True
                    m = self.macros[t.value]
                    if not m.arglist:
                        ex = self.expand_macros([copy.copy(_x) for _x in m.value], expanded)
                        for e in ex:
                            e.lineno = t.lineno

                        tokens[i:i + 1] = ex
                        i += len(ex)
                    else:
                        j = i + 1
                        while j < len(tokens) and tokens[j].type in self.t_WS:
                            j += 1

                    if tokens[j].value == '(':
                        tokcount, args, positions = self.collect_args(tokens[j:])
                        if not m.variadic:
                            if len(args) != len(m.arglist):
                                self.error(self.source, t.lineno, 'Macro %s requires %d arguments' % (t.value, len(m.arglist)))
                                i = j + tokcount
                        elif m.variadic:
                            if len(args) < len(m.arglist) - 1:
                                if len(m.arglist) > 2:
                                    self.error(self.source, t.lineno, 'Macro %s must have at least %d arguments' % (t.value, len(m.arglist) - 1))
                                else:
                                    self.error(self.source, t.lineno, 'Macro %s must have at least %d argument' % (t.value, len(m.arglist) - 1))
                                i = j + tokcount
                        else:
                            if m.variadic:
                                if len(args) == len(m.arglist) - 1:
                                    args.append([])
                                else:
                                    args[len(m.arglist) - 1] = tokens[j + positions[(len(m.arglist) - 1)]:j + tokcount - 1]
                                    del args[len(m.arglist):]
                            rep = self.macro_expand_args(m, args)
                            rep = self.expand_macros(rep, expanded)
                            for r in rep:
                                r.lineno = t.lineno

                            tokens[i:j + tokcount] = rep
                            i += len(rep)
                    del expanded[t.value]
                    continue
                elif t.value == '__LINE__':
                    t.type = self.t_INTEGER
                    t.value = self.t_INTEGER_TYPE(t.lineno)
            i += 1

        return tokens

    def evalexpr(self, tokens):
        i = 0
        while i < len(tokens):
            if tokens[i].type == self.t_ID and tokens[i].value == 'defined':
                j = i + 1
                needparen = False
                result = '0L'
                while j < len(tokens):
                    if tokens[j].type in self.t_WS:
                        j += 1
                        continue
                    else:
                        if tokens[j].type == self.t_ID:
                            if tokens[j].value in self.macros:
                                result = '1L'
                            else:
                                result = '0L'
                            if not needparen:
                                break
                        else:
                            if tokens[j].value == '(':
                                needparen = True
                            else:
                                if tokens[j].value == ')':
                                    break
                                else:
                                    self.error(self.source, tokens[i].lineno, 'Malformed defined()')
                    j += 1

                tokens[i].type = self.t_INTEGER
                tokens[i].value = self.t_INTEGER_TYPE(result)
                del tokens[i + 1:j + 1]
            i += 1

        tokens = self.expand_macros(tokens)
        for i, t in enumerate(tokens):
            if t.type == self.t_ID:
                tokens[i] = copy.copy(t)
                tokens[i].type = self.t_INTEGER
                tokens[i].value = self.t_INTEGER_TYPE('0L')
            elif t.type == self.t_INTEGER:
                tokens[i] = copy.copy(t)
                tokens[i].value = str(tokens[i].value)
                while tokens[i].value[(-1)] not in '0123456789abcdefABCDEF':
                    tokens[i].value = tokens[i].value[:-1]

        expr = ''.join([str(x.value) for x in tokens])
        expr = expr.replace('&&', ' and ')
        expr = expr.replace('||', ' or ')
        expr = expr.replace('!', ' not ')
        try:
            result = eval(expr)
        except Exception:
            self.error(self.source, tokens[0].lineno, "Couldn't evaluate expression")
            result = 0

        return result

    def parsegen--- This code section failed: ---

 L. 614         0  LOAD_GLOBAL              trigraph
                2  LOAD_FAST                'input'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               't'

 L. 615         8  LOAD_FAST                'self'
               10  LOAD_ATTR                group_lines
               12  LOAD_FAST                't'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'lines'

 L. 617        18  LOAD_FAST                'source'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 618        22  LOAD_STR                 ''
               24  STORE_FAST               'source'
             26_0  COME_FROM            20  '20'

 L. 620        26  LOAD_FAST                'self'
               28  LOAD_ATTR                define
               30  LOAD_STR                 '__FILE__ "%s"'
               32  LOAD_FAST                'source'
               34  BINARY_MODULO    
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  POP_TOP          

 L. 622        40  LOAD_FAST                'source'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               source

 L. 623        46  BUILD_LIST_0          0 
               48  STORE_FAST               'chunk'

 L. 624        50  LOAD_CONST               True
               52  STORE_FAST               'enable'

 L. 625        54  LOAD_CONST               False
               56  STORE_FAST               'iftrigger'

 L. 626        58  BUILD_LIST_0          0 
               60  STORE_FAST               'ifstack'

 L. 628        62  SETUP_LOOP          912  'to 912'
               66  LOAD_FAST                'lines'
               68  GET_ITER         
               70  FOR_ITER            910  'to 910'
               74  STORE_FAST               'x'

 L. 629        76  SETUP_LOOP          112  'to 112'
               78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'x'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_ITER         
               86  FOR_ITER            110  'to 110'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'i'
               92  STORE_FAST               'tok'

 L. 630        94  LOAD_FAST                'tok'
               96  LOAD_ATTR                type
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                t_WS
              102  COMPARE_OP               not-in
              104  POP_JUMP_IF_FALSE    86  'to 86'

 L. 630       106  BREAK_LOOP       
            108_0  COME_FROM           104  '104'
              108  JUMP_BACK            86  'to 86'
              110  POP_BLOCK        
            112_0  COME_FROM_LOOP       76  '76'

 L. 631       112  LOAD_FAST                'tok'
              114  LOAD_ATTR                value
              116  LOAD_STR                 '#'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   894  'to 894'

 L. 635       124  SETUP_LOOP          170  'to 170'
              126  LOAD_FAST                'x'
              128  GET_ITER         
              130  FOR_ITER            168  'to 168'
              132  STORE_FAST               'tok'

 L. 636       134  LOAD_FAST                'tok'
              136  LOAD_ATTR                type
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                t_WS
              142  COMPARE_OP               in
              144  POP_JUMP_IF_FALSE   130  'to 130'
              146  LOAD_STR                 '\n'
              148  LOAD_FAST                'tok'
              150  LOAD_ATTR                value
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   130  'to 130'

 L. 637       156  LOAD_FAST                'chunk'
              158  LOAD_ATTR                append
              160  LOAD_FAST                'tok'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_TOP          
              166  JUMP_BACK           130  'to 130'
              168  POP_BLOCK        
            170_0  COME_FROM_LOOP      124  '124'

 L. 639       170  LOAD_FAST                'self'
              172  LOAD_ATTR                tokenstrip
              174  LOAD_FAST                'x'
              176  LOAD_FAST                'i'
              178  LOAD_CONST               1
              180  BINARY_ADD       
              182  LOAD_CONST               None
              184  BUILD_SLICE_2         2 
              186  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  STORE_FAST               'dirtokens'

 L. 640       192  LOAD_FAST                'dirtokens'
              194  POP_JUMP_IF_FALSE   226  'to 226'

 L. 641       196  LOAD_FAST                'dirtokens'
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    
              202  LOAD_ATTR                value
              204  STORE_FAST               'name'

 L. 642       206  LOAD_FAST                'self'
              208  LOAD_ATTR                tokenstrip
              210  LOAD_FAST                'dirtokens'
              212  LOAD_CONST               1
              214  LOAD_CONST               None
              216  BUILD_SLICE_2         2 
              218  BINARY_SUBSCR    
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  STORE_FAST               'args'
              224  JUMP_FORWARD        234  'to 234'
              226  ELSE                     '234'

 L. 644       226  LOAD_STR                 ''
              228  STORE_FAST               'name'

 L. 645       230  BUILD_LIST_0          0 
              232  STORE_FAST               'args'
            234_0  COME_FROM           224  '224'

 L. 647       234  LOAD_FAST                'name'
              236  LOAD_STR                 'define'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   296  'to 296'

 L. 648       244  LOAD_FAST                'enable'
              246  POP_JUMP_IF_FALSE   892  'to 892'

 L. 649       250  SETUP_LOOP          278  'to 278'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                expand_macros
              256  LOAD_FAST                'chunk'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  GET_ITER         
              262  FOR_ITER            276  'to 276'
              264  STORE_FAST               'tok'

 L. 650       266  LOAD_FAST                'tok'
              268  YIELD_VALUE      
              270  POP_TOP          
              272  JUMP_BACK           262  'to 262'
              276  POP_BLOCK        
            278_0  COME_FROM_LOOP      250  '250'

 L. 651       278  BUILD_LIST_0          0 
              280  STORE_FAST               'chunk'

 L. 652       282  LOAD_FAST                'self'
              284  LOAD_ATTR                define
              286  LOAD_FAST                'args'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  POP_TOP          
              292  JUMP_ABSOLUTE       908  'to 908'
              296  ELSE                     '892'

 L. 653       296  LOAD_FAST                'name'
              298  LOAD_STR                 'include'
              300  COMPARE_OP               ==
              302  POP_JUMP_IF_FALSE   402  'to 402'

 L. 654       306  LOAD_FAST                'enable'
              308  POP_JUMP_IF_FALSE   892  'to 892'

 L. 655       312  SETUP_LOOP          340  'to 340'
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                expand_macros
              318  LOAD_FAST                'chunk'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  GET_ITER         
              324  FOR_ITER            338  'to 338'
              326  STORE_FAST               'tok'

 L. 656       328  LOAD_FAST                'tok'
              330  YIELD_VALUE      
              332  POP_TOP          
              334  JUMP_BACK           324  'to 324'
              338  POP_BLOCK        
            340_0  COME_FROM_LOOP      312  '312'

 L. 657       340  BUILD_LIST_0          0 
              342  STORE_FAST               'chunk'

 L. 658       344  LOAD_FAST                'self'
              346  LOAD_ATTR                macros
              348  LOAD_STR                 '__FILE__'
              350  BINARY_SUBSCR    
              352  STORE_FAST               'oldfile'

 L. 659       354  SETUP_LOOP          382  'to 382'
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                include
              360  LOAD_FAST                'args'
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  GET_ITER         
              366  FOR_ITER            380  'to 380'
              368  STORE_FAST               'tok'

 L. 660       370  LOAD_FAST                'tok'
              372  YIELD_VALUE      
              374  POP_TOP          
              376  JUMP_BACK           366  'to 366'
              380  POP_BLOCK        
            382_0  COME_FROM_LOOP      354  '354'

 L. 661       382  LOAD_FAST                'oldfile'
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                macros
              388  LOAD_STR                 '__FILE__'
              390  STORE_SUBSCR     

 L. 662       392  LOAD_FAST                'source'
              394  LOAD_FAST                'self'
              396  STORE_ATTR               source
              398  JUMP_ABSOLUTE       908  'to 908'
              402  ELSE                     '892'

 L. 663       402  LOAD_FAST                'name'
              404  LOAD_STR                 'undef'
              406  COMPARE_OP               ==
              408  POP_JUMP_IF_FALSE   464  'to 464'

 L. 664       412  LOAD_FAST                'enable'
              414  POP_JUMP_IF_FALSE   892  'to 892'

 L. 665       418  SETUP_LOOP          446  'to 446'
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                expand_macros
              424  LOAD_FAST                'chunk'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  GET_ITER         
              430  FOR_ITER            444  'to 444'
              432  STORE_FAST               'tok'

 L. 666       434  LOAD_FAST                'tok'
              436  YIELD_VALUE      
              438  POP_TOP          
              440  JUMP_BACK           430  'to 430'
              444  POP_BLOCK        
            446_0  COME_FROM_LOOP      418  '418'

 L. 667       446  BUILD_LIST_0          0 
              448  STORE_FAST               'chunk'

 L. 668       450  LOAD_FAST                'self'
              452  LOAD_ATTR                undef
              454  LOAD_FAST                'args'
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  POP_TOP          
              460  JUMP_ABSOLUTE       908  'to 908'
              464  ELSE                     '892'

 L. 669       464  LOAD_FAST                'name'
              466  LOAD_STR                 'ifdef'
              468  COMPARE_OP               ==
              470  POP_JUMP_IF_FALSE   530  'to 530'

 L. 670       474  LOAD_FAST                'ifstack'
              476  LOAD_ATTR                append
              478  LOAD_FAST                'enable'
              480  LOAD_FAST                'iftrigger'
              482  BUILD_TUPLE_2         2 
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  POP_TOP          

 L. 671       488  LOAD_FAST                'enable'
              490  POP_JUMP_IF_FALSE   892  'to 892'

 L. 672       494  LOAD_FAST                'args'
              496  LOAD_CONST               0
              498  BINARY_SUBSCR    
              500  LOAD_ATTR                value
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                macros
              506  COMPARE_OP               not-in
              508  POP_JUMP_IF_FALSE   522  'to 522'

 L. 673       512  LOAD_CONST               False
              514  STORE_FAST               'enable'

 L. 674       516  LOAD_CONST               False
              518  STORE_FAST               'iftrigger'
              520  JUMP_FORWARD        526  'to 526'
              522  ELSE                     '526'

 L. 676       522  LOAD_CONST               True
              524  STORE_FAST               'iftrigger'
            526_0  COME_FROM           520  '520'
              526  JUMP_ABSOLUTE       908  'to 908'
              530  ELSE                     '892'

 L. 677       530  LOAD_FAST                'name'
              532  LOAD_STR                 'ifndef'
              534  COMPARE_OP               ==
              536  POP_JUMP_IF_FALSE   596  'to 596'

 L. 678       540  LOAD_FAST                'ifstack'
              542  LOAD_ATTR                append
              544  LOAD_FAST                'enable'
              546  LOAD_FAST                'iftrigger'
              548  BUILD_TUPLE_2         2 
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  POP_TOP          

 L. 679       554  LOAD_FAST                'enable'
              556  POP_JUMP_IF_FALSE   892  'to 892'

 L. 680       560  LOAD_FAST                'args'
              562  LOAD_CONST               0
              564  BINARY_SUBSCR    
              566  LOAD_ATTR                value
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                macros
              572  COMPARE_OP               in
              574  POP_JUMP_IF_FALSE   588  'to 588'

 L. 681       578  LOAD_CONST               False
              580  STORE_FAST               'enable'

 L. 682       582  LOAD_CONST               False
              584  STORE_FAST               'iftrigger'
              586  JUMP_FORWARD        592  'to 592'
              588  ELSE                     '592'

 L. 684       588  LOAD_CONST               True
              590  STORE_FAST               'iftrigger'
            592_0  COME_FROM           586  '586'
              592  JUMP_ABSOLUTE       908  'to 908'
              596  ELSE                     '892'

 L. 685       596  LOAD_FAST                'name'
              598  LOAD_STR                 'if'
              600  COMPARE_OP               ==
              602  POP_JUMP_IF_FALSE   658  'to 658'

 L. 686       606  LOAD_FAST                'ifstack'
              608  LOAD_ATTR                append
              610  LOAD_FAST                'enable'
              612  LOAD_FAST                'iftrigger'
              614  BUILD_TUPLE_2         2 
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  POP_TOP          

 L. 687       620  LOAD_FAST                'enable'
              622  POP_JUMP_IF_FALSE   892  'to 892'

 L. 688       626  LOAD_FAST                'self'
              628  LOAD_ATTR                evalexpr
              630  LOAD_FAST                'args'
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  STORE_FAST               'result'

 L. 689       636  LOAD_FAST                'result'
              638  POP_JUMP_IF_TRUE    652  'to 652'

 L. 690       642  LOAD_CONST               False
              644  STORE_FAST               'enable'

 L. 691       646  LOAD_CONST               False
              648  STORE_FAST               'iftrigger'
              650  JUMP_FORWARD        656  'to 656'
              652  ELSE                     '656'

 L. 693       652  LOAD_CONST               True
              654  STORE_FAST               'iftrigger'
            656_0  COME_FROM           650  '650'
              656  JUMP_FORWARD        892  'to 892'
              658  ELSE                     '892'

 L. 694       658  LOAD_FAST                'name'
              660  LOAD_STR                 'elif'
              662  COMPARE_OP               ==
              664  POP_JUMP_IF_FALSE   756  'to 756'

 L. 695       668  LOAD_FAST                'ifstack'
              670  POP_JUMP_IF_FALSE   732  'to 732'

 L. 696       674  LOAD_FAST                'ifstack'
              676  LOAD_CONST               -1
              678  BINARY_SUBSCR    
              680  LOAD_CONST               0
              682  BINARY_SUBSCR    
              684  POP_JUMP_IF_FALSE   754  'to 754'

 L. 697       688  LOAD_FAST                'enable'
              690  POP_JUMP_IF_FALSE   700  'to 700'

 L. 698       694  LOAD_CONST               False
              696  STORE_FAST               'enable'
              698  JUMP_FORWARD        730  'to 730'
              700  ELSE                     '730'

 L. 699       700  LOAD_FAST                'iftrigger'
              702  POP_JUMP_IF_TRUE    754  'to 754'

 L. 700       706  LOAD_FAST                'self'
              708  LOAD_ATTR                evalexpr
              710  LOAD_FAST                'args'
              712  CALL_FUNCTION_1       1  '1 positional argument'
              714  STORE_FAST               'result'

 L. 701       716  LOAD_FAST                'result'
              718  POP_JUMP_IF_FALSE   754  'to 754'

 L. 702       722  LOAD_CONST               True
              724  STORE_FAST               'enable'

 L. 703       726  LOAD_CONST               True
              728  STORE_FAST               'iftrigger'
            730_0  COME_FROM           698  '698'
              730  JUMP_FORWARD        754  'to 754'
              732  ELSE                     '754'

 L. 705       732  LOAD_FAST                'self'
              734  LOAD_ATTR                error
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                source
              740  LOAD_FAST                'dirtokens'
              742  LOAD_CONST               0
              744  BINARY_SUBSCR    
              746  LOAD_ATTR                lineno
              748  LOAD_STR                 'Misplaced #elif'
              750  CALL_FUNCTION_3       3  '3 positional arguments'
              752  POP_TOP          
            754_0  COME_FROM           730  '730'
            754_1  COME_FROM           718  '718'
            754_2  COME_FROM           702  '702'
            754_3  COME_FROM           684  '684'
              754  JUMP_FORWARD        892  'to 892'
              756  ELSE                     '892'

 L. 707       756  LOAD_FAST                'name'
              758  LOAD_STR                 'else'
              760  COMPARE_OP               ==
              762  POP_JUMP_IF_FALSE   838  'to 838'

 L. 708       766  LOAD_FAST                'ifstack'
              768  POP_JUMP_IF_FALSE   814  'to 814'

 L. 709       772  LOAD_FAST                'ifstack'
              774  LOAD_CONST               -1
              776  BINARY_SUBSCR    
              778  LOAD_CONST               0
              780  BINARY_SUBSCR    
              782  POP_JUMP_IF_FALSE   836  'to 836'

 L. 710       786  LOAD_FAST                'enable'
              788  POP_JUMP_IF_FALSE   798  'to 798'

 L. 711       792  LOAD_CONST               False
              794  STORE_FAST               'enable'
              796  JUMP_FORWARD        812  'to 812'
              798  ELSE                     '812'

 L. 712       798  LOAD_FAST                'iftrigger'
              800  POP_JUMP_IF_TRUE    836  'to 836'

 L. 713       804  LOAD_CONST               True
              806  STORE_FAST               'enable'

 L. 714       808  LOAD_CONST               True
              810  STORE_FAST               'iftrigger'
            812_0  COME_FROM           796  '796'
              812  JUMP_FORWARD        836  'to 836'
              814  ELSE                     '836'

 L. 716       814  LOAD_FAST                'self'
              816  LOAD_ATTR                error
              818  LOAD_FAST                'self'
              820  LOAD_ATTR                source
              822  LOAD_FAST                'dirtokens'
              824  LOAD_CONST               0
              826  BINARY_SUBSCR    
              828  LOAD_ATTR                lineno
              830  LOAD_STR                 'Misplaced #else'
              832  CALL_FUNCTION_3       3  '3 positional arguments'
              834  POP_TOP          
            836_0  COME_FROM           812  '812'
            836_1  COME_FROM           800  '800'
            836_2  COME_FROM           782  '782'
              836  JUMP_FORWARD        892  'to 892'
              838  ELSE                     '892'

 L. 718       838  LOAD_FAST                'name'
              840  LOAD_STR                 'endif'
              842  COMPARE_OP               ==
              844  POP_JUMP_IF_FALSE   908  'to 908'

 L. 719       848  LOAD_FAST                'ifstack'
              850  POP_JUMP_IF_FALSE   868  'to 868'

 L. 720       854  LOAD_FAST                'ifstack'
              856  LOAD_ATTR                pop
              858  CALL_FUNCTION_0       0  '0 positional arguments'
              860  UNPACK_SEQUENCE_2     2 
              862  STORE_FAST               'enable'
              864  STORE_FAST               'iftrigger'
              866  JUMP_FORWARD        890  'to 890'
              868  ELSE                     '890'

 L. 722       868  LOAD_FAST                'self'
              870  LOAD_ATTR                error
              872  LOAD_FAST                'self'
              874  LOAD_ATTR                source
              876  LOAD_FAST                'dirtokens'
              878  LOAD_CONST               0
              880  BINARY_SUBSCR    
              882  LOAD_ATTR                lineno
              884  LOAD_STR                 'Misplaced #endif'
              886  CALL_FUNCTION_3       3  '3 positional arguments'
              888  POP_TOP          
            890_0  COME_FROM           866  '866'
              890  JUMP_FORWARD        892  'to 892'
            892_0  COME_FROM           890  '890'
            892_1  COME_FROM           836  '836'
            892_2  COME_FROM           754  '754'
            892_3  COME_FROM           656  '656'
            892_4  COME_FROM           622  '622'
            892_5  COME_FROM           414  '414'
            892_6  COME_FROM           308  '308'
            892_7  COME_FROM           246  '246'

 L. 725       892  CONTINUE             70  'to 70'

 L. 729       894  LOAD_FAST                'enable'
              896  POP_JUMP_IF_FALSE    70  'to 70'

 L. 730       898  LOAD_FAST                'chunk'
              900  LOAD_ATTR                extend
              902  LOAD_FAST                'x'
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  POP_TOP          
              908  JUMP_BACK            70  'to 70'
              910  POP_BLOCK        
            912_0  COME_FROM_LOOP       62  '62'

 L. 732       912  SETUP_LOOP          940  'to 940'
              914  LOAD_FAST                'self'
              916  LOAD_ATTR                expand_macros
              918  LOAD_FAST                'chunk'
              920  CALL_FUNCTION_1       1  '1 positional argument'
              922  GET_ITER         
              924  FOR_ITER            938  'to 938'
              926  STORE_FAST               'tok'

 L. 733       928  LOAD_FAST                'tok'
              930  YIELD_VALUE      
              932  POP_TOP          
              934  JUMP_BACK           924  'to 924'
              938  POP_BLOCK        
            940_0  COME_FROM_LOOP      912  '912'

 L. 734       940  BUILD_LIST_0          0 
              942  STORE_FAST               'chunk'

Parse error at or near `POP_BLOCK' instruction at offset 910

    def include(self, tokens):
        if not tokens:
            return
        if tokens:
            if tokens[0].value != '<':
                if tokens[0].type != self.t_STRING:
                    tokens = self.expand_macros(tokens)
            else:
                if tokens[0].value == '<':
                    i = 1
                    while i < len(tokens):
                        if tokens[i].value == '>':
                            break
                        i += 1
                    else:
                        print('Malformed #include <...>')
                        return

                    filename = ''.join([x.value for x in tokens[1:i]])
                    path = self.path + [''] + self.temp_path
                else:
                    if tokens[0].type == self.t_STRING:
                        filename = tokens[0].value[1:-1]
                        path = self.temp_path + [''] + self.path
                    else:
                        print('Malformed #include statement')
                        return
        for p in path:
            iname = os.path.join(p, filename)
            try:
                data = open(iname, 'r').read()
                dname = os.path.dirname(iname)
                if dname:
                    self.temp_path.insert(0, dname)
                for tok in self.parsegen(data, filename):
                    yield tok

                if dname:
                    del self.temp_path[0]
                break
            except IOError:
                pass

        else:
            print("Couldn't find '%s'" % filename)

    def define(self, tokens):
        if isinstance(tokens, STRING_TYPES):
            tokens = self.tokenize(tokens)
        linetok = tokens
        try:
            name = linetok[0]
            if len(linetok) > 1:
                mtype = linetok[1]
            else:
                mtype = None
            if not mtype:
                m = Macro(name.value, [])
                self.macros[name.value] = m
            else:
                if mtype.type in self.t_WS:
                    m = Macro(name.value, self.tokenstrip(linetok[2:]))
                    self.macros[name.value] = m
                else:
                    if mtype.value == '(':
                        tokcount, args, positions = self.collect_args(linetok[1:])
                        variadic = False
                        for a in args:
                            if variadic:
                                print('No more arguments may follow a variadic argument')
                                break
                            astr = ''.join([str(_i.value) for _i in a])
                            if astr == '...':
                                variadic = True
                                a[0].type = self.t_ID
                                a[0].value = '__VA_ARGS__'
                                variadic = True
                                del a[1:]
                                continue
                            else:
                                if astr[-3:] == '...':
                                    if a[0].type == self.t_ID:
                                        variadic = True
                                        del a[1:]
                                        if a[0].value[-3:] == '...':
                                            a[0].value = a[0].value[:-3]
                                            continue
                                if len(a) > 1 or a[0].type != self.t_ID:
                                    print('Invalid macro argument')
                                    break
                        else:
                            mvalue = self.tokenstrip(linetok[1 + tokcount:])
                            i = 0
                            while i < len(mvalue):
                                if i + 1 < len(mvalue):
                                    if mvalue[i].type in self.t_WS:
                                        if mvalue[(i + 1)].value == '##':
                                            del mvalue[i]
                                            continue
                                    if mvalue[i].value == '##':
                                        if mvalue[(i + 1)].type in self.t_WS:
                                            del mvalue[i + 1]
                                i += 1

                            m = Macro(name.value, mvalue, [x[0].value for x in args], variadic)
                            self.macro_prescan(m)
                            self.macros[name.value] = m

                    else:
                        print('Bad macro definition')
        except LookupError:
            print('Bad macro definition')

    def undef(self, tokens):
        id = tokens[0].value
        try:
            del self.macros[id]
        except LookupError:
            pass

    def parse(self, input, source=None, ignore={}):
        self.ignore = ignore
        self.parser = self.parsegen(input, source)

    def token(self):
        try:
            while 1:
                tok = next(self.parser)
                if tok.type not in self.ignore:
                    return tok

        except StopIteration:
            self.parser = None
            return


if __name__ == '__main__':
    import ply.lex as lex
    lexer = lex.lex()
    import sys
    f = open(sys.argv[1])
    input = f.read()
    p = Preprocessor(lexer)
    p.parse(input, sys.argv[1])
    while True:
        tok = p.token()
        if not tok:
            break
        print(p.source, tok)