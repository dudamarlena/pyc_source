# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/make_function3.py
# Compiled at: 2020-04-20 22:50:15
"""
All the crazy things we have to do to handle Python functions in 3.0-3.5 or so.
The saga of changes before and after is in other files.
"""
from xdis import iscode, code_has_star_arg, code_has_star_star_arg
from xdis.util import CO_GENERATOR
from uncompyle6.scanner import Code
from uncompyle6.parsers.treenode import SyntaxTree
from uncompyle6.semantics.parser_error import ParserError
from uncompyle6.semantics.helper import print_docstring, find_all_globals, find_globals_and_nonlocals, find_none
from uncompyle6.show import maybe_show_tree_param_default

def make_function3_annotate(self, node, is_lambda, nested=1, code_node=None, annotate_last=-1):
    """
    Dump function defintion, doc string, and function
    body. This code is specialized for Python 3"""

    def build_param(ast, name, default):
        """build parameters:
            - handle defaults
            - handle format tuple parameters
        """
        if default:
            value = self.traverse(default, indent='')
            maybe_show_tree_param_default(self, name, value)
            result = '%s=%s' % (name, value)
            if result[-2:] == '= ':
                result += 'None'
            return result
        else:
            return name

    assert node[(-1)].kind.startswith('MAKE_')
    annotate_tuple = None
    for annotate_last in range(len(node) - 1, -1, -1):
        if node[annotate_last] == 'annotate_tuple':
            annotate_tuple = node[annotate_last]
            break

    annotate_args = {}
    if annotate_tuple == 'annotate_tuple':
        if annotate_tuple[0] in ('LOAD_CONST', 'LOAD_NAME') and isinstance(annotate_tuple[0].attr, tuple):
            annotate_tup = annotate_tuple[0].attr
            i = -1
            j = annotate_last - 1
            l = -len(node)
            while j >= l and node[j].kind in ('annotate_arg', 'annotate_tuple'):
                annotate_args[annotate_tup[i]] = node[j][0]
                i -= 1
                j -= 1

        args_node = node[(-1)]
        if isinstance(args_node.attr, tuple):
            defparams = node[:args_node.attr[0]]
            (pos_args, kw_args, annotate_argc) = args_node.attr
            if 'return' in annotate_args.keys():
                annotate_argc = len(annotate_args) - 1
        else:
            defparams = node[:args_node.attr]
            kw_args = 0
            annotate_argc = 0
        annotate_dict = {}
        for name in annotate_args.keys():
            n = self.traverse(annotate_args[name], indent='')
            annotate_dict[name] = n

        if 3.0 <= self.version <= 3.2:
            lambda_index = -2
        elif 3.03 <= self.version:
            lambda_index = -3
        else:
            lambda_index = None
        assert lambda_index and is_lambda and iscode(node[lambda_index].attr) and node[lambda_index].kind == 'LOAD_LAMBDA'
        code = node[lambda_index].attr
    else:
        code = code_node.attr
    assert iscode(code)
    code = Code(code, self.scanner, self.currentclass)
    argc = code.co_argcount
    kwonlyargcount = code.co_kwonlyargcount
    paramnames = list(code.co_varnames[:argc])
    if kwonlyargcount > 0:
        kwargs = list(code.co_varnames[argc:argc + kwonlyargcount])
    try:
        ast = self.build_ast(code._tokens, code._customize, is_lambda=is_lambda, noneInNames='None' in code.co_names)
    except ParserError, p:
        self.write(str(p))
        if not self.tolerate_errors:
            self.ERROR = p
        return

    indent = self.indent
    if is_lambda:
        self.write('lambda ')
    else:
        self.write('(')
    last_line = self.f.getvalue().split('\n')[(-1)]
    l = len(last_line)
    indent = ' ' * l
    line_number = self.line_number
    i = len(paramnames) - len(defparams)
    suffix = ''
    for param in paramnames[:i]:
        self.write(suffix, param)
        suffix = ', '
        if param in annotate_dict:
            self.write(': %s' % annotate_dict[param])
            if line_number != self.line_number:
                suffix = ',\n' + indent
                line_number = self.line_number

    if i > 0:
        suffix = ', '
    else:
        suffix = ''
    for n in node:
        if n == 'pos_arg':
            self.write(suffix)
            param = paramnames[i]
            self.write(param)
            if param in annotate_args:
                aa = annotate_args[param]
                if isinstance(aa, tuple):
                    aa = aa[0]
                    self.write(': "%s"' % aa)
                elif isinstance(aa, SyntaxTree):
                    self.write(': ')
                    self.preorder(aa)
            self.write('=')
            i += 1
            self.preorder(n)
            if line_number != self.line_number:
                suffix = ',\n' + indent
                line_number = self.line_number
            else:
                suffix = ', '

    if code_has_star_arg(code):
        star_arg = code.co_varnames[(argc + kwonlyargcount)]
        if annotate_dict:
            if star_arg in annotate_dict:
                self.write(suffix, '*%s: %s' % (star_arg, annotate_dict[star_arg]))
            else:
                self.write(suffix, '*%s' % star_arg)
            argc += 1
        ends_in_comma = False
        if kwonlyargcount > 0:
            if code_has_star_arg(code) or argc > 0:
                self.write(', *, ')
            else:
                self.write('*, ')
            ends_in_comma = True
        elif argc > 0:
            self.write(', ')
            ends_in_comma = True
        kw_args = [None] * kwonlyargcount
        for n in node:
            if n == 'kwargs':
                n = n[0]
            if n == 'kwarg':
                name = eval(n[0].pattr)
                idx = kwargs.index(name)
                default = self.traverse(n[1], indent='')
                if annotate_dict and name in annotate_dict:
                    kw_args[idx] = '%s: %s=%s' % (name, annotate_dict[name], default)
                else:
                    kw_args[idx] = '%s=%s' % (name, default)

        other_kw = [ c == None for c in kw_args ]
        for (i, flag) in enumerate(other_kw):
            if flag:
                n = kwargs[i]
                if n in annotate_dict:
                    kw_args[i] = '%s: %s' % (n, annotate_dict[n])
                else:
                    kw_args[i] = '%s' % n

        self.write((', ').join(kw_args))
        ends_in_comma = False
    elif argc == 0:
        ends_in_comma = True
    if code_has_star_star_arg(code):
        if not ends_in_comma:
            self.write(', ')
        star_star_arg = code.co_varnames[(argc + kwonlyargcount)]
        if annotate_dict and star_star_arg in annotate_dict:
            self.write('**%s: %s' % (star_star_arg, annotate_dict[star_star_arg]))
        else:
            self.write('**%s' % star_star_arg)
    if is_lambda:
        self.write(': ')
    else:
        self.write(')')
        if 'return' in annotate_tuple[0].attr:
            if line_number != self.line_number and not no_paramnames:
                self.write('\n' + indent)
                line_number = self.line_number
            self.write(' -> ')
            if 'return' in annotate_dict:
                self.write(annotate_dict['return'])
            else:
                self.preorder(node[(annotate_last - 1)])
        self.println(':')
    if len(code.co_consts) > 0 and code.co_consts[0] is not None and not is_lambda:
        print_docstring(self, self.indent, code.co_consts[0])
    code._tokens = None
    assert ast == 'stmts'
    all_globals = find_all_globals(ast, set())
    (globals, nonlocals) = find_globals_and_nonlocals(ast, set(), set(), code, self.version)
    for g in sorted(all_globals & self.mod_globs | globals):
        self.println(self.indent, 'global ', g)

    for nl in sorted(nonlocals):
        self.println(self.indent, 'nonlocal ', nl)

    self.mod_globs -= all_globals
    has_none = 'None' in code.co_names
    rn = has_none and not find_none(ast)
    self.gen_source(ast, code.co_name, code._customize, is_lambda=is_lambda, returnNone=rn)
    code._tokens = code._customize = None
    return


def make_function3--- This code section failed: ---

 L. 339         0  LOAD_CONST               None
                3  LOAD_CLOSURE          0  'self'
                6  LOAD_CODE                <code_object build_param>
                9  MAKE_CLOSURE_1        1  None
               12  STORE_FAST           11  'build_param'

 L. 360        15  LOAD_FAST             1  'node'
               18  LOAD_CONST               -1
               21  BINARY_SUBSCR    
               22  LOAD_ATTR             3  'kind'
               25  LOAD_ATTR             4  'startswith'
               28  LOAD_CONST               'MAKE_'
               31  CALL_FUNCTION_1       1  None
               34  JUMP_IF_TRUE          7  'to 44'
               37  POP_TOP          
               38  LOAD_ASSERT              AssertionError
               41  RAISE_VARARGS_1       1  None
             44_0  COME_FROM            34  '34'
               44  POP_TOP          

 L. 364        45  LOAD_CONST               3.0
               48  LOAD_DEREF            0  'self'
               51  LOAD_ATTR             7  'version'
               54  DUP_TOP          
               55  ROT_THREE        
               56  COMPARE_OP            1  <=
               59  JUMP_IF_FALSE        10  'to 72'
               62  POP_TOP          
               63  LOAD_CONST               3.2
               66  COMPARE_OP            1  <=
               69  JUMP_FORWARD          2  'to 74'
             72_0  COME_FROM            59  '59'
               72  ROT_TWO          
               73  POP_TOP          
             74_0  COME_FROM            69  '69'
               74  JUMP_IF_FALSE        10  'to 87'
               77  POP_TOP          

 L. 365        78  LOAD_CONST               -2
               81  STORE_FAST           52  'lambda_index'
               84  JUMP_FORWARD         33  'to 120'
             87_0  COME_FROM            74  '74'
               87  POP_TOP          

 L. 366        88  LOAD_CONST               3.03
               91  LOAD_DEREF            0  'self'
               94  LOAD_ATTR             7  'version'
               97  COMPARE_OP            1  <=
              100  JUMP_IF_FALSE        10  'to 113'
              103  POP_TOP          

 L. 367       104  LOAD_CONST               -3
              107  STORE_FAST           52  'lambda_index'
              110  JUMP_FORWARD          7  'to 120'
            113_0  COME_FROM           100  '100'
              113  POP_TOP          

 L. 369       114  LOAD_CONST               None
              117  STORE_FAST           52  'lambda_index'
            120_0  COME_FROM           110  '110'
            120_1  COME_FROM            84  '84'

 L. 371       120  LOAD_FAST             1  'node'
              123  LOAD_CONST               -1
              126  BINARY_SUBSCR    
              127  STORE_FAST           58  'args_node'

 L. 373       130  BUILD_MAP             0 
              133  STORE_FAST           32  'annotate_dict'

 L. 378       136  LOAD_FAST            58  'args_node'
              139  LOAD_ATTR            11  'attr'
              142  STORE_FAST           21  'args_attr'

 L. 380       145  LOAD_GLOBAL          13  'isinstance'
              148  LOAD_FAST            21  'args_attr'
              151  LOAD_GLOBAL          14  'tuple'
              154  CALL_FUNCTION_2       2  None
              157  JUMP_IF_FALSE       771  'to 931'
              160  POP_TOP          

 L. 381       161  LOAD_GLOBAL          15  'len'
              164  LOAD_FAST            21  'args_attr'
              167  CALL_FUNCTION_1       1  None
              170  LOAD_CONST               3
              173  COMPARE_OP            2  ==
              176  JUMP_IF_FALSE        19  'to 198'
              179  POP_TOP          

 L. 382       180  LOAD_FAST            21  'args_attr'
              183  UNPACK_SEQUENCE_3     3 
              186  STORE_FAST           30  'pos_args'
              189  STORE_FAST           33  'kw_args'
              192  STORE_FAST           37  'annotate_argc'
              195  JUMP_FORWARD        378  'to 576'
            198_0  COME_FROM           176  '176'
              198  POP_TOP          

 L. 384       199  LOAD_FAST            21  'args_attr'
              202  UNPACK_SEQUENCE_4     4 
              205  STORE_FAST           30  'pos_args'
              208  STORE_FAST           33  'kw_args'
              211  STORE_FAST           37  'annotate_argc'
              214  STORE_FAST           41  'closure'

 L. 386       217  LOAD_CONST               -4
              220  STORE_FAST           46  'i'

 L. 387       223  LOAD_CONST               0
              226  STORE_FAST           56  'kw_pairs'

 L. 388       229  LOAD_FAST            41  'closure'
              232  JUMP_IF_FALSE        14  'to 249'
            235_0  THEN                     250
              235  POP_TOP          

 L. 390       236  LOAD_FAST            46  'i'
              239  LOAD_CONST               1
              242  INPLACE_SUBTRACT 
              243  STORE_FAST           46  'i'
              246  JUMP_FORWARD          1  'to 250'
            249_0  COME_FROM           232  '232'
              249  POP_TOP          
            250_0  COME_FROM           246  '246'

 L. 391       250  LOAD_FAST            37  'annotate_argc'
              253  JUMP_IF_FALSE       241  'to 497'
            256_0  THEN                     498
              256  POP_TOP          

 L. 393       257  LOAD_FAST             1  'node'
              260  LOAD_FAST            46  'i'
              263  BINARY_SUBSCR    
              264  STORE_FAST           42  'annotate_node'

 L. 394       267  LOAD_FAST            42  'annotate_node'
              270  LOAD_CONST               'expr'
              273  COMPARE_OP            2  ==
              276  JUMP_IF_FALSE       204  'to 483'
            279_0  THEN                     484
              279  POP_TOP          

 L. 395       280  LOAD_FAST            42  'annotate_node'
              283  LOAD_CONST               0
              286  BINARY_SUBSCR    
              287  STORE_FAST           42  'annotate_node'

 L. 396       290  LOAD_FAST            42  'annotate_node'
              293  LOAD_CONST               -1
              296  BINARY_SUBSCR    
              297  STORE_FAST           38  'annotate_name_node'

 L. 397       300  LOAD_FAST            42  'annotate_node'
              303  LOAD_CONST               'dict'
              306  COMPARE_OP            2  ==
              309  JUMP_IF_FALSE       167  'to 479'
              312  POP_TOP          
              313  LOAD_FAST            38  'annotate_name_node'
              316  LOAD_ATTR             3  'kind'
              319  LOAD_ATTR             4  'startswith'
              322  LOAD_CONST               'BUILD_CONST_KEY_MAP'
              325  CALL_FUNCTION_1       1  None
              328  JUMP_IF_FALSE       148  'to 479'
            331_0  THEN                     480
              331  POP_TOP          

 L. 400       332  BUILD_LIST_0          0 
              335  DUP_TOP          
              336  STORE_FAST           50  '_[1]'
              339  LOAD_FAST            42  'annotate_node'
              342  LOAD_CONST               -2
              345  SLICE+2          
              346  GET_ITER         
              347  FOR_ITER             28  'to 378'
              350  STORE_FAST           49  'n'
              353  LOAD_FAST            50  '_[1]'
              356  LOAD_DEREF            0  'self'
              359  LOAD_ATTR            26  'traverse'
              362  LOAD_FAST            49  'n'
              365  LOAD_CONST               'indent'
              368  LOAD_CONST               ''
              371  CALL_FUNCTION_257   257  None
              374  LIST_APPEND      
              375  JUMP_BACK           347  'to 347'
              378  DELETE_FAST          50  '_[1]'
              381  STORE_FAST           40  'types'

 L. 403       384  LOAD_FAST            42  'annotate_node'
              387  LOAD_CONST               -2
              390  BINARY_SUBSCR    
              391  LOAD_ATTR            11  'attr'
              394  STORE_FAST           29  'names'

 L. 404       397  LOAD_GLOBAL          15  'len'
              400  LOAD_FAST            40  'types'
              403  CALL_FUNCTION_1       1  None
              406  STORE_FAST           48  'l'

 L. 405       409  LOAD_FAST            48  'l'
              412  LOAD_GLOBAL          15  'len'
              415  LOAD_FAST            29  'names'
              418  CALL_FUNCTION_1       1  None
              421  COMPARE_OP            2  ==
              424  JUMP_IF_TRUE          7  'to 434'
              427  POP_TOP          
              428  LOAD_ASSERT              AssertionError
              431  RAISE_VARARGS_1       1  None
            434_0  COME_FROM           424  '424'
              434  POP_TOP          

 L. 406       435  SETUP_LOOP           42  'to 480'
              438  LOAD_GLOBAL          30  'range'
              441  LOAD_FAST            48  'l'
              444  CALL_FUNCTION_1       1  None
              447  GET_ITER         
              448  FOR_ITER             24  'to 475'
              451  STORE_FAST           46  'i'

 L. 407       454  LOAD_FAST            40  'types'
              457  LOAD_FAST            46  'i'
              460  BINARY_SUBSCR    
              461  LOAD_FAST            32  'annotate_dict'
              464  LOAD_FAST            29  'names'
              467  LOAD_FAST            46  'i'
              470  BINARY_SUBSCR    
              471  STORE_SUBSCR     
              472  JUMP_BACK           448  'to 448'
              475  POP_BLOCK        
            476_0  COME_FROM           435  '435'

 L. 408       476  JUMP_ABSOLUTE       484  'to 484'
            479_0  COME_FROM           328  '328'
            479_1  COME_FROM           309  '309'
              479  POP_TOP          

 L. 409       480  JUMP_FORWARD          1  'to 484'
            483_0  COME_FROM           276  '276'
              483  POP_TOP          
            484_0  COME_FROM           480  '480'

 L. 410       484  LOAD_FAST            46  'i'
              487  LOAD_CONST               1
              490  INPLACE_SUBTRACT 
              491  STORE_FAST           46  'i'
              494  JUMP_FORWARD          1  'to 498'
            497_0  COME_FROM           253  '253'
              497  POP_TOP          
            498_0  COME_FROM           494  '494'

 L. 411       498  LOAD_FAST            33  'kw_args'
              501  JUMP_IF_FALSE        71  'to 575'
            504_0  THEN                     576
              504  POP_TOP          

 L. 412       505  LOAD_FAST             1  'node'
              508  LOAD_FAST            46  'i'
              511  BINARY_SUBSCR    
              512  STORE_FAST           26  'kw_node'

 L. 413       515  LOAD_FAST            26  'kw_node'
              518  LOAD_CONST               'expr'
              521  COMPARE_OP            2  ==
              524  JUMP_IF_FALSE        14  'to 541'
            527_0  THEN                     542
              527  POP_TOP          

 L. 414       528  LOAD_FAST            26  'kw_node'
              531  LOAD_CONST               0
              534  BINARY_SUBSCR    
              535  STORE_FAST           26  'kw_node'
              538  JUMP_FORWARD          1  'to 542'
            541_0  COME_FROM           524  '524'
              541  POP_TOP          
            542_0  COME_FROM           538  '538'

 L. 415       542  LOAD_FAST            26  'kw_node'
              545  LOAD_CONST               'dict'
              548  COMPARE_OP            2  ==
              551  JUMP_IF_FALSE        17  'to 571'
            554_0  THEN                     572
              554  POP_TOP          

 L. 416       555  LOAD_FAST            26  'kw_node'
              558  LOAD_CONST               -1
              561  BINARY_SUBSCR    
              562  LOAD_ATTR            11  'attr'
              565  STORE_FAST           56  'kw_pairs'
              568  JUMP_ABSOLUTE       576  'to 576'
            571_0  COME_FROM           551  '551'
              571  POP_TOP          
              572  JUMP_FORWARD          1  'to 576'
            575_0  COME_FROM           501  '501'
              575  POP_TOP          
            576_0  COME_FROM           572  '572'
            576_1  COME_FROM           195  '195'

 L. 419       576  LOAD_FAST             1  'node'
              579  LOAD_CONST               0
              582  BINARY_SUBSCR    
              583  LOAD_ATTR             3  'kind'
              586  LOAD_ATTR             4  'startswith'
              589  LOAD_CONST               'kwarg'
              592  CALL_FUNCTION_1       1  None
              595  JUMP_IF_TRUE         14  'to 612'
              598  POP_TOP          
              599  LOAD_FAST             1  'node'
              602  LOAD_CONST               0
              605  BINARY_SUBSCR    
              606  LOAD_CONST               'no_kwargs'
              609  COMPARE_OP            2  ==
            612_0  COME_FROM           595  '595'
              612  STORE_FAST           55  'have_kwargs'

 L. 420       615  LOAD_GLOBAL          15  'len'
              618  LOAD_FAST             1  'node'
              621  CALL_FUNCTION_1       1  None
              624  LOAD_CONST               4
              627  COMPARE_OP            5  >=
              630  JUMP_IF_FALSE        10  'to 643'
              633  POP_TOP          

 L. 421       634  LOAD_CONST               -4
              637  STORE_FAST           36  'lc_index'
              640  JUMP_FORWARD          7  'to 650'
            643_0  COME_FROM           630  '630'
              643  POP_TOP          

 L. 423       644  LOAD_CONST               -3
              647  STORE_FAST           36  'lc_index'
            650_0  COME_FROM           640  '640'

 L. 426       650  LOAD_GLOBAL          15  'len'
              653  LOAD_FAST             1  'node'
              656  CALL_FUNCTION_1       1  None
              659  LOAD_CONST               2
              662  COMPARE_OP            4  >
              665  JUMP_IF_FALSE       236  'to 904'
              668  POP_TOP          
              669  LOAD_FAST            55  'have_kwargs'
              672  JUMP_IF_TRUE         20  'to 695'
              675  POP_TOP          
              676  LOAD_FAST             1  'node'
              679  LOAD_FAST            36  'lc_index'
              682  BINARY_SUBSCR    
              683  LOAD_ATTR             3  'kind'
              686  LOAD_CONST               'load_closure'
              689  COMPARE_OP            3  !=
            692_0  COME_FROM           672  '672'
              692  JUMP_IF_FALSE       209  'to 904'
              695  POP_TOP          

 L. 434       696  LOAD_CONST               0
              699  STORE_FAST           12  'default_values_start'

 L. 435       702  LOAD_FAST             1  'node'
              705  LOAD_CONST               0
              708  BINARY_SUBSCR    
              709  LOAD_CONST               'no_kwargs'
              712  COMPARE_OP            2  ==
              715  JUMP_IF_FALSE        14  'to 732'
            718_0  THEN                     733
              718  POP_TOP          

 L. 436       719  LOAD_FAST            12  'default_values_start'
              722  LOAD_CONST               1
              725  INPLACE_ADD      
              726  STORE_FAST           12  'default_values_start'
              729  JUMP_FORWARD          1  'to 733'
            732_0  COME_FROM           715  '715'
              732  POP_TOP          
            733_0  COME_FROM           729  '729'

 L. 440       733  LOAD_FAST             1  'node'
              736  LOAD_FAST            12  'default_values_start'
              739  BINARY_SUBSCR    
              740  LOAD_CONST               'kwarg'
              743  COMPARE_OP            2  ==
              746  JUMP_IF_FALSE        96  'to 845'
              749  POP_TOP          

 L. 441       750  LOAD_FAST             1  'node'
              753  LOAD_FAST            52  'lambda_index'
              756  BINARY_SUBSCR    
              757  LOAD_CONST               'LOAD_LAMBDA'
              760  COMPARE_OP            2  ==
              763  JUMP_IF_TRUE          7  'to 773'
              766  POP_TOP          
              767  LOAD_ASSERT              AssertionError
              770  RAISE_VARARGS_1       1  None
            773_0  COME_FROM           763  '763'
              773  POP_TOP          

 L. 442       774  LOAD_FAST            12  'default_values_start'
              777  STORE_FAST           46  'i'

 L. 443       780  BUILD_LIST_0          0 
              783  STORE_FAST           28  'defparams'

 L. 444       786  SETUP_LOOP          112  'to 901'
              789  LOAD_FAST             1  'node'
              792  LOAD_FAST            46  'i'
              795  BINARY_SUBSCR    
              796  LOAD_CONST               'kwarg'
              799  COMPARE_OP            2  ==
              802  JUMP_IF_FALSE        35  'to 840'
              805  POP_TOP          

 L. 445       806  LOAD_FAST            28  'defparams'
              809  LOAD_ATTR            36  'append'
              812  LOAD_FAST             1  'node'
              815  LOAD_FAST            46  'i'
              818  BINARY_SUBSCR    
              819  LOAD_CONST               1
              822  BINARY_SUBSCR    
              823  CALL_FUNCTION_1       1  None
              826  POP_TOP          

 L. 446       827  LOAD_FAST            46  'i'
              830  LOAD_CONST               1
              833  INPLACE_ADD      
              834  STORE_FAST           46  'i'
              837  JUMP_BACK           789  'to 789'
              840  POP_TOP          
              841  POP_BLOCK        
              842  JUMP_ABSOLUTE       928  'to 928'
            845_0  COME_FROM           746  '746'
              845  POP_TOP          

 L. 448       846  LOAD_FAST             1  'node'
              849  LOAD_FAST            12  'default_values_start'
              852  BINARY_SUBSCR    
              853  LOAD_CONST               'kwargs'
              856  COMPARE_OP            2  ==
              859  JUMP_IF_FALSE        14  'to 876'
            862_0  THEN                     877
              862  POP_TOP          

 L. 449       863  LOAD_FAST            12  'default_values_start'
              866  LOAD_CONST               1
              869  INPLACE_ADD      
              870  STORE_FAST           12  'default_values_start'
              873  JUMP_FORWARD          1  'to 877'
            876_0  COME_FROM           859  '859'
              876  POP_TOP          
            877_0  COME_FROM           873  '873'

 L. 450       877  LOAD_FAST             1  'node'
              880  LOAD_FAST            12  'default_values_start'
              883  LOAD_FAST            12  'default_values_start'
              886  LOAD_FAST            58  'args_node'
              889  LOAD_ATTR            11  'attr'
              892  LOAD_CONST               0
              895  BINARY_SUBSCR    
              896  BINARY_ADD       
              897  SLICE+3          
              898  STORE_FAST           28  'defparams'
            901_0  COME_FROM           786  '786'
              901  JUMP_ABSOLUTE       951  'to 951'
            904_0  COME_FROM           692  '692'
            904_1  COME_FROM           665  '665'
              904  POP_TOP          

 L. 454       905  LOAD_FAST             1  'node'
              908  LOAD_FAST            58  'args_node'
              911  LOAD_ATTR            11  'attr'
              914  LOAD_CONST               0
              917  BINARY_SUBSCR    
              918  SLICE+2          
              919  STORE_FAST           28  'defparams'

 L. 455       922  LOAD_CONST               0
              925  STORE_FAST           33  'kw_args'
              928  JUMP_FORWARD         20  'to 951'
            931_0  COME_FROM           157  '157'
              931  POP_TOP          

 L. 457       932  LOAD_FAST             1  'node'
              935  LOAD_FAST            58  'args_node'
              938  LOAD_ATTR            11  'attr'
              941  SLICE+2          
              942  STORE_FAST           28  'defparams'

 L. 458       945  LOAD_CONST               0
              948  STORE_FAST           33  'kw_args'
            951_0  COME_FROM           928  '928'

 L. 461       951  LOAD_CONST               3.0
              954  LOAD_DEREF            0  'self'
              957  LOAD_ATTR             7  'version'
              960  DUP_TOP          
              961  ROT_THREE        
              962  COMPARE_OP            1  <=
              965  JUMP_IF_FALSE        10  'to 978'
              968  POP_TOP          
              969  LOAD_CONST               3.2
              972  COMPARE_OP            1  <=
              975  JUMP_FORWARD          2  'to 980'
            978_0  COME_FROM           965  '965'
              978  ROT_TWO          
              979  POP_TOP          
            980_0  COME_FROM           975  '975'
              980  JUMP_IF_FALSE        10  'to 993'
              983  POP_TOP          

 L. 462       984  LOAD_CONST               -2
              987  STORE_FAST           52  'lambda_index'
              990  JUMP_FORWARD         33  'to 1026'
            993_0  COME_FROM           980  '980'
              993  POP_TOP          

 L. 463       994  LOAD_CONST               3.03
              997  LOAD_DEREF            0  'self'
             1000  LOAD_ATTR             7  'version'
             1003  COMPARE_OP            1  <=
             1006  JUMP_IF_FALSE        10  'to 1019'
             1009  POP_TOP          

 L. 464      1010  LOAD_CONST               -3
             1013  STORE_FAST           52  'lambda_index'
             1016  JUMP_FORWARD          7  'to 1026'
           1019_0  COME_FROM          1006  '1006'
             1019  POP_TOP          

 L. 466      1020  LOAD_CONST               None
             1023  STORE_FAST           52  'lambda_index'
           1026_0  COME_FROM          1016  '1016'
           1026_1  COME_FROM           990  '990'

 L. 468      1026  LOAD_FAST            52  'lambda_index'
             1029  JUMP_IF_FALSE        71  'to 1103'
             1032  POP_TOP          
             1033  LOAD_FAST             2  'is_lambda'
             1036  JUMP_IF_FALSE        64  'to 1103'
             1039  POP_TOP          
             1040  LOAD_GLOBAL          38  'iscode'
             1043  LOAD_FAST             1  'node'
             1046  LOAD_FAST            52  'lambda_index'
             1049  BINARY_SUBSCR    
             1050  LOAD_ATTR            11  'attr'
             1053  CALL_FUNCTION_1       1  None
             1056  JUMP_IF_FALSE        44  'to 1103'
             1059  POP_TOP          

 L. 469      1060  LOAD_FAST             1  'node'
             1063  LOAD_FAST            52  'lambda_index'
             1066  BINARY_SUBSCR    
             1067  LOAD_ATTR             3  'kind'
             1070  LOAD_CONST               'LOAD_LAMBDA'
             1073  COMPARE_OP            2  ==
             1076  JUMP_IF_TRUE          7  'to 1086'
             1079  POP_TOP          
             1080  LOAD_ASSERT              AssertionError
             1083  RAISE_VARARGS_1       1  None
           1086_0  COME_FROM          1076  '1076'
             1086  POP_TOP          

 L. 470      1087  LOAD_FAST             1  'node'
             1090  LOAD_FAST            52  'lambda_index'
             1093  BINARY_SUBSCR    
             1094  LOAD_ATTR            11  'attr'
             1097  STORE_FAST            5  'code'
             1100  JUMP_FORWARD         10  'to 1113'
           1103_0  COME_FROM          1056  '1056'
           1103_1  COME_FROM          1036  '1036'
           1103_2  COME_FROM          1029  '1029'
             1103  POP_TOP          

 L. 472      1104  LOAD_FAST             4  'code_node'
             1107  LOAD_ATTR            11  'attr'
             1110  STORE_FAST            5  'code'
           1113_0  COME_FROM          1100  '1100'

 L. 474      1113  LOAD_GLOBAL          38  'iscode'
             1116  LOAD_FAST             5  'code'
             1119  CALL_FUNCTION_1       1  None
             1122  JUMP_IF_TRUE          7  'to 1132'
             1125  POP_TOP          
             1126  LOAD_ASSERT              AssertionError
             1129  RAISE_VARARGS_1       1  None
           1132_0  COME_FROM          1122  '1122'
             1132  POP_TOP          

 L. 475      1133  LOAD_GLOBAL          41  'Code'
             1136  LOAD_FAST             5  'code'
             1139  LOAD_DEREF            0  'self'
             1142  LOAD_ATTR            42  'scanner'
             1145  LOAD_DEREF            0  'self'
             1148  LOAD_ATTR            43  'currentclass'
             1151  CALL_FUNCTION_3       3  None
             1154  STORE_FAST            8  'scanner_code'

 L. 478      1157  LOAD_FAST             5  'code'
             1160  LOAD_ATTR            45  'co_argcount'
             1163  STORE_FAST           15  'argc'

 L. 479      1166  LOAD_FAST             5  'code'
             1169  LOAD_ATTR            47  'co_kwonlyargcount'
             1172  STORE_FAST            9  'kwonlyargcount'

 L. 481      1175  LOAD_GLOBAL          49  'list'
             1178  LOAD_FAST             8  'scanner_code'
             1181  LOAD_ATTR            50  'co_varnames'
             1184  LOAD_FAST            15  'argc'
             1187  SLICE+2          
             1188  CALL_FUNCTION_1       1  None
             1191  STORE_FAST           35  'paramnames'

 L. 482      1194  LOAD_FAST             9  'kwonlyargcount'
             1197  LOAD_CONST               0
             1200  COMPARE_OP            4  >
             1203  JUMP_IF_FALSE        94  'to 1300'
           1206_0  THEN                     1301
             1206  POP_TOP          

 L. 483      1207  LOAD_FAST             2  'is_lambda'
             1210  JUMP_IF_FALSE        57  'to 1270'
           1213_0  THEN                     1297
             1213  POP_TOP          

 L. 484      1214  BUILD_LIST_0          0 
             1217  STORE_FAST           24  'kwargs'

 L. 485      1220  SETUP_LOOP           74  'to 1297'
             1223  LOAD_GLOBAL          30  'range'
             1226  LOAD_FAST             9  'kwonlyargcount'
             1229  CALL_FUNCTION_1       1  None
             1232  GET_ITER         
             1233  FOR_ITER             30  'to 1266'
             1236  STORE_FAST           46  'i'

 L. 486      1239  LOAD_FAST            35  'paramnames'
             1242  LOAD_ATTR            36  'append'
             1245  LOAD_FAST             8  'scanner_code'
             1248  LOAD_ATTR            50  'co_varnames'
             1251  LOAD_FAST            15  'argc'
             1254  LOAD_FAST            46  'i'
             1257  BINARY_ADD       
             1258  BINARY_SUBSCR    
             1259  CALL_FUNCTION_1       1  None
             1262  POP_TOP          
             1263  JUMP_BACK          1233  'to 1233'
             1266  POP_BLOCK        
           1267_0  COME_FROM          1220  '1220'

 L. 487      1267  JUMP_ABSOLUTE      1301  'to 1301'
           1270_0  COME_FROM          1210  '1210'
             1270  POP_TOP          

 L. 489      1271  LOAD_GLOBAL          49  'list'
             1274  LOAD_FAST             8  'scanner_code'
             1277  LOAD_ATTR            50  'co_varnames'
             1280  LOAD_FAST            15  'argc'
             1283  LOAD_FAST            15  'argc'
             1286  LOAD_FAST             9  'kwonlyargcount'
             1289  BINARY_ADD       
             1290  SLICE+3          
             1291  CALL_FUNCTION_1       1  None
             1294  STORE_FAST           24  'kwargs'
             1297  JUMP_FORWARD          1  'to 1301'
           1300_0  COME_FROM          1203  '1203'
             1300  POP_TOP          
           1301_0  COME_FROM          1297  '1297'

 L. 492      1301  LOAD_FAST            35  'paramnames'
             1304  LOAD_ATTR            53  'reverse'
             1307  CALL_FUNCTION_0       0  None
             1310  POP_TOP          

 L. 493      1311  LOAD_FAST            28  'defparams'
             1314  LOAD_ATTR            53  'reverse'
             1317  CALL_FUNCTION_0       0  None
             1320  POP_TOP          

 L. 495      1321  SETUP_EXCEPT         49  'to 1373'

 L. 496      1324  LOAD_DEREF            0  'self'
             1327  LOAD_ATTR            54  'build_ast'
             1330  LOAD_FAST             8  'scanner_code'
             1333  LOAD_ATTR            55  '_tokens'

 L. 497      1336  LOAD_FAST             8  'scanner_code'
             1339  LOAD_ATTR            56  '_customize'

 L. 498      1342  LOAD_CONST               'is_lambda'
             1345  LOAD_FAST             2  'is_lambda'

 L. 499      1348  LOAD_CONST               'noneInNames'
             1351  LOAD_CONST               'None'
             1354  LOAD_FAST             5  'code'
             1357  LOAD_ATTR            57  'co_names'
             1360  COMPARE_OP            6  in
             1363  CALL_FUNCTION_514   514  None
             1366  STORE_FAST           19  'ast'
             1369  POP_BLOCK        
             1370  JUMP_FORWARD         67  'to 1440'
           1373_0  COME_FROM          1321  '1321'

 L. 500      1373  DUP_TOP          
             1374  LOAD_GLOBAL          59  'ParserError'
             1377  COMPARE_OP           10  exception-match
             1380  JUMP_IF_FALSE        55  'to 1438'
             1383  POP_TOP          
             1384  POP_TOP          
             1385  STORE_FAST           51  'p'
             1388  POP_TOP          

 L. 501      1389  LOAD_DEREF            0  'self'
             1392  LOAD_ATTR            61  'write'
             1395  LOAD_GLOBAL          62  'str'
             1398  LOAD_FAST            51  'p'
             1401  CALL_FUNCTION_1       1  None
             1404  CALL_FUNCTION_1       1  None
             1407  POP_TOP          

 L. 502      1408  LOAD_DEREF            0  'self'
             1411  LOAD_ATTR            63  'tolerate_errors'
             1414  JUMP_IF_TRUE         13  'to 1430'
           1417_0  THEN                     1431
             1417  POP_TOP          

 L. 503      1418  LOAD_FAST            51  'p'
             1421  LOAD_DEREF            0  'self'
             1424  STORE_ATTR           64  'ERROR'
             1427  JUMP_FORWARD          1  'to 1431'
           1430_0  COME_FROM          1414  '1414'
             1430  POP_TOP          
           1431_0  COME_FROM          1427  '1427'

 L. 504      1431  LOAD_CONST               None
             1434  RETURN_VALUE     
             1435  JUMP_FORWARD          2  'to 1440'
             1438  POP_TOP          
             1439  END_FINALLY      
           1440_0  COME_FROM          1435  '1435'
           1440_1  COME_FROM          1370  '1370'

 L. 506      1440  LOAD_GLOBAL          15  'len'
             1443  LOAD_FAST            35  'paramnames'
             1446  CALL_FUNCTION_1       1  None
             1449  LOAD_GLOBAL          15  'len'
             1452  LOAD_FAST            28  'defparams'
             1455  CALL_FUNCTION_1       1  None
             1458  BINARY_SUBTRACT  
             1459  STORE_FAST           46  'i'

 L. 509      1462  BUILD_LIST_0          0 
             1465  STORE_FAST           23  'params'

 L. 510      1468  LOAD_FAST            28  'defparams'
             1471  JUMP_IF_FALSE       160  'to 1634'
             1474  POP_TOP          

 L. 511      1475  SETUP_LOOP           71  'to 1549'
             1478  LOAD_GLOBAL          66  'enumerate'
             1481  LOAD_FAST            28  'defparams'
             1484  CALL_FUNCTION_1       1  None
             1487  GET_ITER         
             1488  FOR_ITER             57  'to 1548'
             1491  UNPACK_SEQUENCE_2     2 
             1494  STORE_FAST           46  'i'
             1497  STORE_FAST           43  'defparam'

 L. 512      1500  LOAD_FAST            23  'params'
             1503  LOAD_ATTR            36  'append'
             1506  LOAD_FAST            11  'build_param'
             1509  LOAD_FAST            19  'ast'
             1512  LOAD_FAST            35  'paramnames'
             1515  LOAD_FAST            46  'i'
             1518  BINARY_SUBSCR    
             1519  LOAD_FAST            43  'defparam'
             1522  LOAD_FAST            32  'annotate_dict'
             1525  LOAD_ATTR            68  'get'
             1528  LOAD_FAST            35  'paramnames'
             1531  LOAD_FAST            46  'i'
             1534  BINARY_SUBSCR    
             1535  CALL_FUNCTION_1       1  None
             1538  CALL_FUNCTION_4       4  None
             1541  CALL_FUNCTION_1       1  None
             1544  POP_TOP          
             1545  JUMP_BACK          1488  'to 1488'
             1548  POP_BLOCK        
           1549_0  COME_FROM          1475  '1475'

 L. 518      1549  SETUP_LOOP          157  'to 1709'
             1552  LOAD_FAST            35  'paramnames'
             1555  LOAD_FAST            46  'i'
             1558  LOAD_CONST               1
             1561  BINARY_ADD       
             1562  SLICE+1          
             1563  GET_ITER         
             1564  FOR_ITER             63  'to 1630'
             1567  STORE_FAST           27  'param'

 L. 519      1570  LOAD_FAST            27  'param'
             1573  LOAD_FAST            32  'annotate_dict'
             1576  COMPARE_OP            6  in
             1579  JUMP_IF_FALSE        31  'to 1613'
             1582  POP_TOP          

 L. 520      1583  LOAD_FAST            23  'params'
             1586  LOAD_ATTR            36  'append'
             1589  LOAD_CONST               '%s: %s'
             1592  LOAD_FAST            27  'param'
             1595  LOAD_FAST            32  'annotate_dict'
             1598  LOAD_FAST            27  'param'
             1601  BINARY_SUBSCR    
             1602  BUILD_TUPLE_2         2 
             1605  BINARY_MODULO    
             1606  CALL_FUNCTION_1       1  None
             1609  POP_TOP          
             1610  JUMP_BACK          1564  'to 1564'
           1613_0  COME_FROM          1579  '1579'
             1613  POP_TOP          

 L. 522      1614  LOAD_FAST            23  'params'
             1617  LOAD_ATTR            36  'append'
             1620  LOAD_FAST            27  'param'
             1623  CALL_FUNCTION_1       1  None
             1626  POP_TOP          
             1627  JUMP_BACK          1564  'to 1564'
             1630  POP_BLOCK        
             1631  JUMP_FORWARD         75  'to 1709'
           1634_0  COME_FROM          1471  '1471'
             1634  POP_TOP          

 L. 524      1635  SETUP_LOOP           71  'to 1709'
             1638  LOAD_FAST            35  'paramnames'
             1641  GET_ITER         
             1642  FOR_ITER             63  'to 1708'
             1645  STORE_FAST           27  'param'

 L. 525      1648  LOAD_FAST            27  'param'
             1651  LOAD_FAST            32  'annotate_dict'
             1654  COMPARE_OP            6  in
             1657  JUMP_IF_FALSE        31  'to 1691'
             1660  POP_TOP          

 L. 526      1661  LOAD_FAST            23  'params'
             1664  LOAD_ATTR            36  'append'
             1667  LOAD_CONST               '%s: %s'
             1670  LOAD_FAST            27  'param'
             1673  LOAD_FAST            32  'annotate_dict'
             1676  LOAD_FAST            27  'param'
             1679  BINARY_SUBSCR    
             1680  BUILD_TUPLE_2         2 
             1683  BINARY_MODULO    
             1684  CALL_FUNCTION_1       1  None
             1687  POP_TOP          
             1688  JUMP_BACK          1642  'to 1642'
           1691_0  COME_FROM          1657  '1657'
             1691  POP_TOP          

 L. 528      1692  LOAD_FAST            23  'params'
             1695  LOAD_ATTR            36  'append'
             1698  LOAD_FAST            27  'param'
             1701  CALL_FUNCTION_1       1  None
             1704  POP_TOP          
             1705  JUMP_BACK          1642  'to 1642'
             1708  POP_BLOCK        
           1709_0  COME_FROM          1635  '1635'
           1709_1  COME_FROM          1549  '1549'

 L. 530      1709  LOAD_FAST            23  'params'
             1712  LOAD_ATTR            53  'reverse'
             1715  CALL_FUNCTION_0       0  None
             1718  POP_TOP          

 L. 532      1719  LOAD_GLOBAL          70  'code_has_star_arg'
             1722  LOAD_FAST             5  'code'
             1725  CALL_FUNCTION_1       1  None
             1728  JUMP_IF_FALSE       131  'to 1862'
             1731  POP_TOP          

 L. 533      1732  LOAD_FAST             5  'code'
             1735  LOAD_ATTR            50  'co_varnames'
             1738  LOAD_FAST            15  'argc'
             1741  LOAD_FAST             9  'kwonlyargcount'
             1744  BINARY_ADD       
             1745  BINARY_SUBSCR    
             1746  STORE_FAST           57  'star_arg'

 L. 534      1749  LOAD_FAST            32  'annotate_dict'
             1752  JUMP_IF_FALSE        44  'to 1799'
             1755  POP_TOP          
             1756  LOAD_FAST            57  'star_arg'
             1759  LOAD_FAST            32  'annotate_dict'
             1762  COMPARE_OP            6  in
             1765  JUMP_IF_FALSE        31  'to 1799'
             1768  POP_TOP          

 L. 535      1769  LOAD_FAST            23  'params'
             1772  LOAD_ATTR            36  'append'
             1775  LOAD_CONST               '*%s: %s'
             1778  LOAD_FAST            57  'star_arg'
             1781  LOAD_FAST            32  'annotate_dict'
             1784  LOAD_FAST            57  'star_arg'
             1787  BINARY_SUBSCR    
             1788  BUILD_TUPLE_2         2 
             1791  BINARY_MODULO    
             1792  CALL_FUNCTION_1       1  None
             1795  POP_TOP          
             1796  JUMP_FORWARD         18  'to 1817'
           1799_0  COME_FROM          1765  '1765'
           1799_1  COME_FROM          1752  '1752'
             1799  POP_TOP          

 L. 537      1800  LOAD_FAST            23  'params'
             1803  LOAD_ATTR            36  'append'
             1806  LOAD_CONST               '*%s'
             1809  LOAD_FAST            57  'star_arg'
             1812  BINARY_MODULO    
             1813  CALL_FUNCTION_1       1  None
             1816  POP_TOP          
           1817_0  COME_FROM          1796  '1796'

 L. 539      1817  LOAD_FAST             2  'is_lambda'
             1820  JUMP_IF_FALSE        14  'to 1837'
           1823_0  THEN                     1838
             1823  POP_TOP          

 L. 540      1824  LOAD_FAST            23  'params'
             1827  LOAD_ATTR            53  'reverse'
             1830  CALL_FUNCTION_0       0  None
             1833  POP_TOP          
             1834  JUMP_FORWARD          1  'to 1838'
           1837_0  COME_FROM          1820  '1820'
             1837  POP_TOP          
           1838_0  COME_FROM          1834  '1834'

 L. 541      1838  LOAD_FAST             2  'is_lambda'
             1841  JUMP_IF_TRUE         14  'to 1858'
             1844  POP_TOP          

 L. 542      1845  LOAD_FAST            15  'argc'
             1848  LOAD_CONST               1
             1851  INPLACE_ADD      
             1852  STORE_FAST           15  'argc'
             1855  JUMP_ABSOLUTE      1909  'to 1909'
           1858_0  COME_FROM          1841  '1841'
             1858  POP_TOP          

 L. 543      1859  JUMP_FORWARD         47  'to 1909'
           1862_0  COME_FROM          1728  '1728'
             1862  POP_TOP          

 L. 544      1863  LOAD_FAST             2  'is_lambda'
             1866  JUMP_IF_FALSE        39  'to 1908'
             1869  POP_TOP          
             1870  LOAD_FAST             9  'kwonlyargcount'
             1873  LOAD_CONST               0
             1876  COMPARE_OP            4  >
             1879  JUMP_IF_FALSE        26  'to 1908'
           1882_0  THEN                     1909
             1882  POP_TOP          

 L. 545      1883  LOAD_FAST            23  'params'
             1886  LOAD_ATTR            72  'insert'
             1889  LOAD_CONST               0
             1892  LOAD_CONST               '*'
             1895  CALL_FUNCTION_2       2  None
             1898  POP_TOP          

 L. 546      1899  LOAD_CONST               0
             1902  STORE_FAST            9  'kwonlyargcount'
             1905  JUMP_FORWARD          1  'to 1909'
           1908_0  COME_FROM          1879  '1879'
           1908_1  COME_FROM          1866  '1866'
             1908  POP_TOP          
           1909_0  COME_FROM          1905  '1905'
           1909_1  COME_FROM          1859  '1859'

 L. 549      1909  LOAD_FAST             2  'is_lambda'
             1912  JUMP_IF_FALSE       174  'to 2089'
             1915  POP_TOP          

 L. 550      1916  LOAD_DEREF            0  'self'
             1919  LOAD_ATTR            61  'write'
             1922  LOAD_CONST               'lambda '
             1925  LOAD_CONST               ', '
             1928  LOAD_ATTR            73  'join'
             1931  LOAD_FAST            23  'params'
             1934  CALL_FUNCTION_1       1  None
             1937  CALL_FUNCTION_2       2  None
             1940  POP_TOP          

 L. 557      1941  LOAD_GLOBAL          15  'len'
             1944  LOAD_FAST            19  'ast'
             1947  CALL_FUNCTION_1       1  None
             1950  LOAD_CONST               1
             1953  COMPARE_OP            4  >
             1956  JUMP_IF_FALSE       126  'to 2085'
             1959  POP_TOP          
             1960  LOAD_DEREF            0  'self'
             1963  LOAD_ATTR            26  'traverse'
             1966  LOAD_FAST            19  'ast'
             1969  LOAD_CONST               -1
             1972  BINARY_SUBSCR    
             1973  CALL_FUNCTION_1       1  None
             1976  LOAD_CONST               'None'
             1979  COMPARE_OP            2  ==
             1982  JUMP_IF_FALSE       100  'to 2085'
             1985  POP_TOP          
             1986  LOAD_DEREF            0  'self'
             1989  LOAD_ATTR            26  'traverse'
             1992  LOAD_FAST            19  'ast'
             1995  LOAD_CONST               -2
             1998  BINARY_SUBSCR    
             1999  CALL_FUNCTION_1       1  None
             2002  LOAD_ATTR            74  'strip'
             2005  CALL_FUNCTION_0       0  None
             2008  LOAD_ATTR             4  'startswith'
             2011  LOAD_CONST               'yield'
             2014  CALL_FUNCTION_1       1  None
             2017  JUMP_IF_FALSE        65  'to 2085'
             2020  POP_TOP          

 L. 562      2021  LOAD_FAST            19  'ast'
             2024  LOAD_CONST               -1
             2027  DELETE_SUBSCR    

 L. 564      2028  LOAD_FAST            19  'ast'
             2031  LOAD_CONST               -1
             2034  BINARY_SUBSCR    
             2035  STORE_FAST           17  'ast_expr'

 L. 565      2038  SETUP_LOOP           31  'to 2072'
             2041  LOAD_FAST            17  'ast_expr'
             2044  LOAD_ATTR             3  'kind'
             2047  LOAD_CONST               'expr'
             2050  COMPARE_OP            3  !=
             2053  JUMP_IF_FALSE        14  'to 2070'
             2056  POP_TOP          

 L. 566      2057  LOAD_FAST            17  'ast_expr'
             2060  LOAD_CONST               0
             2063  BINARY_SUBSCR    
             2064  STORE_FAST           17  'ast_expr'
             2067  JUMP_BACK          2041  'to 2041'
             2070  POP_TOP          
             2071  POP_BLOCK        
           2072_0  COME_FROM          2038  '2038'

 L. 567      2072  LOAD_FAST            17  'ast_expr'
             2075  LOAD_FAST            19  'ast'
             2078  LOAD_CONST               -1
             2081  STORE_SUBSCR     

 L. 568      2082  JUMP_ABSOLUTE      2115  'to 2115'
           2085_0  COME_FROM          2017  '2017'
           2085_1  COME_FROM          1982  '1982'
           2085_2  COME_FROM          1956  '1956'
             2085  POP_TOP          
             2086  JUMP_FORWARD         26  'to 2115'
           2089_0  COME_FROM          1912  '1912'
             2089  POP_TOP          

 L. 571      2090  LOAD_DEREF            0  'self'
             2093  LOAD_ATTR            61  'write'
             2096  LOAD_CONST               '('
             2099  LOAD_CONST               ', '
             2102  LOAD_ATTR            73  'join'
             2105  LOAD_FAST            23  'params'
             2108  CALL_FUNCTION_1       1  None
             2111  CALL_FUNCTION_2       2  None
             2114  POP_TOP          
           2115_0  COME_FROM          2086  '2086'

 L. 577      2115  LOAD_GLOBAL          76  'False'
             2118  STORE_FAST           25  'ends_in_comma'

 L. 578      2121  LOAD_FAST             9  'kwonlyargcount'
             2124  LOAD_CONST               0
             2127  COMPARE_OP            4  >
             2130  JUMP_IF_FALSE       485  'to 2618'
             2133  POP_TOP          

 L. 579      2134  LOAD_CONST               4
             2137  LOAD_FAST             5  'code'
             2140  LOAD_ATTR            78  'co_flags'
             2143  BINARY_AND       
             2144  JUMP_IF_TRUE         53  'to 2200'
             2147  POP_TOP          

 L. 580      2148  LOAD_FAST            15  'argc'
             2151  LOAD_CONST               0
             2154  COMPARE_OP            4  >
             2157  JUMP_IF_FALSE        17  'to 2177'
             2160  POP_TOP          

 L. 581      2161  LOAD_DEREF            0  'self'
             2164  LOAD_ATTR            61  'write'
             2167  LOAD_CONST               ', *, '
             2170  CALL_FUNCTION_1       1  None
             2173  POP_TOP          
             2174  JUMP_FORWARD         14  'to 2191'
           2177_0  COME_FROM          2157  '2157'
             2177  POP_TOP          

 L. 583      2178  LOAD_DEREF            0  'self'
             2181  LOAD_ATTR            61  'write'
             2184  LOAD_CONST               '*, '
             2187  CALL_FUNCTION_1       1  None
             2190  POP_TOP          
           2191_0  COME_FROM          2174  '2174'

 L. 585      2191  LOAD_GLOBAL          79  'True'
             2194  STORE_FAST           25  'ends_in_comma'
             2197  JUMP_FORWARD         54  'to 2254'
           2200_0  COME_FROM          2144  '2144'
             2200  POP_TOP          

 L. 587      2201  LOAD_FAST            15  'argc'
             2204  LOAD_CONST               0
             2207  COMPARE_OP            4  >
             2210  JUMP_IF_FALSE        40  'to 2253'
             2213  POP_TOP          
             2214  LOAD_FAST             1  'node'
             2217  LOAD_CONST               0
             2220  BINARY_SUBSCR    
             2221  LOAD_CONST               'kwarg'
             2224  COMPARE_OP            3  !=
             2227  JUMP_IF_FALSE        23  'to 2253'
           2230_0  THEN                     2254
             2230  POP_TOP          

 L. 588      2231  LOAD_DEREF            0  'self'
             2234  LOAD_ATTR            61  'write'
             2237  LOAD_CONST               ', '
             2240  CALL_FUNCTION_1       1  None
             2243  POP_TOP          

 L. 589      2244  LOAD_GLOBAL          79  'True'
             2247  STORE_FAST           25  'ends_in_comma'
             2250  JUMP_FORWARD          1  'to 2254'
           2253_0  COME_FROM          2227  '2227'
           2253_1  COME_FROM          2210  '2210'
             2253  POP_TOP          
           2254_0  COME_FROM          2250  '2250'
           2254_1  COME_FROM          2197  '2197'

 L. 591      2254  LOAD_CONST               None
             2257  BUILD_LIST_1          1 
             2260  LOAD_FAST             9  'kwonlyargcount'
             2263  BINARY_MULTIPLY  
             2264  STORE_FAST           33  'kw_args'

 L. 592      2267  LOAD_DEREF            0  'self'
             2270  LOAD_ATTR             7  'version'
             2273  LOAD_CONST               3.3
             2276  COMPARE_OP            1  <=
             2279  JUMP_IF_FALSE        14  'to 2296'
             2282  POP_TOP          

 L. 593      2283  LOAD_FAST             1  'node'
             2286  LOAD_CONST               0
             2289  BINARY_SUBSCR    
             2290  STORE_FAST           10  'kw_nodes'
             2293  JUMP_FORWARD         18  'to 2314'
           2296_0  COME_FROM          2279  '2279'
             2296  POP_TOP          

 L. 595      2297  LOAD_FAST             1  'node'
             2300  LOAD_FAST            58  'args_node'
             2303  LOAD_ATTR            11  'attr'
             2306  LOAD_CONST               0
             2309  BINARY_SUBSCR    
             2310  BINARY_SUBSCR    
             2311  STORE_FAST           10  'kw_nodes'
           2314_0  COME_FROM          2293  '2293'

 L. 596      2314  LOAD_FAST            10  'kw_nodes'
             2317  LOAD_CONST               'kwargs'
             2320  COMPARE_OP            2  ==
             2323  JUMP_IF_FALSE       100  'to 2426'
           2326_0  THEN                     2427
             2326  POP_TOP          

 L. 597      2327  SETUP_LOOP           97  'to 2427'
             2330  LOAD_FAST            10  'kw_nodes'
             2333  GET_ITER         
             2334  FOR_ITER             85  'to 2422'
             2337  STORE_FAST           49  'n'

 L. 598      2340  LOAD_GLOBAL          81  'eval'
             2343  LOAD_FAST            49  'n'
             2346  LOAD_CONST               0
             2349  BINARY_SUBSCR    
             2350  LOAD_ATTR            82  'pattr'
             2353  CALL_FUNCTION_1       1  None
             2356  STORE_FAST           44  'name'

 L. 599      2359  LOAD_DEREF            0  'self'
             2362  LOAD_ATTR            26  'traverse'
             2365  LOAD_FAST            49  'n'
             2368  LOAD_CONST               1
             2371  BINARY_SUBSCR    
             2372  LOAD_CONST               'indent'
             2375  LOAD_CONST               ''
             2378  CALL_FUNCTION_257   257  None
             2381  STORE_FAST           22  'default'

 L. 600      2384  LOAD_FAST            24  'kwargs'
             2387  LOAD_ATTR            85  'index'
             2390  LOAD_FAST            44  'name'
             2393  CALL_FUNCTION_1       1  None
             2396  STORE_FAST           45  'idx'

 L. 601      2399  LOAD_CONST               '%s=%s'
             2402  LOAD_FAST            44  'name'
             2405  LOAD_FAST            22  'default'
             2408  BUILD_TUPLE_2         2 
             2411  BINARY_MODULO    
             2412  LOAD_FAST            33  'kw_args'
             2415  LOAD_FAST            45  'idx'
             2418  STORE_SUBSCR     

 L. 602      2419  JUMP_BACK          2334  'to 2334'
             2422  POP_BLOCK        

 L. 603      2423  JUMP_FORWARD          1  'to 2427'
           2426_0  COME_FROM          2323  '2323'
             2426  POP_TOP          
           2427_0  COME_FROM          2327  '2327'

 L. 611      2427  LOAD_FAST            10  'kw_nodes'
             2430  LOAD_CONST               'kwarg'
             2433  COMPARE_OP            3  !=
             2436  JUMP_IF_TRUE         16  'to 2455'
             2439  POP_TOP          
             2440  LOAD_DEREF            0  'self'
             2443  LOAD_ATTR             7  'version'
             2446  LOAD_CONST               3.5
             2449  COMPARE_OP            2  ==
           2452_0  COME_FROM          2436  '2436'
             2452  JUMP_IF_FALSE       159  'to 2614'
             2455  POP_TOP          

 L. 612      2456  BUILD_LIST_0          0 
             2459  DUP_TOP          
             2460  STORE_FAST           50  '_[1]'
             2463  LOAD_FAST            33  'kw_args'
             2466  GET_ITER         
             2467  FOR_ITER             19  'to 2489'
             2470  STORE_FAST           31  'c'
             2473  LOAD_FAST            50  '_[1]'
             2476  LOAD_FAST            31  'c'
             2479  LOAD_CONST               None
             2482  COMPARE_OP            2  ==
             2485  LIST_APPEND      
             2486  JUMP_BACK          2467  'to 2467'
             2489  DELETE_FAST          50  '_[1]'
             2492  STORE_FAST           47  'other_kw'

 L. 614      2495  SETUP_LOOP           85  'to 2583'
             2498  LOAD_GLOBAL          66  'enumerate'
             2501  LOAD_FAST            47  'other_kw'
             2504  CALL_FUNCTION_1       1  None
             2507  GET_ITER         
             2508  FOR_ITER             71  'to 2582'
             2511  UNPACK_SEQUENCE_2     2 
             2514  STORE_FAST           46  'i'
             2517  STORE_FAST           34  'flag'

 L. 615      2520  LOAD_FAST            34  'flag'
             2523  JUMP_IF_FALSE        52  'to 2578'
             2526  POP_TOP          

 L. 616      2527  LOAD_FAST            46  'i'
             2530  LOAD_GLOBAL          15  'len'
             2533  LOAD_FAST            24  'kwargs'
             2536  CALL_FUNCTION_1       1  None
             2539  COMPARE_OP            0  <
             2542  JUMP_IF_FALSE        22  'to 2567'
             2545  POP_TOP          

 L. 617      2546  LOAD_CONST               '%s'
             2549  LOAD_FAST            24  'kwargs'
             2552  LOAD_FAST            46  'i'
             2555  BINARY_SUBSCR    
             2556  BINARY_MODULO    
             2557  LOAD_FAST            33  'kw_args'
             2560  LOAD_FAST            46  'i'
             2563  STORE_SUBSCR     
             2564  JUMP_ABSOLUTE      2579  'to 2579'
           2567_0  COME_FROM          2542  '2542'
             2567  POP_TOP          

 L. 619      2568  LOAD_FAST            33  'kw_args'
             2571  LOAD_FAST            46  'i'
             2574  DELETE_SUBSCR    

 L. 620      2575  JUMP_BACK          2508  'to 2508'
           2578_0  COME_FROM          2523  '2523'
             2578  POP_TOP          
             2579  JUMP_BACK          2508  'to 2508'
             2582  POP_BLOCK        
           2583_0  COME_FROM          2495  '2495'

 L. 622      2583  LOAD_DEREF            0  'self'
             2586  LOAD_ATTR            61  'write'
             2589  LOAD_CONST               ', '
             2592  LOAD_ATTR            73  'join'
             2595  LOAD_FAST            33  'kw_args'
             2598  CALL_FUNCTION_1       1  None
             2601  CALL_FUNCTION_1       1  None
             2604  POP_TOP          

 L. 623      2605  LOAD_GLOBAL          76  'False'
             2608  STORE_FAST           25  'ends_in_comma'

 L. 624      2611  JUMP_ABSOLUTE      2642  'to 2642'
           2614_0  COME_FROM          2452  '2452'
             2614  POP_TOP          

 L. 626      2615  JUMP_FORWARD         24  'to 2642'
           2618_0  COME_FROM          2130  '2130'
             2618  POP_TOP          

 L. 628      2619  LOAD_FAST            15  'argc'
             2622  LOAD_CONST               0
             2625  COMPARE_OP            2  ==
             2628  JUMP_IF_FALSE        10  'to 2641'
           2631_0  THEN                     2642
             2631  POP_TOP          

 L. 629      2632  LOAD_GLOBAL          79  'True'
             2635  STORE_FAST           25  'ends_in_comma'
             2638  JUMP_FORWARD          1  'to 2642'
           2641_0  COME_FROM          2628  '2628'
             2641  POP_TOP          
           2642_0  COME_FROM          2638  '2638'
           2642_1  COME_FROM          2615  '2615'

 L. 631      2642  LOAD_GLOBAL          90  'code_has_star_star_arg'
             2645  LOAD_FAST             5  'code'
             2648  CALL_FUNCTION_1       1  None
             2651  JUMP_IF_FALSE       113  'to 2767'
           2654_0  THEN                     2768
             2654  POP_TOP          

 L. 632      2655  LOAD_FAST            25  'ends_in_comma'
             2658  JUMP_IF_TRUE         17  'to 2678'
           2661_0  THEN                     2679
             2661  POP_TOP          

 L. 633      2662  LOAD_DEREF            0  'self'
             2665  LOAD_ATTR            61  'write'
             2668  LOAD_CONST               ', '
             2671  CALL_FUNCTION_1       1  None
             2674  POP_TOP          
             2675  JUMP_FORWARD          1  'to 2679'
           2678_0  COME_FROM          2658  '2658'
             2678  POP_TOP          
           2679_0  COME_FROM          2675  '2675'

 L. 634      2679  LOAD_FAST             5  'code'
             2682  LOAD_ATTR            50  'co_varnames'
             2685  LOAD_FAST            15  'argc'
             2688  LOAD_FAST             9  'kwonlyargcount'
             2691  BINARY_ADD       
             2692  BINARY_SUBSCR    
             2693  STORE_FAST            7  'star_star_arg'

 L. 635      2696  LOAD_FAST            32  'annotate_dict'
             2699  JUMP_IF_FALSE        44  'to 2746'
             2702  POP_TOP          
             2703  LOAD_FAST             7  'star_star_arg'
             2706  LOAD_FAST            32  'annotate_dict'
             2709  COMPARE_OP            6  in
             2712  JUMP_IF_FALSE        31  'to 2746'
           2715_0  THEN                     2764
             2715  POP_TOP          

 L. 636      2716  LOAD_DEREF            0  'self'
             2719  LOAD_ATTR            61  'write'
             2722  LOAD_CONST               '**%s: %s'
             2725  LOAD_FAST             7  'star_star_arg'
             2728  LOAD_FAST            32  'annotate_dict'
             2731  LOAD_FAST             7  'star_star_arg'
             2734  BINARY_SUBSCR    
             2735  BUILD_TUPLE_2         2 
             2738  BINARY_MODULO    
             2739  CALL_FUNCTION_1       1  None
             2742  POP_TOP          
             2743  JUMP_ABSOLUTE      2768  'to 2768'
           2746_0  COME_FROM          2712  '2712'
           2746_1  COME_FROM          2699  '2699'
             2746  POP_TOP          

 L. 638      2747  LOAD_DEREF            0  'self'
             2750  LOAD_ATTR            61  'write'
             2753  LOAD_CONST               '**%s'
             2756  LOAD_FAST             7  'star_star_arg'
             2759  BINARY_MODULO    
             2760  CALL_FUNCTION_1       1  None
             2763  POP_TOP          
             2764  JUMP_FORWARD          1  'to 2768'
           2767_0  COME_FROM          2651  '2651'
             2767  POP_TOP          
           2768_0  COME_FROM          2764  '2764'

 L. 640      2768  LOAD_FAST             2  'is_lambda'
             2771  JUMP_IF_FALSE        17  'to 2791'
             2774  POP_TOP          

 L. 641      2775  LOAD_DEREF            0  'self'
             2778  LOAD_ATTR            61  'write'
             2781  LOAD_CONST               ': '
             2784  CALL_FUNCTION_1       1  None
             2787  POP_TOP          
             2788  JUMP_FORWARD         72  'to 2863'
           2791_0  COME_FROM          2771  '2771'
             2791  POP_TOP          

 L. 643      2792  LOAD_DEREF            0  'self'
             2795  LOAD_ATTR            61  'write'
             2798  LOAD_CONST               ')'
             2801  CALL_FUNCTION_1       1  None
             2804  POP_TOP          

 L. 644      2805  LOAD_FAST            32  'annotate_dict'
             2808  JUMP_IF_FALSE        38  'to 2849'
             2811  POP_TOP          
             2812  LOAD_CONST               'return'
             2815  LOAD_FAST            32  'annotate_dict'
             2818  COMPARE_OP            6  in
             2821  JUMP_IF_FALSE        25  'to 2849'
           2824_0  THEN                     2850
             2824  POP_TOP          

 L. 645      2825  LOAD_DEREF            0  'self'
             2828  LOAD_ATTR            61  'write'
             2831  LOAD_CONST               ' -> %s'
             2834  LOAD_FAST            32  'annotate_dict'
             2837  LOAD_CONST               'return'
             2840  BINARY_SUBSCR    
             2841  BINARY_MODULO    
             2842  CALL_FUNCTION_1       1  None
             2845  POP_TOP          
             2846  JUMP_FORWARD          1  'to 2850'
           2849_0  COME_FROM          2821  '2821'
           2849_1  COME_FROM          2808  '2808'
             2849  POP_TOP          
           2850_0  COME_FROM          2846  '2846'

 L. 646      2850  LOAD_DEREF            0  'self'
             2853  LOAD_ATTR            92  'println'
             2856  LOAD_CONST               ':'
             2859  CALL_FUNCTION_1       1  None
             2862  POP_TOP          
           2863_0  COME_FROM          2788  '2788'

 L. 648      2863  LOAD_GLOBAL          15  'len'
             2866  LOAD_FAST             5  'code'
             2869  LOAD_ATTR            93  'co_consts'
             2872  CALL_FUNCTION_1       1  None
             2875  LOAD_CONST               0
             2878  COMPARE_OP            4  >
             2881  JUMP_IF_FALSE        58  'to 2942'
             2884  POP_TOP          
             2885  LOAD_FAST             5  'code'
             2888  LOAD_ATTR            93  'co_consts'
             2891  LOAD_CONST               0
             2894  BINARY_SUBSCR    
             2895  LOAD_CONST               None
             2898  COMPARE_OP            9  is-not
             2901  JUMP_IF_FALSE        38  'to 2942'
             2904  POP_TOP          
             2905  LOAD_FAST             2  'is_lambda'
             2908  UNARY_NOT        
             2909  JUMP_IF_FALSE        30  'to 2942'
           2912_0  THEN                     2943
             2912  POP_TOP          

 L. 652      2913  LOAD_GLOBAL          94  'print_docstring'
             2916  LOAD_DEREF            0  'self'
             2919  LOAD_DEREF            0  'self'
             2922  LOAD_ATTR            95  'indent'
             2925  LOAD_FAST             5  'code'
             2928  LOAD_ATTR            93  'co_consts'
             2931  LOAD_CONST               0
             2934  BINARY_SUBSCR    
             2935  CALL_FUNCTION_3       3  None
             2938  POP_TOP          
             2939  JUMP_FORWARD          1  'to 2943'
           2942_0  COME_FROM          2909  '2909'
           2942_1  COME_FROM          2901  '2901'
           2942_2  COME_FROM          2881  '2881'
             2942  POP_TOP          
           2943_0  COME_FROM          2939  '2939'

 L. 654      2943  LOAD_FAST            19  'ast'
             2946  LOAD_CONST               'stmts'
             2949  COMPARE_OP            2  ==
             2952  JUMP_IF_TRUE          7  'to 2962'
             2955  POP_TOP          
             2956  LOAD_ASSERT              AssertionError
             2959  RAISE_VARARGS_1       1  None
           2962_0  COME_FROM          2952  '2952'
             2962  POP_TOP          

 L. 656      2963  LOAD_GLOBAL          96  'find_all_globals'
             2966  LOAD_FAST            19  'ast'
             2969  LOAD_GLOBAL          97  'set'
             2972  CALL_FUNCTION_0       0  None
             2975  CALL_FUNCTION_2       2  None
             2978  STORE_FAST           39  'all_globals'

 L. 657      2981  LOAD_GLOBAL          99  'find_globals_and_nonlocals'
             2984  LOAD_FAST            19  'ast'
             2987  LOAD_GLOBAL          97  'set'
             2990  CALL_FUNCTION_0       0  None
             2993  LOAD_GLOBAL          97  'set'
             2996  CALL_FUNCTION_0       0  None
             2999  LOAD_FAST             5  'code'
             3002  LOAD_DEREF            0  'self'
             3005  LOAD_ATTR             7  'version'
             3008  CALL_FUNCTION_5       5  None
             3011  UNPACK_SEQUENCE_2     2 
             3014  STORE_FAST           13  'globals'
             3017  STORE_FAST           14  'nonlocals'

 L. 661      3020  SETUP_LOOP           53  'to 3076'
             3023  LOAD_GLOBAL         102  'sorted'
             3026  LOAD_FAST            39  'all_globals'
             3029  LOAD_DEREF            0  'self'
             3032  LOAD_ATTR           103  'mod_globs'
             3035  BINARY_AND       
             3036  LOAD_FAST            13  'globals'
             3039  BINARY_OR        
             3040  CALL_FUNCTION_1       1  None
             3043  GET_ITER         
             3044  FOR_ITER             28  'to 3075'
             3047  STORE_FAST           20  'g'

 L. 662      3050  LOAD_DEREF            0  'self'
             3053  LOAD_ATTR            92  'println'
             3056  LOAD_DEREF            0  'self'
             3059  LOAD_ATTR            95  'indent'
             3062  LOAD_CONST               'global '
             3065  LOAD_FAST            20  'g'
             3068  CALL_FUNCTION_3       3  None
             3071  POP_TOP          
             3072  JUMP_BACK          3044  'to 3044'
             3075  POP_BLOCK        
           3076_0  COME_FROM          3020  '3020'

 L. 664      3076  SETUP_LOOP           42  'to 3121'
             3079  LOAD_GLOBAL         102  'sorted'
             3082  LOAD_FAST            14  'nonlocals'
             3085  CALL_FUNCTION_1       1  None
             3088  GET_ITER         
             3089  FOR_ITER             28  'to 3120'
             3092  STORE_FAST           16  'nl'

 L. 665      3095  LOAD_DEREF            0  'self'
             3098  LOAD_ATTR            92  'println'
             3101  LOAD_DEREF            0  'self'
             3104  LOAD_ATTR            95  'indent'
             3107  LOAD_CONST               'nonlocal '
             3110  LOAD_FAST            16  'nl'
             3113  CALL_FUNCTION_3       3  None
             3116  POP_TOP          
             3117  JUMP_BACK          3089  'to 3089'
             3120  POP_BLOCK        
           3121_0  COME_FROM          3076  '3076'

 L. 667      3121  LOAD_DEREF            0  'self'
             3124  DUP_TOP          
             3125  LOAD_ATTR           103  'mod_globs'
             3128  LOAD_FAST            39  'all_globals'
             3131  INPLACE_SUBTRACT 
             3132  ROT_TWO          
             3133  STORE_ATTR          103  'mod_globs'

 L. 668      3136  LOAD_CONST               'None'
             3139  LOAD_FAST             5  'code'
             3142  LOAD_ATTR            57  'co_names'
             3145  COMPARE_OP            6  in
             3148  STORE_FAST           18  'has_none'

 L. 669      3151  LOAD_FAST            18  'has_none'
             3154  JUMP_IF_FALSE        11  'to 3168'
             3157  POP_TOP          
             3158  LOAD_GLOBAL         107  'find_none'
             3161  LOAD_FAST            19  'ast'
             3164  CALL_FUNCTION_1       1  None
             3167  UNARY_NOT        
           3168_0  COME_FROM          3154  '3154'
             3168  STORE_FAST            6  'rn'

 L. 670      3171  LOAD_DEREF            0  'self'
             3174  LOAD_ATTR           109  'gen_source'
             3177  LOAD_FAST            19  'ast'
             3180  LOAD_FAST             5  'code'
             3183  LOAD_ATTR           110  'co_name'
             3186  LOAD_FAST             8  'scanner_code'
             3189  LOAD_ATTR            56  '_customize'
             3192  LOAD_CONST               'is_lambda'
             3195  LOAD_FAST             2  'is_lambda'
             3198  LOAD_CONST               'returnNone'
             3201  LOAD_FAST             6  'rn'
             3204  CALL_FUNCTION_515   515  None
             3207  POP_TOP          

 L. 679      3208  LOAD_FAST             2  'is_lambda'
             3211  UNARY_NOT        
             3212  JUMP_IF_FALSE        95  'to 3310'
             3215  POP_TOP          
             3216  LOAD_FAST             5  'code'
             3219  LOAD_ATTR            78  'co_flags'
             3222  LOAD_GLOBAL         111  'CO_GENERATOR'
             3225  BINARY_AND       
             3226  JUMP_IF_FALSE        81  'to 3310'
           3229_0  THEN                     3311
             3229  POP_TOP          

 L. 680      3230  LOAD_GLOBAL          79  'True'
             3233  STORE_FAST           54  'need_bogus_yield'

 L. 681      3236  SETUP_LOOP           41  'to 3280'
             3239  LOAD_FAST             8  'scanner_code'
             3242  LOAD_ATTR            55  '_tokens'
             3245  GET_ITER         
             3246  FOR_ITER             30  'to 3279'
             3249  STORE_FAST           53  'token'

 L. 682      3252  LOAD_FAST            53  'token'
             3255  LOAD_CONST               ('YIELD_VALUE', 'YIELD_FROM')
             3258  COMPARE_OP            6  in
             3261  JUMP_IF_FALSE        11  'to 3275'
             3264  POP_TOP          

 L. 683      3265  LOAD_GLOBAL          76  'False'
             3268  STORE_FAST           54  'need_bogus_yield'

 L. 684      3271  BREAK_LOOP       
             3272  JUMP_BACK          3246  'to 3246'
           3275_0  COME_FROM          3261  '3261'
             3275  POP_TOP          

 L. 685      3276  JUMP_BACK          3246  'to 3246'
             3279  POP_BLOCK        
           3280_0  COME_FROM          3236  '3236'

 L. 686      3280  LOAD_FAST            54  'need_bogus_yield'
             3283  JUMP_IF_FALSE        20  'to 3306'
           3286_0  THEN                     3307
             3286  POP_TOP          

 L. 687      3287  LOAD_DEREF            0  'self'
             3290  LOAD_ATTR           114  'template_engine'
             3293  LOAD_CONST               ('%|if False:\n%+%|yield None%-',)
             3296  LOAD_FAST             1  'node'
             3299  CALL_FUNCTION_2       2  None
             3302  POP_TOP          
             3303  JUMP_ABSOLUTE      3311  'to 3311'
           3306_0  COME_FROM          3283  '3283'
             3306  POP_TOP          
             3307  JUMP_FORWARD          1  'to 3311'
           3310_0  COME_FROM          3226  '3226'
           3310_1  COME_FROM          3212  '3212'
             3310  POP_TOP          
           3311_0  COME_FROM          3307  '3307'

 L. 689      3311  LOAD_CONST               None
             3314  LOAD_FAST             8  'scanner_code'
             3317  STORE_ATTR           55  '_tokens'

 L. 690      3320  LOAD_CONST               None
             3323  LOAD_FAST             8  'scanner_code'
             3326  STORE_ATTR           56  '_customize'
             3329  LOAD_CONST               None
             3332  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 901