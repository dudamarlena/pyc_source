# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/expression/expression.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 21251 bytes
import os, ast, imp, math, cmath, random
from collections import Sequence, defaultdict
from ply import lex, yacc
import mpmath
numpy = None

def check_numpy--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              numpy
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  34         8  LOAD_CONST               True
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  35        12  SETUP_FINALLY        66  'to 66'

 L.  36        14  LOAD_CONST               0
               16  LOAD_CONST               None
               18  IMPORT_NAME              numpy
               20  STORE_GLOBAL             numpy

 L.  38        22  LOAD_GLOBAL              default_funcs
               24  LOAD_METHOD              update

 L.  40        26  LOAD_GLOBAL              numpy
               28  LOAD_ATTR                transpose
               30  LOAD_GLOBAL              _render_transpose
               32  BUILD_TUPLE_2         2 

 L.  41        34  LOAD_GLOBAL              numpy
               36  LOAD_ATTR                linalg
               38  LOAD_ATTR                norm
               40  LOAD_GLOBAL              _render_norm
               42  BUILD_TUPLE_2         2 

 L.  42        44  LOAD_GLOBAL              numpy
               46  LOAD_ATTR                dot
               48  LOAD_GLOBAL              _render_dot
               50  BUILD_TUPLE_2         2 

 L.  39        52  LOAD_CONST               ('transpose', 'norm', 'dot')
               54  BUILD_CONST_KEY_MAP_3     3 

 L.  38        56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  45        60  POP_BLOCK        
               62  LOAD_CONST               True
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    12  '12'

 L.  46        66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  47        72  POP_EXCEPT       
               74  LOAD_CONST               False
               76  RETURN_VALUE     
               78  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 64


def _render_transpose(x):
    out = '\\left({%s}\\right)^T' % x[0]
    if len(x) != 1:
        return (
         out, 'transpose takes exactly one argument')
    return out


def _render_norm(x):
    out = '\\left\\|{%s}\\right\\|' % x[0]
    if len(x) != 1:
        return (
         out, 'norm takes exactly one argument')
    return out


def _render_dot(x):
    if len(x) == 0:
        return ('\\cdot', 'dot takes exactly two arguments')
    if len(x) != 2:
        return (
         '\\cdot '.join(x), 'dot takes exactly two arguments')
    return '\\left(%s\\right)\\cdot \\left(%s\\right)' % (x[0], x[1])


smallbox, _ = csm_tutor.question('smallbox')
defaults = {'csq_error_on_unknown_variable':False, 
 'csq_input_check':lambda raw, tree: None, 
 'csq_render_result':True, 
 'csq_syntax':'base', 
 'csq_num_trials':20, 
 'csq_ratio_threshold':1e-09, 
 'csq_absolute_threshold':None, 
 'csq_precision':1000, 
 'csq_soln':[
  '6', 'sqrt(2)'], 
 'csq_npoints':1, 
 'csq_msg_function':lambda sub: '', 
 'csq_show_check':False, 
 'csq_variable_dimensions':{},  'csq_names':{}}
default_names = {'pi':[
  mpmath.mpc(math.pi)], 
 'e':[
  mpmath.mpc(math.e)], 
 'j':[
  mpmath.mpc(complex(0.0, 1.0))], 
 'i':[
  mpmath.mpc(complex(0.0, 1.0))]}

def _draw_sqrt(x):
    out = '\\sqrt{%s}' % ', '.join(x)
    if len(x) != 1:
        return (
         out, 'sqrt takes exactly one argument')
    return out


def _draw_abs(x):
    out = '\\left|%s\\right|' % x[0]
    if len(x) != 1:
        return (
         out, 'abs takes exactly one argument')
    return out


def _draw_default(context, c):
    out = '%s(%s)' % (c[1], ', '.join(c[2]))
    if len(c[2]) == 1:
        if _implicit_multiplication(context):
            return (
             out, 'Assuming implicit multiplication.')
    return (
     out, 'Unknown function <tt>%s</tt>.' % c[1])


def _default_func(context, names, funcs, c):
    if _implicit_multiplication(context):
        if len(c[2]) == 1:
            val1 = eval_expr(context, names, funcs, c[1])
            val2 = eval_expr(context, names, funcs, c[2][0])
            return val1 * val2
    return random.random()


def _draw_func(name):

    def _drawer(args):
        return '%s\\left(%s\\right)' % (name, ', '.join(args))

    return _drawer


def _draw_log(x):
    if len(x) == 0:
        base = ''
    else:
        if len(x) == 1:
            base = 'e'
        else:
            base = x[1]
    if any((i in x[0] for i in ' -+')):
        arg = '\\left(%s\\right)' % x[0]
    else:
        arg = x[0]
    out = '\\log_{%s}{%s}' % (base, arg)
    if len(x) > 2:
        return (
         out, 'log takes at most 2 arguments')
    return out


default_funcs = {'atan':(
  cmath.atan, _draw_func('\\text{tan}^{-1}')), 
 'asin':(
  cmath.asin, _draw_func('\\text{sin}^{-1}')), 
 'acos':(
  cmath.acos, _draw_func('\\text{cos}^{-1}')), 
 'tan':(
  cmath.tan, _draw_func('\\text{tan}')), 
 'sin':(
  cmath.sin, _draw_func('\\text{sin}')), 
 'cos':(
  cmath.cos, _draw_func('\\text{cos}')), 
 'log':(
  cmath.log, _draw_log), 
 'sqrt':(
  cmath.sqrt, _draw_sqrt), 
 'abs':(
  abs, _draw_abs), 
 '_default':(
  _default_func, _draw_default)}

def _contains(l, test):
    if not isinstance(l, list):
        return False
    if l[0] == test:
        return True
    if l[0] == 'CALL':
        return _contains(l[1], test) or any((_contains(i, test) for i in l[2]))
    return any((_contains(i, test) for i in l[1:]))


def eval_expr(context, names, funcs, n):
    return _eval_map[n[0]](context, names, funcs, n)


def eval_name(context, names, funcs, n):
    return names[n[1]]


def eval_number(context, names, funcs, n):
    if n[1].endswith('j'):
        return mpmath.mpc(imag=(n[1][:-1]))
    return mpmath.mpf(n[1])


def check_shapes(x, y):
    xs = getattr(x, 'shape', None)
    ys = getattr(y, 'shape', None)
    if xs is not None:
        if all((i == 1 for i in xs)):
            xs = None
    if ys is not None:
        if all((i == 1 for i in ys)):
            ys = None
    if xs is not None:
        if ys is not None:
            if xs != ys:
                raise ValueError('array shapes do not match: %s and %s' % (xs, ys))


def _to_numpy(x):
    global numpy
    if check_numpy():
        if isinstance(x, numpy.ndarray):
            return x.astype(numpy.complex_)
    return x


def eval_binop(func, match_shapes=True):

    def _evaler(context, names, funcs, o):
        left = eval_expr(context, names, funcs, o[1])
        right = eval_expr(context, names, funcs, o[2])
        left = _to_numpy(left)
        right = _to_numpy(right)
        if match_shapes:
            check_shapes(left, right)
        return func(left, right)

    return _evaler


def eval_uminus(context, names, funcs, o):
    return -eval_expr(context, names, funcs, o[1])


def eval_uplus(context, names, funcs, o):
    return +eval_expr(context, names, funcs, o[1])


def eval_call(context, names, funcs, c):
    if c[1][0] == 'NAME':
        if c[1][1] in funcs:
            return (funcs[c[1][1]][0])(*(eval_expr(context, names, funcs, i) for i in c[2]))
    return funcs['_default'][0](context, names, funcs, c)


def _div(x, y):
    return x / y


_eval_map = {'NAME':eval_name, 
 'NUMBER':eval_number, 
 '+':eval_binop(lambda x, y: x + y), 
 '-':eval_binop(lambda x, y: x - y), 
 '*':eval_binop(lambda x, y: x * y), 
 '/':eval_binop(_div), 
 '@':eval_binop(lambda x, y: x @ y, match_shapes=False), 
 '^':eval_binop(lambda x, y: x ** y, match_shapes=False), 
 'u-':eval_uminus, 
 'u+':eval_uplus, 
 'CALL':eval_call}

def _run_one_test--- This code section failed: ---

 L. 259         0  LOAD_GLOBAL              _get_all_names
                2  LOAD_FAST                'sub'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               '_sub_names'

 L. 260         8  LOAD_GLOBAL              _get_all_names
               10  LOAD_FAST                'soln'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               '_sol_names'

 L. 261        16  LOAD_GLOBAL              _get_all_mappings
               18  LOAD_FAST                'context'
               20  LOAD_FAST                '_sub_names'
               22  LOAD_FAST                '_sol_names'
               24  CALL_FUNCTION_3       3  ''
               26  STORE_FAST               'maps_to_try'

 L. 262        28  LOAD_FAST                'maps_to_try'
               30  GET_ITER         
               32  FOR_ITER            252  'to 252'
               34  STORE_FAST               'm'

 L. 263        36  SETUP_FINALLY        60  'to 60'

 L. 264        38  LOAD_GLOBAL              _to_numpy
               40  LOAD_GLOBAL              eval_expr
               42  LOAD_FAST                'context'
               44  LOAD_FAST                'm'
               46  LOAD_FAST                'funcs'
               48  LOAD_FAST                'sub'
               50  CALL_FUNCTION_4       4  ''
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'subm'
               56  POP_BLOCK        
               58  JUMP_FORWARD         76  'to 76'
             60_0  COME_FROM_FINALLY    36  '36'

 L. 265        60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 266        66  POP_EXCEPT       
               68  POP_TOP          
               70  LOAD_CONST               False
               72  RETURN_VALUE     
               74  END_FINALLY      
             76_0  COME_FROM            58  '58'

 L. 267        76  LOAD_GLOBAL              _to_numpy
               78  LOAD_GLOBAL              eval_expr
               80  LOAD_FAST                'context'
               82  LOAD_FAST                'm'
               84  LOAD_FAST                'funcs'
               86  LOAD_FAST                'soln'
               88  CALL_FUNCTION_4       4  ''
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'sol'

 L. 269        94  LOAD_GLOBAL              abs
               96  STORE_FAST               'mag'

 L. 270        98  LOAD_GLOBAL              len
              100  LOAD_FAST                'context'
              102  LOAD_STR                 'csq_variable_dimensions'
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               0
              110  COMPARE_OP               >
              112  POP_JUMP_IF_FALSE   128  'to 128'
              114  LOAD_GLOBAL              check_numpy
              116  CALL_FUNCTION_0       0  ''
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 272       120  LOAD_CODE                <code_object mag>
              122  LOAD_STR                 '_run_one_test.<locals>.mag'
              124  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              126  STORE_FAST               'mag'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           112  '112'

 L. 278       128  SETUP_FINALLY       234  'to 234'

 L. 279       130  LOAD_FAST                'ratio_threshold'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
              136  STORE_FAST               'r'

 L. 280       138  LOAD_FAST                'absolute_threshold'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  STORE_FAST               'a'

 L. 281       146  LOAD_FAST                'r'
              148  POP_JUMP_IF_FALSE   170  'to 170'
              150  LOAD_FAST                'a'
              152  POP_JUMP_IF_FALSE   170  'to 170'

 L. 282       154  LOAD_GLOBAL              max
              156  LOAD_FAST                'ratio_threshold'
              158  LOAD_FAST                'sol'
              160  BINARY_MULTIPLY  
              162  LOAD_FAST                'absolute_threshold'
              164  CALL_FUNCTION_2       2  ''
              166  STORE_FAST               'threshold'
              168  JUMP_FORWARD        202  'to 202'
            170_0  COME_FROM           152  '152'
            170_1  COME_FROM           148  '148'

 L. 283       170  LOAD_FAST                'r'
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 284       174  LOAD_FAST                'ratio_threshold'
              176  LOAD_FAST                'sol'
              178  BINARY_MULTIPLY  
              180  STORE_FAST               'threshold'
              182  JUMP_FORWARD        202  'to 202'
            184_0  COME_FROM           172  '172'

 L. 285       184  LOAD_FAST                'a'
              186  POP_JUMP_IF_FALSE   194  'to 194'

 L. 286       188  LOAD_FAST                'absolute_threshold'
              190  STORE_FAST               'threshold'
              192  JUMP_FORWARD        202  'to 202'
            194_0  COME_FROM           186  '186'

 L. 288       194  POP_BLOCK        
              196  POP_TOP          
              198  LOAD_CONST               False
              200  RETURN_VALUE     
            202_0  COME_FROM           192  '192'
            202_1  COME_FROM           182  '182'
            202_2  COME_FROM           168  '168'

 L. 289       202  LOAD_FAST                'mag'
              204  LOAD_FAST                'subm'
              206  LOAD_FAST                'sol'
              208  BINARY_SUBTRACT  
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_FAST                'mag'
              214  LOAD_FAST                'threshold'
              216  CALL_FUNCTION_1       1  ''
              218  COMPARE_OP               >
              220  POP_JUMP_IF_FALSE   230  'to 230'

 L. 290       222  POP_BLOCK        
              224  POP_TOP          
              226  LOAD_CONST               False
              228  RETURN_VALUE     
            230_0  COME_FROM           220  '220'
              230  POP_BLOCK        
              232  JUMP_BACK            32  'to 32'
            234_0  COME_FROM_FINALLY   128  '128'

 L. 291       234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L. 292       240  POP_EXCEPT       
              242  POP_TOP          
              244  LOAD_CONST               False
              246  RETURN_VALUE     
              248  END_FINALLY      
              250  JUMP_BACK            32  'to 32'

 L. 294       252  LOAD_CONST               True
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 68


def _get_all_names(tree):
    if not isinstance(tree, list):
        return []
    if tree[0] == 'NAME':
        return [
         tree[1]]
    if tree[0] == 'CALL':
        return _get_all_names(tree[1]) + sum((_get_all_names(i) for i in tree[2]), [])
    return sum((_get_all_names(i) for i in tree[1:]), [])


def _get_random_value():
    return mpmath.mpf(random.uniform(1, 30))


def _fix_precision(names):
    return {mpmath.mpc(v) if isinstance(v, (float, int)) else v:k for k, v in names.items()}


def _get_all_mappings(context, soln_names, sub_names):
    names = dict(context.get('csq_default_names', default_names))
    names.update(_fix_precision(context.get('csq_names', {})))
    dimensions = context['csq_variable_dimensions']
    dim_vars = defaultdict(lambda : random.randint(2, 30))
    for n in soln_names:
        if n not in names:
            if n in dimensions:
                d = [i if isinstance(i, int) else dim_vars[i] for i in dimensions[n]]
                names[n] = (numpy.random.rand)(*d)
            else:
                names[n] = _get_random_value()
        for n in sub_names or []:
            if n not in names:
                if n in dimensions:
                    d = [i if isinstance(i, int) else dim_vars[i] for i in dimensions[n]]
                    names[n] = (numpy.random.rand)(*d)
                else:
                    names[n] = _get_random_value()
            for n in names:
                if callable(names[n]):
                    names[n] = names[n]()
                if numpy is not None and isinstance(names[n], numpy.ndarray):
                    names[n] = [
                     names[n]]
                else:
                    try:
                        names[n] = [i for i in names[n]]
                    except:
                        names[n] = [
                         names[n]]

            else:
                return _all_mappings_helper(names)


def _all_mappings_helper(m):
    lm = len(m)
    if lm == 0:
        return {}
    n = list(m.keys())[0]
    test = [{n: i} for i in m[n]]
    if lm == 1:
        return test
    c = dict(m)
    del c[n]
    o = _all_mappings_helper(c)
    out = []
    for i in o:
        for j in test:
            d = dict(i)
            d.update(j)
            out.append(d)
        else:
            return out


def total_points(**info):
    return info['csq_npoints']


def _get_syntax_module(context):
    syntax = context['csq_syntax']
    fname = os.path.join(context['cs_fs_root'], '__QTYPES__', 'expression', '__SYNTAX__', '%s.py' % syntax)
    return imp.load_source(syntax, fname)


def _implicit_multiplication(context):
    m = _get_syntax_module(context)
    if hasattr(m, 'implicit_multiplication'):
        return m.implicit_multiplication
    return True


def _get_parser(context):
    return _get_syntax_module(context).parser(lex, yacc)


def handle_submission--- This code section failed: ---

 L. 405         0  LOAD_GLOBAL              mpmath
                2  LOAD_METHOD              workdps
                4  LOAD_DEREF               'info'
                6  LOAD_STR                 'csq_precision'
                8  BINARY_SUBSCR    
               10  CALL_METHOD_1         1  ''
            12_14  SETUP_WITH          628  'to 628'
               16  POP_TOP          

 L. 407        18  LOAD_GLOBAL              len
               20  LOAD_DEREF               'info'
               22  LOAD_STR                 'csq_variable_dimensions'
               24  BINARY_SUBSCR    
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               0
               30  COMPARE_OP               >
               32  POP_JUMP_IF_FALSE    44  'to 44'

 L. 408        34  LOAD_GLOBAL              check_numpy
               36  CALL_FUNCTION_0       0  ''
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  LOAD_ASSERT              AssertionError
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'
             44_1  COME_FROM            32  '32'

 L. 410        44  LOAD_FAST                'submissions'
               46  LOAD_DEREF               'info'
               48  LOAD_STR                 'csq_name'
               50  BINARY_SUBSCR    
               52  BINARY_SUBSCR    
               54  DUP_TOP          
               56  STORE_FAST               '_sub'
               58  STORE_FAST               'sub'

 L. 411        60  LOAD_DEREF               'info'
               62  LOAD_STR                 'csq_soln'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'solns'

 L. 413        68  LOAD_GLOBAL              _get_parser
               70  LOAD_DEREF               'info'
               72  CALL_FUNCTION_1       1  ''
               74  STORE_DEREF              'parser'

 L. 415        76  LOAD_GLOBAL              dict
               78  LOAD_DEREF               'info'
               80  LOAD_METHOD              get
               82  LOAD_STR                 'csq_default_funcs'
               84  LOAD_GLOBAL              default_funcs
               86  CALL_METHOD_2         2  ''
               88  CALL_FUNCTION_1       1  ''
               90  STORE_DEREF              'funcs'

 L. 416        92  LOAD_DEREF               'funcs'
               94  LOAD_METHOD              update
               96  LOAD_DEREF               'info'
               98  LOAD_METHOD              get
              100  LOAD_STR                 'csq_funcs'
              102  BUILD_MAP_0           0 
              104  CALL_METHOD_2         2  ''
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 418       110  SETUP_FINALLY       126  'to 126'

 L. 419       112  LOAD_DEREF               'parser'
              114  LOAD_METHOD              parse
              116  LOAD_FAST                'sub'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'sub'
              122  POP_BLOCK        
              124  JUMP_FORWARD        160  'to 160'
            126_0  COME_FROM_FINALLY   110  '110'

 L. 420       126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 422       132  LOAD_CONST               False

 L. 423       134  LOAD_STR                 '<font color="red">Error: could not parse input.</font>'

 L. 421       136  LOAD_CONST               ('score', 'msg')
              138  BUILD_CONST_KEY_MAP_2     2 
              140  ROT_FOUR         
              142  POP_EXCEPT       
              144  POP_BLOCK        
              146  ROT_TWO          
              148  BEGIN_FINALLY    
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  POP_FINALLY           0  ''
              156  RETURN_VALUE     
              158  END_FINALLY      
            160_0  COME_FROM           124  '124'

 L. 425       160  LOAD_CONST               None
              162  STORE_FAST               '_m'

 L. 426       164  LOAD_FAST                'sub'
              166  LOAD_CONST               None
              168  COMPARE_OP               is
              170  POP_JUMP_IF_FALSE   180  'to 180'

 L. 427       172  LOAD_CONST               False
              174  STORE_FAST               'result'
          176_178  JUMP_FORWARD        446  'to 446'
            180_0  COME_FROM           170  '170'

 L. 429       180  LOAD_DEREF               'info'
              182  LOAD_STR                 'csq_input_check'
              184  BINARY_SUBSCR    
              186  LOAD_FAST                '_sub'
              188  LOAD_FAST                'sub'
              190  CALL_FUNCTION_2       2  ''
              192  STORE_FAST               'in_check'

 L. 430       194  LOAD_FAST                'in_check'
              196  LOAD_CONST               None
              198  COMPARE_OP               is-not
              200  POP_JUMP_IF_FALSE   212  'to 212'

 L. 431       202  LOAD_CONST               False
              204  STORE_FAST               'result'

 L. 432       206  LOAD_FAST                'in_check'
              208  STORE_FAST               '_m'
              210  JUMP_FORWARD        446  'to 446'
            212_0  COME_FROM           200  '200'

 L. 434       212  LOAD_GLOBAL              isinstance
              214  LOAD_FAST                'solns'
              216  LOAD_GLOBAL              list
              218  CALL_FUNCTION_2       2  ''
              220  POP_JUMP_IF_TRUE    228  'to 228'

 L. 435       222  LOAD_FAST                'solns'
              224  BUILD_LIST_1          1 
              226  STORE_FAST               'solns'
            228_0  COME_FROM           220  '220'

 L. 436       228  LOAD_CLOSURE             'parser'
              230  BUILD_TUPLE_1         1 
              232  LOAD_LISTCOMP            '<code_object <listcomp>>'
              234  LOAD_STR                 'handle_submission.<locals>.<listcomp>'
              236  MAKE_FUNCTION_8          'closure'
              238  LOAD_FAST                'solns'
              240  GET_ITER         
              242  CALL_FUNCTION_1       1  ''
              244  STORE_FAST               'solns'

 L. 438       246  LOAD_CONST               False
              248  STORE_FAST               'result'

 L. 439       250  LOAD_FAST                'solns'
              252  GET_ITER         
            254_0  COME_FROM           432  '432'
              254  FOR_ITER            446  'to 446'
              256  STORE_FAST               'soln'

 L. 440       258  LOAD_GLOBAL              range
              260  LOAD_DEREF               'info'
              262  LOAD_STR                 'csq_num_trials'
              264  BINARY_SUBSCR    
              266  CALL_FUNCTION_1       1  ''
              268  GET_ITER         
            270_0  COME_FROM           416  '416'
              270  FOR_ITER            430  'to 430'
              272  STORE_FAST               'attempt'

 L. 441       274  LOAD_GLOBAL              _get_all_names
              276  LOAD_FAST                'sub'
              278  CALL_FUNCTION_1       1  ''
              280  STORE_FAST               '_sub_names'

 L. 442       282  LOAD_GLOBAL              _get_all_names
              284  LOAD_FAST                'soln'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               '_sol_names'

 L. 443       290  LOAD_DEREF               'info'
              292  LOAD_STR                 'csq_error_on_unknown_variable'
              294  BINARY_SUBSCR    
          296_298  POP_JUMP_IF_FALSE   388  'to 388'

 L. 444       300  LOAD_GLOBAL              set
              302  LOAD_FAST                '_sub_names'
              304  CALL_FUNCTION_1       1  ''
              306  LOAD_METHOD              difference
              308  LOAD_FAST                '_sol_names'
              310  CALL_METHOD_1         1  ''
              312  STORE_FAST               '_unique_names'

 L. 445       314  LOAD_GLOBAL              len
              316  LOAD_FAST                '_unique_names'
              318  CALL_FUNCTION_1       1  ''
              320  LOAD_CONST               0
              322  COMPARE_OP               >
          324_326  POP_JUMP_IF_FALSE   388  'to 388'

 L. 446       328  LOAD_GLOBAL              len
              330  LOAD_FAST                '_unique_names'
              332  CALL_FUNCTION_1       1  ''
              334  LOAD_CONST               1
              336  COMPARE_OP               >
          338_340  POP_JUMP_IF_FALSE   346  'to 346'
              342  LOAD_STR                 's'
              344  JUMP_FORWARD        348  'to 348'
            346_0  COME_FROM           338  '338'
              346  LOAD_STR                 ''
            348_0  COME_FROM           344  '344'
              348  STORE_FAST               '_s'

 L. 447       350  LOAD_STR                 ', '
              352  LOAD_METHOD              join
              354  LOAD_CLOSURE             'funcs'
              356  LOAD_CLOSURE             'info'
              358  BUILD_TUPLE_2         2 
              360  LOAD_GENEXPR             '<code_object <genexpr>>'
              362  LOAD_STR                 'handle_submission.<locals>.<genexpr>'
              364  MAKE_FUNCTION_8          'closure'

 L. 449       366  LOAD_FAST                '_unique_names'

 L. 447       368  GET_ITER         
              370  CALL_FUNCTION_1       1  ''
              372  CALL_METHOD_1         1  ''
              374  STORE_FAST               '_v'

 L. 451       376  LOAD_STR                 'Unknown variable%s: $%s$'
              378  LOAD_FAST                '_s'
              380  LOAD_FAST                '_v'
              382  BUILD_TUPLE_2         2 
              384  BINARY_MODULO    
              386  STORE_FAST               '_m'
            388_0  COME_FROM           324  '324'
            388_1  COME_FROM           296  '296'

 L. 452       388  LOAD_GLOBAL              _run_one_test

 L. 453       390  LOAD_DEREF               'info'

 L. 454       392  LOAD_FAST                'sub'

 L. 455       394  LOAD_FAST                'soln'

 L. 456       396  LOAD_DEREF               'funcs'

 L. 457       398  LOAD_DEREF               'info'
              400  LOAD_STR                 'csq_ratio_threshold'
              402  BINARY_SUBSCR    

 L. 458       404  LOAD_DEREF               'info'
              406  LOAD_STR                 'csq_absolute_threshold'
              408  BINARY_SUBSCR    

 L. 452       410  CALL_FUNCTION_6       6  ''
              412  STORE_FAST               'result'

 L. 460       414  LOAD_FAST                'result'
          416_418  POP_JUMP_IF_TRUE    270  'to 270'

 L. 461       420  POP_TOP          
          422_424  BREAK_LOOP          430  'to 430'
          426_428  JUMP_BACK           270  'to 270'

 L. 462       430  LOAD_FAST                'result'
          432_434  POP_JUMP_IF_FALSE   254  'to 254'

 L. 463       436  POP_TOP          
          438_440  BREAK_LOOP          446  'to 446'
          442_444  JUMP_BACK           254  'to 254'
            446_0  COME_FROM           210  '210'
            446_1  COME_FROM           176  '176'

 L. 465       446  LOAD_DEREF               'info'
              448  LOAD_STR                 'csq_show_check'
              450  BINARY_SUBSCR    
          452_454  POP_JUMP_IF_FALSE   490  'to 490'

 L. 466       456  LOAD_FAST                'result'
          458_460  POP_JUMP_IF_FALSE   476  'to 476'

 L. 467       462  LOAD_STR                 '<img src="%s" />'
              464  LOAD_DEREF               'info'
              466  LOAD_STR                 'cs_check_image'
              468  BINARY_SUBSCR    
              470  BINARY_MODULO    
              472  STORE_FAST               'msg'
              474  JUMP_FORWARD        488  'to 488'
            476_0  COME_FROM           458  '458'

 L. 469       476  LOAD_STR                 '<img src="%s" />'
              478  LOAD_DEREF               'info'
              480  LOAD_STR                 'cs_cross_image'
              482  BINARY_SUBSCR    
              484  BINARY_MODULO    
              486  STORE_FAST               'msg'
            488_0  COME_FROM           474  '474'
              488  JUMP_FORWARD        494  'to 494'
            490_0  COME_FROM           452  '452'

 L. 471       490  LOAD_STR                 ''
              492  STORE_FAST               'msg'
            494_0  COME_FROM           488  '488'

 L. 472       494  LOAD_DEREF               'info'
              496  LOAD_STR                 'csq_name'
              498  BINARY_SUBSCR    
              500  STORE_FAST               'n'

 L. 473       502  LOAD_FAST                'msg'
              504  LOAD_DEREF               'info'
              506  LOAD_STR                 'csq_msg_function'
              508  BINARY_SUBSCR    
              510  LOAD_FAST                'submissions'
              512  LOAD_DEREF               'info'
              514  LOAD_STR                 'csq_name'
              516  BINARY_SUBSCR    
              518  BINARY_SUBSCR    
              520  CALL_FUNCTION_1       1  ''
              522  INPLACE_ADD      
              524  STORE_FAST               'msg'

 L. 474       526  LOAD_DEREF               'info'
              528  LOAD_STR                 'csm_language'
              530  BINARY_SUBSCR    
              532  LOAD_METHOD              source_transform_string
              534  LOAD_DEREF               'info'
              536  LOAD_FAST                'msg'
              538  CALL_METHOD_2         2  ''
              540  STORE_FAST               'msg'

 L. 476       542  LOAD_STR                 '\n<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ndocument.getElementById("image%s").innerHTML = %r;\n// @license-end\n</script>'

 L. 481       544  LOAD_FAST                'n'
              546  LOAD_FAST                'msg'
              548  BUILD_TUPLE_2         2 

 L. 475       550  BINARY_MODULO    
              552  STORE_FAST               'msg'

 L. 482       554  LOAD_DEREF               'info'
              556  LOAD_STR                 'csq_render_result'
              558  BINARY_SUBSCR    
          560_562  POP_JUMP_IF_FALSE   592  'to 592'

 L. 483       564  LOAD_FAST                'msg'
              566  LOAD_GLOBAL              get_display
              568  LOAD_DEREF               'info'
              570  LOAD_FAST                'n'
              572  LOAD_FAST                'sub'
              574  LOAD_CONST               False
              576  LOAD_FAST                '_m'
          578_580  JUMP_IF_TRUE_OR_POP   584  'to 584'
              582  LOAD_STR                 ''
            584_0  COME_FROM           578  '578'
              584  CALL_FUNCTION_5       5  ''
              586  INPLACE_ADD      
              588  STORE_FAST               'msg'
              590  JUMP_FORWARD        606  'to 606'
            592_0  COME_FROM           560  '560'

 L. 485       592  LOAD_FAST                'msg'
              594  LOAD_FAST                '_m'
          596_598  JUMP_IF_TRUE_OR_POP   602  'to 602'
              600  LOAD_STR                 ''
            602_0  COME_FROM           596  '596'
              602  INPLACE_ADD      
              604  STORE_FAST               'msg'
            606_0  COME_FROM           590  '590'

 L. 486       606  LOAD_FAST                'result'
              608  LOAD_FAST                'msg'
              610  LOAD_CONST               ('score', 'msg')
              612  BUILD_CONST_KEY_MAP_2     2 
              614  POP_BLOCK        
              616  ROT_TWO          
              618  BEGIN_FINALLY    
              620  WITH_CLEANUP_START
              622  WITH_CLEANUP_FINISH
              624  POP_FINALLY           0  ''
              626  RETURN_VALUE     
            628_0  COME_FROM_WITH       12  '12'
              628  WITH_CLEANUP_START
              630  WITH_CLEANUP_FINISH
              632  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 144


checktext = 'Check Syntax'

def handle_check(submission, **info):
    if len(info['csq_variable_dimensions']) > 0:
        assert check_numpy()
    last = submission.get(info['csq_name'])
    return get_display(info, info['csq_name'], last)


def render_html(last_log, **info):
    if len(info['csq_variable_dimensions']) > 0:
        if not check_numpy():
            return '<font color="red">Error: the <tt>numpy</tt> module is required for nonscalar values'
    name = info['csq_name']
    out = (smallbox['render_html'])(last_log, **info)
    out += "\n<span id='image%s'></span>" % (name,)
    return out


def get_display(info, name, last, reparse=True, extra_msg=''):
    try:
        if reparse:
            parser = _get_parser(info)
            tree = parser.parse(last)
        else:
            tree = last
        funcs = dict(default_funcs)
        funcs.update(info.get('csq_funcs', {}))
        last = '<displaymath>%s</displaymath>' % tree2tex(info, funcs, tree)[0]
    except:
        last = '<font color="red">ERROR: Could not interpret your input</font>'
    else:
        last += csm_language.source_transform_string(info, extra_msg)
        out = '<div id="expr%s">Your entry was parsed as:<br/>%s</div>' % (name, last)
        out += '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ncatsoop.render_all_math(document.getElementById("expr%s"), true);\n// @license-end\n</script>' % name
        return out


def answer_display(**info):
    if len(info['csq_variable_dimensions']) > 0:
        if not check_numpy():
            return '<font color="red">Error: the <tt>numpy</tt> module is required for nonscalar values'
    else:
        parser = _get_parser(info)
        funcs = dict(default_funcs)
        funcs.update(info.get('csq_funcs', {}))
        if isinstance(info['csq_soln'], str):
            a = tree2tex(info, funcs, parser.parse(info['csq_soln']))[0]
            out = '<p>Solution: <tt>%s</tt><br><div id="%s_soln"><displaymath>%s</displaymath></div><p>' % (
             info['csq_soln'], info['csq_name'], a)
        else:
            out = '<p><div id="%s_soln"><b>Multiple Possible Solutions:</b>' % info['csq_name']
        count = 1
        for i in info['csq_soln']:
            out += '<hr width="80%" />'
            a = tree2tex(info, funcs, parser.parse(i))[0]
            out += '<p>Solution %s: <tt>%s</tt><br><displaymath>%s</displaymath></p>' % (
             count, i, a)
            count += 1
        else:
            out += '</div>'

    out += '<script type="text/javascript">\n// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3\ncatsoop.render_all_math(document.getElementById("%s_soln"), true);\n// @license-end\n</script>' % info['csq_name']
    return out


GREEK_LETTERS = [
 'alpha',
 'beta',
 'gamma',
 'delta',
 'epsilon',
 'zeta',
 'eta',
 'theta',
 'iota',
 'kappa',
 'lambda',
 'mu',
 'nu',
 'xi',
 'omicron',
 'pi',
 'rho',
 'sigma',
 'tau',
 'upsilon',
 'phi',
 'chi',
 'psi',
 'omega']
GREEK_DICT = {}
for i in GREEK_LETTERS:
    GREEK_DICT[i] = '\\%s' % i
    GREEK_DICT[i.upper()] = '\\%s' % i.title()
else:

    def name2tex(context, funcs, n):
        prec = 5
        on = n = n[1]
        s = None
        if '_' in n:
            n, s = n.split('_')
        if n in GREEK_DICT:
            n = GREEK_DICT[n]
        if on in context['csq_variable_dimensions']:
            n = '\\mathbf{%s}' % n
        if s is not None:
            if s in GREEK_DICT:
                s = GREEK_DICT[s]
            return (
             '%s_{%s}' % (n, s), prec)
        return (
         n, prec)


    def plus2tex(context, funcs, n):
        prec = 1
        left, lprec = tree2tex(context, funcs, n[1])
        right, rprec = tree2tex(context, funcs, n[2])
        return ('%s + %s' % (left, right), prec)


    def minus2tex(context, funcs, n):
        prec = 1
        left, lprec = tree2tex(context, funcs, n[1])
        right, rprec = tree2tex(context, funcs, n[2])
        if rprec <= prec:
            right = '\\left(%s\\right)' % right
        return (
         '%s - %s' % (left, right), prec)


    def div2tex(context, funcs, n):
        prec = 2
        left, lprec = tree2tex(context, funcs, n[1])
        right, rprec = tree2tex(context, funcs, n[2])
        return ('\\frac{%s}{%s}' % (left, right), prec)


    def times2tex(context, funcs, n):
        prec = 2
        left, lprec = tree2tex(context, funcs, n[1])
        if lprec < prec:
            left = '\\left(%s\\right)' % left
        right, rprec = tree2tex(context, funcs, n[2])
        if rprec < prec:
            right = '\\left(%s\\right)' % right
        return (
         '%s \\times %s' % (left, right), prec)


    def matmul2tex(context, funcs, n):
        prec = 2
        left, lprec = tree2tex(context, funcs, n[1])
        if lprec < prec:
            left = '\\left(%s\\right)' % left
        right, rprec = tree2tex(context, funcs, n[2])
        if rprec < prec:
            right = '\\left(%s\\right)' % right
        return (
         '%s%s' % (left, right), prec)


    def exp2tex(context, funcs, n):
        prec = 4
        left, lprec = tree2tex(context, funcs, n[1])
        if lprec <= prec:
            left = '\\left(%s\\right)' % left
        right, rprec = tree2tex(context, funcs, n[2])
        return ('%s ^ {%s}' % (left, right), prec)


    def uminus2tex(context, funcs, n):
        prec = 3
        operand, oprec = tree2tex(context, funcs, n[1])
        if oprec < prec:
            operand = '\\left(%s\\right)' % operand
        return (
         '-%s' % operand, prec)


    def uplus2tex(context, funcs, n):
        prec = 3
        operand, oprec = tree2tex(context, funcs, n[1])
        if oprec < prec:
            operand = '\\left(%s\\right)' % operand
        return (
         '+%s' % operand, prec)


    def call2tex(context, funcs, c):
        prec = 6
        if c[1][0] == 'NAME':
            if c[1][1] in funcs:
                o = funcs[c[1][1]][1]([tree2tex(context, funcs, i)[0] for i in c[2]])
            else:
                new_c = list(c)
                new_c[1] = tree2tex(context, funcs, c[1])[0]
                new_c[2] = [tree2tex(context, funcs, i)[0] for i in c[2]]
                o = funcs['_default'][1](context, new_c)
            if isinstance(o, str):
                pass
        elif isinstance(o, Sequence):
            if len(o) > 1:
                o = '{\\color{red} \\underbrace{%s}_{\\text{%s}}}' % tuple(o[:2])
        return (
         o, prec)


    def _opt_clear_dec_part(x):
        n = x.split('.', 1)
        if len(n) == 1 or all((i == '0' for i in n[1])):
            return n[0]
        return '.'.join(n)


    def number2tex(context, funcs, x):
        n = x[1].lower()
        if n.endswith('j'):
            imag = True
            n = n[:-1]
        else:
            imag = False
        if 'e' in n:
            o = [
             '%s\\times 10^{%s}' % tuple(n.split('e')), 22]
        else:
            o = [
             n, 5]
        if imag:
            o[0] += 'j'
        return tuple(o)


    _tree_map = {'NAME':name2tex, 
     'NUMBER':number2tex, 
     '+':plus2tex, 
     '-':minus2tex, 
     '*':times2tex, 
     '/':div2tex, 
     '^':exp2tex, 
     '@':matmul2tex, 
     'u-':uminus2tex, 
     'u+':uplus2tex, 
     'CALL':call2tex}

    def tree2tex(context, funcs, tree):
        return _tree_map[tree[0]](context, funcs, tree)