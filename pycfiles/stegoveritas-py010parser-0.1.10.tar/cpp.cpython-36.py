# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../py010parser/ply/cpp.py
# Compiled at: 2019-04-24 09:45:01
# Size of source mod 2**32: 33066 bytes
from __future__ import generators
import six
tokens = ('CPP_ID', 'CPP_INTEGER', 'CPP_FLOAT', 'CPP_STRING', 'CPP_CHAR', 'CPP_WS',
          'CPP_COMMENT', 'CPP_POUND', 'CPP_DPOUND')
literals = '+-*/%|&~^<>=!?()[]{}.,;:\\\'"'

def t_CPP_WS(t):
    r"""\s+"""
    t.lexer.lineno += t.value.count('\n')
    return t


t_CPP_POUND = '\\#'
t_CPP_DPOUND = '\\#\\#'
t_CPP_ID = '[A-Za-z_][\\w_]*'

def CPP_INTEGER(t):
    r"""(((((0x)|(0X))[0-9a-fA-F]+)|(\d+))([uU]|[lL]|[uU][lL]|[lL][uU])?)"""
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


def t_CPP_COMMENT(t):
    r"""(/\*(.|\n)*?\*/)|(//.*?\n)"""
    t.lexer.lineno += t.value.count('\n')
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
        for i in six.moves.xrange(len(lines)):
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
        except StandardError:
            self.error(self.source, tokens[0].lineno, "Couldn't evaluate expression")
            result = 0

        return result

    def parsegen--- This code section failed: ---

 L. 598         0  LOAD_GLOBAL              trigraph
                2  LOAD_FAST                'input'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               't'

 L. 599         8  LOAD_FAST                'self'
               10  LOAD_ATTR                group_lines
               12  LOAD_FAST                't'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'lines'

 L. 601        18  LOAD_FAST                'source'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 602        22  LOAD_STR                 ''
               24  STORE_FAST               'source'
             26_0  COME_FROM            20  '20'

 L. 604        26  LOAD_FAST                'self'
               28  LOAD_ATTR                define
               30  LOAD_STR                 '__FILE__ "%s"'
               32  LOAD_FAST                'source'
               34  BINARY_MODULO    
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  POP_TOP          

 L. 606        40  LOAD_FAST                'source'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               source

 L. 607        46  BUILD_LIST_0          0 
               48  STORE_FAST               'chunk'

 L. 608        50  LOAD_CONST               True
               52  STORE_FAST               'enable'

 L. 609        54  LOAD_CONST               False
               56  STORE_FAST               'iftrigger'

 L. 610        58  BUILD_LIST_0          0 
               60  STORE_FAST               'ifstack'

 L. 612        62  SETUP_LOOP          910  'to 910'
               66  LOAD_FAST                'lines'
               68  GET_ITER         
               70  FOR_ITER            908  'to 908'
               74  STORE_FAST               'x'

 L. 613        76  SETUP_LOOP          112  'to 112'
               78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'x'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_ITER         
               86  FOR_ITER            110  'to 110'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'i'
               92  STORE_FAST               'tok'

 L. 614        94  LOAD_FAST                'tok'
               96  LOAD_ATTR                type
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                t_WS
              102  COMPARE_OP               not-in
              104  POP_JUMP_IF_FALSE    86  'to 86'

 L. 614       106  BREAK_LOOP       
            108_0  COME_FROM           104  '104'
              108  JUMP_BACK            86  'to 86'
              110  POP_BLOCK        
            112_0  COME_FROM_LOOP       76  '76'

 L. 615       112  LOAD_FAST                'tok'
              114  LOAD_ATTR                value
              116  LOAD_STR                 '#'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   892  'to 892'

 L. 618       124  SETUP_LOOP          168  'to 168'
              126  LOAD_FAST                'x'
              128  GET_ITER         
              130  FOR_ITER            166  'to 166'
              132  STORE_FAST               'tok'

 L. 619       134  LOAD_FAST                'tok'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                t_WS
              140  COMPARE_OP               in
              142  POP_JUMP_IF_FALSE   130  'to 130'
              144  LOAD_STR                 '\n'
              146  LOAD_FAST                'tok'
              148  LOAD_ATTR                value
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   130  'to 130'

 L. 620       154  LOAD_FAST                'chunk'
              156  LOAD_ATTR                append
              158  LOAD_FAST                'tok'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  POP_TOP          
              164  JUMP_BACK           130  'to 130'
              166  POP_BLOCK        
            168_0  COME_FROM_LOOP      124  '124'

 L. 622       168  LOAD_FAST                'self'
              170  LOAD_ATTR                tokenstrip
              172  LOAD_FAST                'x'
              174  LOAD_FAST                'i'
              176  LOAD_CONST               1
              178  BINARY_ADD       
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  BINARY_SUBSCR    
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  STORE_FAST               'dirtokens'

 L. 623       190  LOAD_FAST                'dirtokens'
              192  POP_JUMP_IF_FALSE   224  'to 224'

 L. 624       194  LOAD_FAST                'dirtokens'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  LOAD_ATTR                value
              202  STORE_FAST               'name'

 L. 625       204  LOAD_FAST                'self'
              206  LOAD_ATTR                tokenstrip
              208  LOAD_FAST                'dirtokens'
              210  LOAD_CONST               1
              212  LOAD_CONST               None
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_FAST               'args'
              222  JUMP_FORWARD        232  'to 232'
              224  ELSE                     '232'

 L. 627       224  LOAD_STR                 ''
              226  STORE_FAST               'name'

 L. 628       228  BUILD_LIST_0          0 
              230  STORE_FAST               'args'
            232_0  COME_FROM           222  '222'

 L. 630       232  LOAD_FAST                'name'
              234  LOAD_STR                 'define'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_FALSE   294  'to 294'

 L. 631       242  LOAD_FAST                'enable'
              244  POP_JUMP_IF_FALSE   890  'to 890'

 L. 632       248  SETUP_LOOP          276  'to 276'
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                expand_macros
              254  LOAD_FAST                'chunk'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  GET_ITER         
              260  FOR_ITER            274  'to 274'
              262  STORE_FAST               'tok'

 L. 633       264  LOAD_FAST                'tok'
              266  YIELD_VALUE      
              268  POP_TOP          
              270  JUMP_BACK           260  'to 260'
              274  POP_BLOCK        
            276_0  COME_FROM_LOOP      248  '248'

 L. 634       276  BUILD_LIST_0          0 
              278  STORE_FAST               'chunk'

 L. 635       280  LOAD_FAST                'self'
              282  LOAD_ATTR                define
              284  LOAD_FAST                'args'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  POP_TOP          
              290  JUMP_ABSOLUTE       906  'to 906'
              294  ELSE                     '890'

 L. 636       294  LOAD_FAST                'name'
              296  LOAD_STR                 'include'
              298  COMPARE_OP               ==
              300  POP_JUMP_IF_FALSE   400  'to 400'

 L. 637       304  LOAD_FAST                'enable'
              306  POP_JUMP_IF_FALSE   890  'to 890'

 L. 638       310  SETUP_LOOP          338  'to 338'
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                expand_macros
              316  LOAD_FAST                'chunk'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  GET_ITER         
              322  FOR_ITER            336  'to 336'
              324  STORE_FAST               'tok'

 L. 639       326  LOAD_FAST                'tok'
              328  YIELD_VALUE      
              330  POP_TOP          
              332  JUMP_BACK           322  'to 322'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      310  '310'

 L. 640       338  BUILD_LIST_0          0 
              340  STORE_FAST               'chunk'

 L. 641       342  LOAD_FAST                'self'
              344  LOAD_ATTR                macros
              346  LOAD_STR                 '__FILE__'
              348  BINARY_SUBSCR    
              350  STORE_FAST               'oldfile'

 L. 642       352  SETUP_LOOP          380  'to 380'
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                include
              358  LOAD_FAST                'args'
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  GET_ITER         
              364  FOR_ITER            378  'to 378'
              366  STORE_FAST               'tok'

 L. 643       368  LOAD_FAST                'tok'
              370  YIELD_VALUE      
              372  POP_TOP          
              374  JUMP_BACK           364  'to 364'
              378  POP_BLOCK        
            380_0  COME_FROM_LOOP      352  '352'

 L. 644       380  LOAD_FAST                'oldfile'
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                macros
              386  LOAD_STR                 '__FILE__'
              388  STORE_SUBSCR     

 L. 645       390  LOAD_FAST                'source'
              392  LOAD_FAST                'self'
              394  STORE_ATTR               source
              396  JUMP_ABSOLUTE       906  'to 906'
              400  ELSE                     '890'

 L. 646       400  LOAD_FAST                'name'
              402  LOAD_STR                 'undef'
              404  COMPARE_OP               ==
              406  POP_JUMP_IF_FALSE   462  'to 462'

 L. 647       410  LOAD_FAST                'enable'
              412  POP_JUMP_IF_FALSE   890  'to 890'

 L. 648       416  SETUP_LOOP          444  'to 444'
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                expand_macros
              422  LOAD_FAST                'chunk'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  GET_ITER         
              428  FOR_ITER            442  'to 442'
              430  STORE_FAST               'tok'

 L. 649       432  LOAD_FAST                'tok'
              434  YIELD_VALUE      
              436  POP_TOP          
              438  JUMP_BACK           428  'to 428'
              442  POP_BLOCK        
            444_0  COME_FROM_LOOP      416  '416'

 L. 650       444  BUILD_LIST_0          0 
              446  STORE_FAST               'chunk'

 L. 651       448  LOAD_FAST                'self'
              450  LOAD_ATTR                undef
              452  LOAD_FAST                'args'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  POP_TOP          
              458  JUMP_ABSOLUTE       906  'to 906'
              462  ELSE                     '890'

 L. 652       462  LOAD_FAST                'name'
              464  LOAD_STR                 'ifdef'
              466  COMPARE_OP               ==
              468  POP_JUMP_IF_FALSE   528  'to 528'

 L. 653       472  LOAD_FAST                'ifstack'
              474  LOAD_ATTR                append
              476  LOAD_FAST                'enable'
              478  LOAD_FAST                'iftrigger'
              480  BUILD_TUPLE_2         2 
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  POP_TOP          

 L. 654       486  LOAD_FAST                'enable'
              488  POP_JUMP_IF_FALSE   890  'to 890'

 L. 655       492  LOAD_FAST                'args'
              494  LOAD_CONST               0
              496  BINARY_SUBSCR    
              498  LOAD_ATTR                value
              500  LOAD_FAST                'self'
              502  LOAD_ATTR                macros
              504  COMPARE_OP               not-in
              506  POP_JUMP_IF_FALSE   520  'to 520'

 L. 656       510  LOAD_CONST               False
              512  STORE_FAST               'enable'

 L. 657       514  LOAD_CONST               False
              516  STORE_FAST               'iftrigger'
              518  JUMP_FORWARD        524  'to 524'
              520  ELSE                     '524'

 L. 659       520  LOAD_CONST               True
              522  STORE_FAST               'iftrigger'
            524_0  COME_FROM           518  '518'
              524  JUMP_ABSOLUTE       906  'to 906'
              528  ELSE                     '890'

 L. 660       528  LOAD_FAST                'name'
              530  LOAD_STR                 'ifndef'
              532  COMPARE_OP               ==
              534  POP_JUMP_IF_FALSE   594  'to 594'

 L. 661       538  LOAD_FAST                'ifstack'
              540  LOAD_ATTR                append
              542  LOAD_FAST                'enable'
              544  LOAD_FAST                'iftrigger'
              546  BUILD_TUPLE_2         2 
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  POP_TOP          

 L. 662       552  LOAD_FAST                'enable'
              554  POP_JUMP_IF_FALSE   890  'to 890'

 L. 663       558  LOAD_FAST                'args'
              560  LOAD_CONST               0
              562  BINARY_SUBSCR    
              564  LOAD_ATTR                value
              566  LOAD_FAST                'self'
              568  LOAD_ATTR                macros
              570  COMPARE_OP               in
              572  POP_JUMP_IF_FALSE   586  'to 586'

 L. 664       576  LOAD_CONST               False
              578  STORE_FAST               'enable'

 L. 665       580  LOAD_CONST               False
              582  STORE_FAST               'iftrigger'
              584  JUMP_FORWARD        590  'to 590'
              586  ELSE                     '590'

 L. 667       586  LOAD_CONST               True
              588  STORE_FAST               'iftrigger'
            590_0  COME_FROM           584  '584'
              590  JUMP_ABSOLUTE       906  'to 906'
              594  ELSE                     '890'

 L. 668       594  LOAD_FAST                'name'
              596  LOAD_STR                 'if'
              598  COMPARE_OP               ==
              600  POP_JUMP_IF_FALSE   656  'to 656'

 L. 669       604  LOAD_FAST                'ifstack'
              606  LOAD_ATTR                append
              608  LOAD_FAST                'enable'
              610  LOAD_FAST                'iftrigger'
              612  BUILD_TUPLE_2         2 
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  POP_TOP          

 L. 670       618  LOAD_FAST                'enable'
              620  POP_JUMP_IF_FALSE   890  'to 890'

 L. 671       624  LOAD_FAST                'self'
              626  LOAD_ATTR                evalexpr
              628  LOAD_FAST                'args'
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  STORE_FAST               'result'

 L. 672       634  LOAD_FAST                'result'
              636  POP_JUMP_IF_TRUE    650  'to 650'

 L. 673       640  LOAD_CONST               False
              642  STORE_FAST               'enable'

 L. 674       644  LOAD_CONST               False
              646  STORE_FAST               'iftrigger'
              648  JUMP_FORWARD        654  'to 654'
              650  ELSE                     '654'

 L. 676       650  LOAD_CONST               True
              652  STORE_FAST               'iftrigger'
            654_0  COME_FROM           648  '648'
              654  JUMP_FORWARD        890  'to 890'
              656  ELSE                     '890'

 L. 677       656  LOAD_FAST                'name'
              658  LOAD_STR                 'elif'
              660  COMPARE_OP               ==
              662  POP_JUMP_IF_FALSE   754  'to 754'

 L. 678       666  LOAD_FAST                'ifstack'
              668  POP_JUMP_IF_FALSE   730  'to 730'

 L. 679       672  LOAD_FAST                'ifstack'
              674  LOAD_CONST               -1
              676  BINARY_SUBSCR    
              678  LOAD_CONST               0
              680  BINARY_SUBSCR    
              682  POP_JUMP_IF_FALSE   752  'to 752'

 L. 680       686  LOAD_FAST                'enable'
              688  POP_JUMP_IF_FALSE   698  'to 698'

 L. 681       692  LOAD_CONST               False
              694  STORE_FAST               'enable'
              696  JUMP_FORWARD        728  'to 728'
              698  ELSE                     '728'

 L. 682       698  LOAD_FAST                'iftrigger'
              700  POP_JUMP_IF_TRUE    752  'to 752'

 L. 683       704  LOAD_FAST                'self'
              706  LOAD_ATTR                evalexpr
              708  LOAD_FAST                'args'
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  STORE_FAST               'result'

 L. 684       714  LOAD_FAST                'result'
              716  POP_JUMP_IF_FALSE   752  'to 752'

 L. 685       720  LOAD_CONST               True
              722  STORE_FAST               'enable'

 L. 686       724  LOAD_CONST               True
              726  STORE_FAST               'iftrigger'
            728_0  COME_FROM           696  '696'
              728  JUMP_FORWARD        752  'to 752'
              730  ELSE                     '752'

 L. 688       730  LOAD_FAST                'self'
              732  LOAD_ATTR                error
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                source
              738  LOAD_FAST                'dirtokens'
              740  LOAD_CONST               0
              742  BINARY_SUBSCR    
              744  LOAD_ATTR                lineno
              746  LOAD_STR                 'Misplaced #elif'
              748  CALL_FUNCTION_3       3  '3 positional arguments'
              750  POP_TOP          
            752_0  COME_FROM           728  '728'
            752_1  COME_FROM           716  '716'
            752_2  COME_FROM           700  '700'
            752_3  COME_FROM           682  '682'
              752  JUMP_FORWARD        890  'to 890'
              754  ELSE                     '890'

 L. 690       754  LOAD_FAST                'name'
              756  LOAD_STR                 'else'
              758  COMPARE_OP               ==
              760  POP_JUMP_IF_FALSE   836  'to 836'

 L. 691       764  LOAD_FAST                'ifstack'
              766  POP_JUMP_IF_FALSE   812  'to 812'

 L. 692       770  LOAD_FAST                'ifstack'
              772  LOAD_CONST               -1
              774  BINARY_SUBSCR    
              776  LOAD_CONST               0
              778  BINARY_SUBSCR    
              780  POP_JUMP_IF_FALSE   834  'to 834'

 L. 693       784  LOAD_FAST                'enable'
              786  POP_JUMP_IF_FALSE   796  'to 796'

 L. 694       790  LOAD_CONST               False
              792  STORE_FAST               'enable'
              794  JUMP_FORWARD        810  'to 810'
              796  ELSE                     '810'

 L. 695       796  LOAD_FAST                'iftrigger'
              798  POP_JUMP_IF_TRUE    834  'to 834'

 L. 696       802  LOAD_CONST               True
              804  STORE_FAST               'enable'

 L. 697       806  LOAD_CONST               True
              808  STORE_FAST               'iftrigger'
            810_0  COME_FROM           794  '794'
              810  JUMP_FORWARD        834  'to 834'
              812  ELSE                     '834'

 L. 699       812  LOAD_FAST                'self'
              814  LOAD_ATTR                error
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                source
              820  LOAD_FAST                'dirtokens'
              822  LOAD_CONST               0
              824  BINARY_SUBSCR    
              826  LOAD_ATTR                lineno
              828  LOAD_STR                 'Misplaced #else'
              830  CALL_FUNCTION_3       3  '3 positional arguments'
              832  POP_TOP          
            834_0  COME_FROM           810  '810'
            834_1  COME_FROM           798  '798'
            834_2  COME_FROM           780  '780'
              834  JUMP_FORWARD        890  'to 890'
              836  ELSE                     '890'

 L. 701       836  LOAD_FAST                'name'
              838  LOAD_STR                 'endif'
              840  COMPARE_OP               ==
              842  POP_JUMP_IF_FALSE   906  'to 906'

 L. 702       846  LOAD_FAST                'ifstack'
              848  POP_JUMP_IF_FALSE   866  'to 866'

 L. 703       852  LOAD_FAST                'ifstack'
              854  LOAD_ATTR                pop
              856  CALL_FUNCTION_0       0  '0 positional arguments'
              858  UNPACK_SEQUENCE_2     2 
              860  STORE_FAST               'enable'
              862  STORE_FAST               'iftrigger'
              864  JUMP_FORWARD        888  'to 888'
              866  ELSE                     '888'

 L. 705       866  LOAD_FAST                'self'
              868  LOAD_ATTR                error
              870  LOAD_FAST                'self'
              872  LOAD_ATTR                source
              874  LOAD_FAST                'dirtokens'
              876  LOAD_CONST               0
              878  BINARY_SUBSCR    
              880  LOAD_ATTR                lineno
              882  LOAD_STR                 'Misplaced #endif'
              884  CALL_FUNCTION_3       3  '3 positional arguments'
              886  POP_TOP          
            888_0  COME_FROM           864  '864'
              888  JUMP_FORWARD        890  'to 890'
            890_0  COME_FROM           888  '888'
            890_1  COME_FROM           834  '834'
            890_2  COME_FROM           752  '752'
            890_3  COME_FROM           654  '654'
            890_4  COME_FROM           620  '620'
            890_5  COME_FROM           412  '412'
            890_6  COME_FROM           306  '306'
            890_7  COME_FROM           244  '244'

 L. 708       890  CONTINUE             70  'to 70'

 L. 712       892  LOAD_FAST                'enable'
              894  POP_JUMP_IF_FALSE    70  'to 70'

 L. 713       896  LOAD_FAST                'chunk'
              898  LOAD_ATTR                extend
              900  LOAD_FAST                'x'
              902  CALL_FUNCTION_1       1  '1 positional argument'
              904  POP_TOP          
              906  JUMP_BACK            70  'to 70'
              908  POP_BLOCK        
            910_0  COME_FROM_LOOP       62  '62'

 L. 715       910  SETUP_LOOP          938  'to 938'
              912  LOAD_FAST                'self'
              914  LOAD_ATTR                expand_macros
              916  LOAD_FAST                'chunk'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  GET_ITER         
              922  FOR_ITER            936  'to 936'
              924  STORE_FAST               'tok'

 L. 716       926  LOAD_FAST                'tok'
              928  YIELD_VALUE      
              930  POP_TOP          
              932  JUMP_BACK           922  'to 922'
              936  POP_BLOCK        
            938_0  COME_FROM_LOOP      910  '910'

 L. 717       938  BUILD_LIST_0          0 
              940  STORE_FAST               'chunk'

Parse error at or near `POP_BLOCK' instruction at offset 908

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
        if isinstance(tokens, six.string_types):
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