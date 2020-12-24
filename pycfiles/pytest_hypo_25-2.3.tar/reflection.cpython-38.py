# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\reflection.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 19781 bytes
"""This file can approximately be considered the collection of hypothesis going
to really unreasonable lengths to produce pretty output."""
import ast, hashlib, inspect, re, types
from functools import wraps
from tokenize import detect_encoding
from types import ModuleType
from typing import TypeVar
from hypothesis.internal.compat import qualname, str_to_bytes, to_unicode, update_code_location
import hypothesis.vendor.pretty as pretty
C = TypeVar('C', bound=callable)

def fully_qualified_name(f):
    """Returns a unique identifier for f pointing to the module it was defined
    on, and an containing functions."""
    if f.__module__ is not None:
        return f.__module__ + '.' + qualname(f)
    return qualname(f)


def is_mock(obj):
    """Determine if the given argument is a mock type."""
    return hasattr(obj, 'hypothesis_internal_is_this_a_mock_check')


def function_digest(function):
    """Returns a string that is stable across multiple invocations across
    multiple processes and is prone to changing significantly in response to
    minor changes to the function.

    No guarantee of uniqueness though it usually will be.
    """
    hasher = hashlib.sha384()
    try:
        hasher.update(to_unicode(inspect.getsource(function)).encode('utf-8'))
    except (OSError, TypeError):
        pass

    try:
        hasher.update(str_to_bytes(function.__name__))
    except AttributeError:
        pass

    try:
        hasher.update(function.__module__.__name__.encode('utf-8'))
    except AttributeError:
        pass

    try:
        hasher.update(str_to_bytes(repr(inspect.getfullargspec(function))))
    except TypeError:
        pass
    else:
        try:
            hasher.update(function._hypothesis_internal_add_digest)
        except AttributeError:
            pass
        else:
            return hasher.digest()


def is_typed_named_tuple(cls):
    """Return True if cls is probably a subtype of `typing.NamedTuple`.

    Unfortunately types created with `class T(NamedTuple):` actually
    subclass `tuple` directly rather than NamedTuple.  This is annoying,
    and means we just have to hope that nobody defines a different tuple
    subclass with similar attributes.
    """
    return issubclass(cls, tuple) and hasattr(cls, '_fields') and hasattr(cls, '_field_types')


def required_args(target, args=(), kwargs=()):
    """Return a set of names of required args to target that were not supplied
    in args or kwargs.

    This is used in builds() to determine which arguments to attempt to
    fill from type hints.  target may be any callable (including classes
    and bound methods).  args and kwargs should be as they are passed to
    builds() - that is, a tuple of values and a dict of names: values.
    """
    if inspect.isclass(target):
        if is_typed_named_tuple(target):
            provided = set(kwargs) | set(target._fields[:len(args)])
            return set(target._fields) - provided
    try:
        spec = inspect.getfullargspec(getattr(target, '__init__', target) if inspect.isclass(target) else target)
    except TypeError:
        return
    else:
        skip_self = int(inspect.isclass(target) or inspect.ismethod(target))
        return set(spec.args[skip_self + len(args):] + spec.kwonlyargs) - set(spec.args[len(spec.args) - len(spec.defaults or ()):]) - set(spec.kwonlydefaults or ()) - set(kwargs)


def convert_keyword_arguments(function, args, kwargs):
    """Returns a pair of a tuple and a dictionary which would be equivalent
    passed as positional and keyword args to the function. Unless function has.

    **kwargs the dictionary will always be empty.
    """
    argspec = inspect.getfullargspec(function)
    new_args = []
    kwargs = dict(kwargs)
    defaults = dict(argspec.kwonlydefaults or {})
    if argspec.defaults:
        for name, value in zip(argspec.args[-len(argspec.defaults):], argspec.defaults):
            defaults[name] = value

    n = max(len(args), len(argspec.args))
    for i in range(n):
        if i < len(args):
            new_args.append(args[i])
        else:
            arg_name = argspec.args[i]
            if arg_name in kwargs:
                new_args.append(kwargs.pop(arg_name))
            elif arg_name in defaults:
                new_args.append(defaults[arg_name])
            else:
                raise TypeError('No value provided for argument %r' % arg_name)
    else:
        if kwargs:
            if not argspec.varkw:
                if not argspec.kwonlyargs:
                    if len(kwargs) > 1:
                        raise TypeError('%s() got unexpected keyword arguments %s' % (
                         function.__name__, ', '.join(map(repr, kwargs))))
                    else:
                        bad_kwarg = next(iter(kwargs))
                        raise TypeError('%s() got an unexpected keyword argument %r' % (
                         function.__name__, bad_kwarg))
        return (
         tuple(new_args), kwargs)


def convert_positional_arguments(function, args, kwargs):
    """Return a tuple (new_args, new_kwargs) where all possible arguments have
    been moved to kwargs.

    new_args will only be non-empty if function has a variadic argument.
    """
    argspec = inspect.getfullargspec(function)
    new_kwargs = dict(argspec.kwonlydefaults or {})
    new_kwargs.update(kwargs)
    if not argspec.varkw:
        for k in new_kwargs.keys():
            if k not in argspec.args and k not in argspec.kwonlyargs:
                raise TypeError('%s() got an unexpected keyword argument %r' % (
                 function.__name__, k))

    if len(args) < len(argspec.args):
        for i in range(len(args), len(argspec.args) - len(argspec.defaults or ())):
            if argspec.args[i] not in kwargs:
                raise TypeError('No value provided for argument %s' % (argspec.args[i],))

    for kw in argspec.kwonlyargs:
        if kw not in new_kwargs:
            raise TypeError('No value provided for argument %s' % kw)
    else:
        if len(args) > len(argspec.args) and not argspec.varargs:
            raise TypeError('%s() takes at most %d positional arguments (%d given)' % (
             function.__name__, len(argspec.args), len(args)))

    for arg, name in zip(args, argspec.args):
        if name in new_kwargs:
            raise TypeError('%s() got multiple values for keyword argument %r' % (
             function.__name__, name))
        else:
            new_kwargs[name] = arg
    else:
        return (
         tuple(args[len(argspec.args):]), new_kwargs)


def extract_all_lambdas(tree):
    lambdas = []

    class Visitor(ast.NodeVisitor):

        def visit_Lambda(self, node):
            lambdas.append(node)

    Visitor().visit(tree)
    return lambdas


def args_for_lambda_ast(l):
    return [n.arg for n in l.args.args]


LINE_CONTINUATION = re.compile('\\\\\\n')
WHITESPACE = re.compile('\\s+')
PROBABLY_A_COMMENT = re.compile('#[^\'"]*$')
SPACE_FOLLOWS_OPEN_BRACKET = re.compile('\\( ')
SPACE_PRECEDES_CLOSE_BRACKET = re.compile(' \\)')

def extract_lambda_source--- This code section failed: ---

 L. 261         0  LOAD_GLOBAL              inspect
                2  LOAD_METHOD              getfullargspec
                4  LOAD_FAST                'f'
                6  CALL_METHOD_1         1  ''
                8  STORE_DEREF              'argspec'

 L. 262        10  BUILD_LIST_0          0 
               12  STORE_FAST               'arg_strings'

 L. 263        14  LOAD_DEREF               'argspec'
               16  LOAD_ATTR                args
               18  GET_ITER         
               20  FOR_ITER             50  'to 50'
               22  STORE_FAST               'a'

 L. 264        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'a'
               28  LOAD_GLOBAL              str
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  LOAD_ASSERT              AssertionError
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L. 265        38  LOAD_FAST                'arg_strings'
               40  LOAD_METHOD              append
               42  LOAD_FAST                'a'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_BACK            20  'to 20'

 L. 266        50  LOAD_DEREF               'argspec'
               52  LOAD_ATTR                varargs
               54  POP_JUMP_IF_FALSE    74  'to 74'

 L. 267        56  LOAD_FAST                'arg_strings'
               58  LOAD_METHOD              append
               60  LOAD_STR                 '*'
               62  LOAD_DEREF               'argspec'
               64  LOAD_ATTR                varargs
               66  BINARY_ADD       
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  JUMP_FORWARD         90  'to 90'
             74_0  COME_FROM            54  '54'

 L. 268        74  LOAD_DEREF               'argspec'
               76  LOAD_ATTR                kwonlyargs
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L. 269        80  LOAD_FAST                'arg_strings'
               82  LOAD_METHOD              append
               84  LOAD_STR                 '*'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            78  '78'
             90_1  COME_FROM            72  '72'

 L. 270        90  LOAD_DEREF               'argspec'
               92  LOAD_ATTR                kwonlyargs
               94  JUMP_IF_TRUE_OR_POP    98  'to 98'
               96  BUILD_LIST_0          0 
             98_0  COME_FROM            94  '94'
               98  GET_ITER         
              100  FOR_ITER            156  'to 156'
              102  STORE_FAST               'a'

 L. 271       104  LOAD_DEREF               'argspec'
              106  LOAD_ATTR                kwonlydefaults
              108  JUMP_IF_TRUE_OR_POP   112  'to 112'
              110  BUILD_MAP_0           0 
            112_0  COME_FROM           108  '108'
              112  LOAD_METHOD              get
              114  LOAD_FAST                'a'
              116  CALL_METHOD_1         1  ''
              118  STORE_FAST               'default'

 L. 272       120  LOAD_FAST                'default'
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L. 273       124  LOAD_FAST                'arg_strings'
              126  LOAD_METHOD              append
              128  LOAD_STR                 '{}={}'
              130  LOAD_METHOD              format
              132  LOAD_FAST                'a'
              134  LOAD_FAST                'default'
              136  CALL_METHOD_2         2  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK           100  'to 100'
            144_0  COME_FROM           122  '122'

 L. 275       144  LOAD_FAST                'arg_strings'
              146  LOAD_METHOD              append
              148  LOAD_FAST                'a'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_BACK           100  'to 100'

 L. 277       156  LOAD_FAST                'arg_strings'
              158  POP_JUMP_IF_FALSE   178  'to 178'

 L. 278       160  LOAD_STR                 'lambda %s: <unknown>'
              162  LOAD_STR                 ', '
              164  LOAD_METHOD              join
              166  LOAD_FAST                'arg_strings'
              168  CALL_METHOD_1         1  ''
              170  BUILD_TUPLE_1         1 
              172  BINARY_MODULO    
              174  STORE_FAST               'if_confused'
              176  JUMP_FORWARD        182  'to 182'
            178_0  COME_FROM           158  '158'

 L. 280       178  LOAD_STR                 'lambda: <unknown>'
              180  STORE_FAST               'if_confused'
            182_0  COME_FROM           176  '176'

 L. 281       182  SETUP_FINALLY       198  'to 198'

 L. 282       184  LOAD_GLOBAL              inspect
              186  LOAD_METHOD              getsource
              188  LOAD_FAST                'f'
              190  CALL_METHOD_1         1  ''
              192  STORE_FAST               'source'
              194  POP_BLOCK        
              196  JUMP_FORWARD        222  'to 222'
            198_0  COME_FROM_FINALLY   182  '182'

 L. 283       198  DUP_TOP          
              200  LOAD_GLOBAL              OSError
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   220  'to 220'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L. 284       212  LOAD_FAST                'if_confused'
              214  ROT_FOUR         
              216  POP_EXCEPT       
              218  RETURN_VALUE     
            220_0  COME_FROM           204  '204'
              220  END_FINALLY      
            222_0  COME_FROM           196  '196'

 L. 286       222  LOAD_GLOBAL              LINE_CONTINUATION
              224  LOAD_METHOD              sub
              226  LOAD_STR                 ' '
              228  LOAD_FAST                'source'
              230  CALL_METHOD_2         2  ''
              232  STORE_FAST               'source'

 L. 287       234  LOAD_GLOBAL              WHITESPACE
              236  LOAD_METHOD              sub
              238  LOAD_STR                 ' '
              240  LOAD_FAST                'source'
              242  CALL_METHOD_2         2  ''
              244  STORE_FAST               'source'

 L. 288       246  LOAD_FAST                'source'
              248  LOAD_METHOD              strip
              250  CALL_METHOD_0         0  ''
              252  STORE_FAST               'source'

 L. 289       254  LOAD_STR                 'lambda'
              256  LOAD_FAST                'source'
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_TRUE    268  'to 268'
              264  LOAD_ASSERT              AssertionError
              266  RAISE_VARARGS_1       1  'exception instance'
            268_0  COME_FROM           260  '260'

 L. 291       268  LOAD_CONST               None
              270  STORE_FAST               'tree'

 L. 293       272  SETUP_FINALLY       288  'to 288'

 L. 294       274  LOAD_GLOBAL              ast
              276  LOAD_METHOD              parse
              278  LOAD_FAST                'source'
              280  CALL_METHOD_1         1  ''
              282  STORE_FAST               'tree'
              284  POP_BLOCK        
              286  JUMP_FORWARD        426  'to 426'
            288_0  COME_FROM_FINALLY   272  '272'

 L. 295       288  DUP_TOP          
              290  LOAD_GLOBAL              SyntaxError
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   424  'to 424'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L. 296       304  LOAD_GLOBAL              range
              306  LOAD_GLOBAL              len
              308  LOAD_FAST                'source'
              310  CALL_FUNCTION_1       1  ''
              312  LOAD_CONST               1
              314  BINARY_SUBTRACT  
              316  LOAD_GLOBAL              len
              318  LOAD_STR                 'lambda'
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_CONST               -1
              324  CALL_FUNCTION_3       3  ''
              326  GET_ITER         
              328  FOR_ITER            420  'to 420'
              330  STORE_FAST               'i'

 L. 297       332  LOAD_FAST                'source'
              334  LOAD_CONST               None
              336  LOAD_FAST                'i'
              338  BUILD_SLICE_2         2 
              340  BINARY_SUBSCR    
              342  STORE_FAST               'prefix'

 L. 298       344  LOAD_STR                 'lambda'
              346  LOAD_FAST                'prefix'
              348  COMPARE_OP               not-in
          350_352  POP_JUMP_IF_FALSE   360  'to 360'

 L. 299       354  POP_TOP          
          356_358  BREAK_LOOP          420  'to 420'
            360_0  COME_FROM           350  '350'

 L. 300       360  SETUP_FINALLY       388  'to 388'

 L. 301       362  LOAD_GLOBAL              ast
              364  LOAD_METHOD              parse
              366  LOAD_FAST                'prefix'
              368  CALL_METHOD_1         1  ''
              370  STORE_FAST               'tree'

 L. 302       372  LOAD_FAST                'prefix'
              374  STORE_FAST               'source'

 L. 303       376  POP_BLOCK        
              378  POP_TOP          
          380_382  BREAK_LOOP          420  'to 420'
              384  POP_BLOCK        
              386  JUMP_BACK           328  'to 328'
            388_0  COME_FROM_FINALLY   360  '360'

 L. 304       388  DUP_TOP          
              390  LOAD_GLOBAL              SyntaxError
              392  COMPARE_OP               exception-match
          394_396  POP_JUMP_IF_FALSE   414  'to 414'
              398  POP_TOP          
              400  POP_TOP          
              402  POP_TOP          

 L. 305       404  POP_EXCEPT       
          406_408  JUMP_BACK           328  'to 328'
              410  POP_EXCEPT       
              412  JUMP_BACK           328  'to 328'
            414_0  COME_FROM           394  '394'
              414  END_FINALLY      
          416_418  JUMP_BACK           328  'to 328'
              420  POP_EXCEPT       
              422  JUMP_FORWARD        426  'to 426'
            424_0  COME_FROM           294  '294'
              424  END_FINALLY      
            426_0  COME_FROM           422  '422'
            426_1  COME_FROM           286  '286'

 L. 306       426  LOAD_FAST                'tree'
              428  LOAD_CONST               None
              430  COMPARE_OP               is
          432_434  POP_JUMP_IF_FALSE   544  'to 544'

 L. 307       436  LOAD_FAST                'source'
              438  LOAD_METHOD              startswith
              440  LOAD_STR                 '@'
              442  CALL_METHOD_1         1  ''
          444_446  POP_JUMP_IF_FALSE   544  'to 544'

 L. 313       448  LOAD_GLOBAL              range
              450  LOAD_GLOBAL              len
              452  LOAD_FAST                'source'
              454  CALL_FUNCTION_1       1  ''
              456  LOAD_CONST               1
              458  BINARY_ADD       
              460  CALL_FUNCTION_1       1  ''
              462  GET_ITER         
            464_0  COME_FROM           486  '486'
              464  FOR_ITER            544  'to 544'
              466  STORE_FAST               'i'

 L. 314       468  LOAD_FAST                'source'
              470  LOAD_CONST               1
              472  LOAD_FAST                'i'
              474  BUILD_SLICE_2         2 
              476  BINARY_SUBSCR    
              478  STORE_FAST               'p'

 L. 315       480  LOAD_STR                 'lambda'
              482  LOAD_FAST                'p'
              484  COMPARE_OP               in
          486_488  POP_JUMP_IF_FALSE   464  'to 464'

 L. 316       490  SETUP_FINALLY       518  'to 518'

 L. 317       492  LOAD_GLOBAL              ast
              494  LOAD_METHOD              parse
              496  LOAD_FAST                'p'
              498  CALL_METHOD_1         1  ''
              500  STORE_FAST               'tree'

 L. 318       502  LOAD_FAST                'p'
              504  STORE_FAST               'source'

 L. 319       506  POP_BLOCK        
              508  POP_TOP          
          510_512  JUMP_ABSOLUTE       544  'to 544'
              514  POP_BLOCK        
              516  JUMP_BACK           464  'to 464'
            518_0  COME_FROM_FINALLY   490  '490'

 L. 320       518  DUP_TOP          
              520  LOAD_GLOBAL              SyntaxError
              522  COMPARE_OP               exception-match
          524_526  POP_JUMP_IF_FALSE   538  'to 538'
              528  POP_TOP          
              530  POP_TOP          
              532  POP_TOP          

 L. 321       534  POP_EXCEPT       
              536  JUMP_BACK           464  'to 464'
            538_0  COME_FROM           524  '524'
              538  END_FINALLY      
          540_542  JUMP_BACK           464  'to 464'
            544_0  COME_FROM           444  '444'
            544_1  COME_FROM           432  '432'

 L. 323       544  LOAD_FAST                'tree'
              546  LOAD_CONST               None
              548  COMPARE_OP               is
          550_552  POP_JUMP_IF_FALSE   558  'to 558'

 L. 324       554  LOAD_FAST                'if_confused'
              556  RETURN_VALUE     
            558_0  COME_FROM           550  '550'

 L. 326       558  LOAD_GLOBAL              extract_all_lambdas
              560  LOAD_FAST                'tree'
              562  CALL_FUNCTION_1       1  ''
              564  STORE_FAST               'all_lambdas'

 L. 327       566  LOAD_CLOSURE             'argspec'
              568  BUILD_TUPLE_1         1 
              570  LOAD_LISTCOMP            '<code_object <listcomp>>'
              572  LOAD_STR                 'extract_lambda_source.<locals>.<listcomp>'
              574  MAKE_FUNCTION_8          'closure'
              576  LOAD_FAST                'all_lambdas'
              578  GET_ITER         
              580  CALL_FUNCTION_1       1  ''
              582  STORE_FAST               'aligned_lambdas'

 L. 328       584  LOAD_GLOBAL              len
              586  LOAD_FAST                'aligned_lambdas'
              588  CALL_FUNCTION_1       1  ''
              590  LOAD_CONST               1
              592  COMPARE_OP               !=
          594_596  POP_JUMP_IF_FALSE   602  'to 602'

 L. 329       598  LOAD_FAST                'if_confused'
              600  RETURN_VALUE     
            602_0  COME_FROM           594  '594'

 L. 330       602  LOAD_FAST                'aligned_lambdas'
              604  LOAD_CONST               0
              606  BINARY_SUBSCR    
              608  STORE_FAST               'lambda_ast'

 L. 331       610  LOAD_FAST                'lambda_ast'
              612  LOAD_ATTR                lineno
              614  LOAD_CONST               1
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_TRUE    626  'to 626'
              622  LOAD_ASSERT              AssertionError
              624  RAISE_VARARGS_1       1  'exception instance'
            626_0  COME_FROM           618  '618'

 L. 350       626  SETUP_FINALLY       712  'to 712'

 L. 351       628  LOAD_GLOBAL              open
              630  LOAD_GLOBAL              inspect
              632  LOAD_METHOD              getsourcefile
              634  LOAD_FAST                'f'
              636  CALL_METHOD_1         1  ''
              638  LOAD_STR                 'rb'
              640  CALL_FUNCTION_2       2  ''
              642  SETUP_WITH          664  'to 664'
              644  STORE_FAST               'src_f'

 L. 352       646  LOAD_GLOBAL              detect_encoding
              648  LOAD_FAST                'src_f'
              650  LOAD_ATTR                readline
              652  CALL_FUNCTION_1       1  ''
              654  UNPACK_SEQUENCE_2     2 
              656  STORE_FAST               'encoding'
              658  STORE_FAST               '_'
              660  POP_BLOCK        
              662  BEGIN_FINALLY    
            664_0  COME_FROM_WITH      642  '642'
              664  WITH_CLEANUP_START
              666  WITH_CLEANUP_FINISH
              668  END_FINALLY      

 L. 354       670  LOAD_FAST                'source'
              672  LOAD_METHOD              encode
              674  LOAD_FAST                'encoding'
              676  CALL_METHOD_1         1  ''
              678  STORE_FAST               'source_bytes'

 L. 355       680  LOAD_FAST                'source_bytes'
              682  LOAD_FAST                'lambda_ast'
              684  LOAD_ATTR                col_offset
              686  LOAD_CONST               None
              688  BUILD_SLICE_2         2 
              690  BINARY_SUBSCR    
              692  LOAD_METHOD              strip
              694  CALL_METHOD_0         0  ''
              696  STORE_FAST               'source_bytes'

 L. 356       698  LOAD_FAST                'source_bytes'
              700  LOAD_METHOD              decode
              702  LOAD_FAST                'encoding'
              704  CALL_METHOD_1         1  ''
              706  STORE_FAST               'source'
              708  POP_BLOCK        
              710  JUMP_FORWARD        756  'to 756'
            712_0  COME_FROM_FINALLY   626  '626'

 L. 357       712  DUP_TOP          
              714  LOAD_GLOBAL              OSError
              716  LOAD_GLOBAL              TypeError
              718  BUILD_TUPLE_2         2 
              720  COMPARE_OP               exception-match
          722_724  POP_JUMP_IF_FALSE   754  'to 754'
              726  POP_TOP          
              728  POP_TOP          
              730  POP_TOP          

 L. 358       732  LOAD_FAST                'source'
              734  LOAD_FAST                'lambda_ast'
              736  LOAD_ATTR                col_offset
              738  LOAD_CONST               None
              740  BUILD_SLICE_2         2 
              742  BINARY_SUBSCR    
              744  LOAD_METHOD              strip
              746  CALL_METHOD_0         0  ''
              748  STORE_FAST               'source'
              750  POP_EXCEPT       
              752  JUMP_FORWARD        756  'to 756'
            754_0  COME_FROM           722  '722'
              754  END_FINALLY      
            756_0  COME_FROM           752  '752'
            756_1  COME_FROM           710  '710'

 L. 370       756  SETUP_FINALLY       780  'to 780'

 L. 371       758  LOAD_FAST                'source'
              760  LOAD_FAST                'source'
              762  LOAD_METHOD              index
              764  LOAD_STR                 'lambda'
              766  CALL_METHOD_1         1  ''
              768  LOAD_CONST               None
              770  BUILD_SLICE_2         2 
              772  BINARY_SUBSCR    
              774  STORE_FAST               'source'
              776  POP_BLOCK        
              778  JUMP_FORWARD        806  'to 806'
            780_0  COME_FROM_FINALLY   756  '756'

 L. 372       780  DUP_TOP          
              782  LOAD_GLOBAL              ValueError
              784  COMPARE_OP               exception-match
          786_788  POP_JUMP_IF_FALSE   804  'to 804'
              790  POP_TOP          
              792  POP_TOP          
              794  POP_TOP          

 L. 373       796  LOAD_FAST                'if_confused'
              798  ROT_FOUR         
              800  POP_EXCEPT       
              802  RETURN_VALUE     
            804_0  COME_FROM           786  '786'
              804  END_FINALLY      
            806_0  COME_FROM           778  '778'

 L. 375       806  LOAD_GLOBAL              range
              808  LOAD_GLOBAL              len
              810  LOAD_FAST                'source'
              812  CALL_FUNCTION_1       1  ''
              814  LOAD_GLOBAL              len
              816  LOAD_STR                 'lambda'
              818  CALL_FUNCTION_1       1  ''
              820  LOAD_CONST               -1
              822  CALL_FUNCTION_3       3  ''
              824  GET_ITER         
              826  FOR_ITER            954  'to 954'
              828  STORE_FAST               'i'

 L. 376       830  SETUP_FINALLY       928  'to 928'

 L. 377       832  LOAD_GLOBAL              ast
              834  LOAD_METHOD              parse
              836  LOAD_FAST                'source'
              838  LOAD_CONST               None
              840  LOAD_FAST                'i'
              842  BUILD_SLICE_2         2 
              844  BINARY_SUBSCR    
              846  CALL_METHOD_1         1  ''
              848  STORE_FAST               'parsed'

 L. 378       850  LOAD_GLOBAL              len
              852  LOAD_FAST                'parsed'
              854  LOAD_ATTR                body
              856  CALL_FUNCTION_1       1  ''
              858  LOAD_CONST               1
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_TRUE    870  'to 870'
              866  LOAD_ASSERT              AssertionError
              868  RAISE_VARARGS_1       1  'exception instance'
            870_0  COME_FROM           862  '862'

 L. 379       870  LOAD_FAST                'parsed'
              872  LOAD_ATTR                body
          874_876  POP_JUMP_IF_TRUE    882  'to 882'
              878  LOAD_ASSERT              AssertionError
              880  RAISE_VARARGS_1       1  'exception instance'
            882_0  COME_FROM           874  '874'

 L. 380       882  LOAD_GLOBAL              isinstance
              884  LOAD_FAST                'parsed'
              886  LOAD_ATTR                body
              888  LOAD_CONST               0
              890  BINARY_SUBSCR    
              892  LOAD_ATTR                value
              894  LOAD_GLOBAL              ast
              896  LOAD_ATTR                Lambda
              898  CALL_FUNCTION_2       2  ''
          900_902  POP_JUMP_IF_FALSE   924  'to 924'

 L. 381       904  LOAD_FAST                'source'
              906  LOAD_CONST               None
              908  LOAD_FAST                'i'
              910  BUILD_SLICE_2         2 
              912  BINARY_SUBSCR    
              914  STORE_FAST               'source'

 L. 382       916  POP_BLOCK        
              918  POP_TOP          
          920_922  BREAK_LOOP          954  'to 954'
            924_0  COME_FROM           900  '900'
              924  POP_BLOCK        
              926  JUMP_BACK           826  'to 826'
            928_0  COME_FROM_FINALLY   830  '830'

 L. 383       928  DUP_TOP          
              930  LOAD_GLOBAL              SyntaxError
              932  COMPARE_OP               exception-match
          934_936  POP_JUMP_IF_FALSE   948  'to 948'
              938  POP_TOP          
              940  POP_TOP          
              942  POP_TOP          

 L. 384       944  POP_EXCEPT       
              946  JUMP_BACK           826  'to 826'
            948_0  COME_FROM           934  '934'
              948  END_FINALLY      
          950_952  JUMP_BACK           826  'to 826'

 L. 385       954  LOAD_FAST                'source'
              956  LOAD_METHOD              split
              958  LOAD_STR                 '\n'
              960  CALL_METHOD_1         1  ''
              962  STORE_FAST               'lines'

 L. 386       964  LOAD_LISTCOMP            '<code_object <listcomp>>'
              966  LOAD_STR                 'extract_lambda_source.<locals>.<listcomp>'
              968  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              970  LOAD_FAST                'lines'
              972  GET_ITER         
              974  CALL_FUNCTION_1       1  ''
              976  STORE_FAST               'lines'

 L. 387       978  LOAD_STR                 '\n'
              980  LOAD_METHOD              join
              982  LOAD_FAST                'lines'
              984  CALL_METHOD_1         1  ''
              986  STORE_FAST               'source'

 L. 389       988  LOAD_GLOBAL              WHITESPACE
              990  LOAD_METHOD              sub
              992  LOAD_STR                 ' '
              994  LOAD_FAST                'source'
              996  CALL_METHOD_2         2  ''
              998  STORE_FAST               'source'

 L. 390      1000  LOAD_GLOBAL              SPACE_FOLLOWS_OPEN_BRACKET
             1002  LOAD_METHOD              sub
             1004  LOAD_STR                 '('
             1006  LOAD_FAST                'source'
             1008  CALL_METHOD_2         2  ''
             1010  STORE_FAST               'source'

 L. 391      1012  LOAD_GLOBAL              SPACE_PRECEDES_CLOSE_BRACKET
             1014  LOAD_METHOD              sub
             1016  LOAD_STR                 ')'
             1018  LOAD_FAST                'source'
             1020  CALL_METHOD_2         2  ''
             1022  STORE_FAST               'source'

 L. 392      1024  LOAD_FAST                'source'
             1026  LOAD_METHOD              strip
             1028  CALL_METHOD_0         0  ''
             1030  STORE_FAST               'source'

 L. 393      1032  LOAD_FAST                'source'
             1034  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 410


def get_pretty_function_description(f):
    if not hasattr(f, '__name__'):
        return repr(f)
        name = f.__name__
        if name == '<lambda>':
            return extract_lambda_source(f)
    elif isinstance(f, types.MethodType):
        self = f.__self__
        if not self is None:
            if not inspect.isclass(self):
                return '%r.%s' % (self, name)
    return name


def nicerepr(v):
    if inspect.isfunction(v):
        return get_pretty_function_description(v)
    if isinstance(v, type):
        return v.__name__
    return pretty(v)


def arg_string(f, args, kwargs, reorder=True):
    if reorder:
        args, kwargs = convert_positional_arguments(f, args, kwargs)
    argspec = inspect.getfullargspec(f)
    bits = []
    for a in argspec.args:
        if a in kwargs:
            bits.append('%s=%s' % (a, nicerepr(kwargs.pop(a))))
        if kwargs:
            for a in sorted(kwargs):
                bits.append('%s=%s' % (a, nicerepr(kwargs[a])))

        else:
            return ', '.join([nicerepr(x) for x in args] + bits)


def unbind_method(f):
    """Take something that might be a method or a function and return the
    underlying function."""
    return getattr(f, 'im_func', getattr(f, '__func__', f))


def check_valid_identifier(identifier):
    if not identifier.isidentifier():
        raise ValueError('%r is not a valid python identifier' % (identifier,))


eval_cache = {}

def source_exec_as_module--- This code section failed: ---

 L. 451         0  SETUP_FINALLY        12  'to 12'

 L. 452         2  LOAD_GLOBAL              eval_cache
                4  LOAD_FAST                'source'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 453        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 454        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L. 456        32  LOAD_GLOBAL              ModuleType

 L. 457        34  LOAD_STR                 'hypothesis_temporary_module_%s'

 L. 458        36  LOAD_GLOBAL              hashlib
               38  LOAD_METHOD              sha384
               40  LOAD_GLOBAL              str_to_bytes
               42  LOAD_FAST                'source'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_METHOD_1         1  ''
               48  LOAD_METHOD              hexdigest
               50  CALL_METHOD_0         0  ''
               52  BUILD_TUPLE_1         1 

 L. 457        54  BINARY_MODULO    

 L. 456        56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'result'

 L. 460        60  LOAD_GLOBAL              isinstance
               62  LOAD_FAST                'source'
               64  LOAD_GLOBAL              str
               66  CALL_FUNCTION_2       2  ''
               68  POP_JUMP_IF_TRUE     74  'to 74'
               70  LOAD_ASSERT              AssertionError
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            68  '68'

 L. 461        74  LOAD_GLOBAL              exec
               76  LOAD_FAST                'source'
               78  LOAD_FAST                'result'
               80  LOAD_ATTR                __dict__
               82  CALL_FUNCTION_2       2  ''
               84  POP_TOP          

 L. 462        86  LOAD_FAST                'result'
               88  LOAD_GLOBAL              eval_cache
               90  LOAD_FAST                'source'
               92  STORE_SUBSCR     

 L. 463        94  LOAD_FAST                'result'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22


COPY_ARGSPEC_SCRIPT = '\nfrom hypothesis.utils.conventions import not_set\n\ndef accept(%(funcname)s):\n    def %(name)s(%(argspec)s):\n        return %(funcname)s(%(invocation)s)\n    return %(name)s\n'.lstrip()

def define_function_signature(name, docstring, argspec):
    """A decorator which sets the name, argspec and docstring of the function
    passed into it."""
    check_valid_identifier(name)
    for a in argspec.args:
        check_valid_identifier(a)
    else:
        if argspec.varargs is not None:
            check_valid_identifier(argspec.varargs)
        else:
            if argspec.varkw is not None:
                check_valid_identifier(argspec.varkw)
            n_defaults = len(argspec.defaults or ())
            if n_defaults:
                parts = []
                for a in argspec.args[:-n_defaults]:
                    parts.append(a)
                else:
                    for a in argspec.args[-n_defaults:]:
                        parts.append('%s=not_set' % (a,))

            else:
                parts = list(argspec.args)
        used_names = list(argspec.args) + list(argspec.kwonlyargs)
        used_names.append(name)
        for a in argspec.kwonlyargs:
            check_valid_identifier(a)
        else:

            def accept(f):
                fargspec = inspect.getfullargspec(f)
                must_pass_as_kwargs = []
                invocation_parts = []
                for a in argspec.args:
                    if a not in fargspec.args:
                        fargspec.varargs or must_pass_as_kwargs.append(a)
                    else:
                        invocation_parts.append(a)

                if argspec.varargs:
                    used_names.append(argspec.varargs)
                    parts.append('*' + argspec.varargs)
                    invocation_parts.append('*' + argspec.varargs)
                else:
                    if argspec.kwonlyargs:
                        parts.append('*')
                    else:
                        for k in must_pass_as_kwargs:
                            invocation_parts.append('%(k)s=%(k)s' % {'k': k})
                        else:
                            for k in argspec.kwonlyargs:
                                invocation_parts.append('%(k)s=%(k)s' % {'k': k})
                                if k in (argspec.kwonlydefaults or []):
                                    parts.append('%(k)s=not_set' % {'k': k})
                                else:
                                    parts.append(k)
                            else:
                                if argspec.varkw:
                                    used_names.append(argspec.varkw)
                                    parts.append('**' + argspec.varkw)
                                    invocation_parts.append('**' + argspec.varkw)
                                candidate_names = ['f'] + ['f_%d' % (i,) for i in range(1, len(used_names) + 2)]
                                for funcname in candidate_names:
                                    if funcname not in used_names:
                                        break
                                    base_accept = source_exec_as_module(COPY_ARGSPEC_SCRIPT % {'name':name, 
                                     'funcname':funcname, 
                                     'argspec':', '.join(parts), 
                                     'invocation':', '.join(invocation_parts)}).accept
                                    result = base_accept(f)
                                    result.__doc__ = docstring
                                    result.__defaults__ = argspec.defaults
                                    if argspec.kwonlydefaults:
                                        result.__kwdefaults__ = argspec.kwonlydefaults

                    if argspec.annotations:
                        result.__annotations__ = argspec.annotations
                    return result

            return accept


def impersonate(target):
    """Decorator to update the attributes of a function so that to external
    introspectors it will appear to be the target function.

    Note that this updates the function in place, it doesn't return a
    new one.
    """

    def accept(f):
        f.__code__ = update_code_location(f.__code__, target.__code__.co_filename, target.__code__.co_firstlineno)
        f.__name__ = target.__name__
        f.__module__ = target.__module__
        f.__doc__ = target.__doc__
        f.__globals__['__hypothesistracebackhide__'] = True
        return f

    return accept


def proxies(target):

    def accept(proxy):
        return impersonate(target)(wraps(target)(define_function_signature(target.__name__.replace'<lambda>''_lambda_', target.__doc__, inspect.getfullargspec(target))(proxy)))

    return accept