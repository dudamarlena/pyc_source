# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\compat.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 5871 bytes
import codecs, importlib, inspect, platform, sys, time, typing
PYPY = platform.python_implementation() == 'PyPy'
CAN_PACK_HALF_FLOAT = sys.version_info[:2] >= (3, 6)
WINDOWS = platform.system() == 'Windows'

def bit_length(n):
    return n.bit_length()


def str_to_bytes(s):
    return s.encode(a_good_encoding())


def escape_unicode_characters(s):
    return codecs.encode(s, 'unicode_escape').decode('ascii')


def int_from_bytes(data):
    return int.from_bytes(data, 'big')


def int_to_bytes(i, size):
    return i.to_bytes(size, 'big')


def int_to_byte(i):
    return bytes([i])


def benchmark_time():
    return time.monotonic()


def a_good_encoding():
    return 'utf-8'


def to_unicode(x):
    if isinstance(x, str):
        return x
    return x.decode(a_good_encoding())


def qualname--- This code section failed: ---

 L.  69         0  SETUP_FINALLY        10  'to 10'

 L.  70         2  LOAD_FAST                'f'
                4  LOAD_ATTR                __qualname__
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L.  71        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    34  'to 34'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  72        24  LOAD_FAST                'f'
               26  LOAD_ATTR                __name__
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
             34_0  COME_FROM            16  '16'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 20


try:
    typing_root_type = (
     typing._Final, typing._GenericAlias)
    ForwardRef = typing.ForwardRef
except AttributeError:
    typing_root_type = (
     typing.TypingMeta, typing.TypeVar)
    try:
        typing_root_type += (typing._Union,)
    except AttributeError:
        pass
    else:
        ForwardRef = typing._ForwardRef
else:
    if sys.version_info[:2] < (3, 6):

        def get_type_hints--- This code section failed: ---

 L.  94         0  SETUP_FINALLY        38  'to 38'

 L.  95         2  LOAD_GLOBAL              inspect
                4  LOAD_METHOD              getfullargspec
                6  LOAD_FAST                'thing'
                8  CALL_METHOD_1         1  ''
               10  STORE_DEREF              'spec'

 L.  96        12  LOAD_CLOSURE             'spec'
               14  BUILD_TUPLE_1         1 
               16  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               18  LOAD_STR                 'get_type_hints.<locals>.<dictcomp>'
               20  MAKE_FUNCTION_8          'closure'

 L.  98        22  LOAD_DEREF               'spec'
               24  LOAD_ATTR                annotations
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''

 L.  96        30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L. 101        38  DUP_TOP          
               40  LOAD_GLOBAL              TypeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 102        52  BUILD_MAP_0           0 
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            44  '44'
               60  END_FINALLY      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 16


    else:

        def get_type_hints--- This code section failed: ---

 L. 108         0  SETUP_FINALLY        14  'to 14'

 L. 109         2  LOAD_GLOBAL              typing
                4  LOAD_METHOD              get_type_hints
                6  LOAD_FAST                'thing'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 110        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    36  'to 36'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 111        28  BUILD_MAP_0           0 
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


    importlib_invalidate_caches = getattr(importlib, 'invalidate_caches', lambda : ())

    def update_code_location(code, newfile, newlineno):
        """Take a code object and lie shamelessly about where it comes from.

    Why do we want to do this? It's for really shallow reasons involving
    hiding the hypothesis_temporary_module code from test runners like
    pytest's verbose mode. This is a vastly disproportionate terrible
    hack that I've done purely for vanity, and if you're reading this
    code you're probably here because it's broken something and now
    you're angry at me. Sorry.
    """
        if hasattr(code, 'replace'):
            return code.replace(co_filename=newfile, co_firstlineno=newlineno)
        CODE_FIELD_ORDER = [
         'co_argcount',
         'co_kwonlyargcount',
         'co_nlocals',
         'co_stacksize',
         'co_flags',
         'co_code',
         'co_consts',
         'co_names',
         'co_varnames',
         'co_filename',
         'co_name',
         'co_firstlineno',
         'co_lnotab',
         'co_freevars',
         'co_cellvars']
        unpacked = [getattr(code, name) for name in CODE_FIELD_ORDER]
        unpacked[CODE_FIELD_ORDER.index('co_filename')] = newfile
        unpacked[CODE_FIELD_ORDER.index('co_firstlineno')] = newlineno
        return (type(code))(*unpacked)


    def cast_unicode(s, encoding=None):
        if isinstance(s, bytes):
            return s.decode(encoding or a_good_encoding(), 'replace')
        return s


    def get_stream_enc(stream, default=None):
        return getattr(stream, 'encoding', None) or default


    def floor(x):
        y = int(x)
        if y != x:
            if x < 0:
                return y - 1
        return y


    def ceil(x):
        y = int(x)
        if y != x:
            if x > 0:
                return y + 1
        return y


try:
    from django.test import TransactionTestCase

    def bad_django_TestCase(runner):
        if runner is None:
            return False
        else:
            return isinstance(runner, TransactionTestCase) or False
        from hypothesis.extra.django._impl import HypothesisTestCase
        return not isinstance(runner, HypothesisTestCase)


except Exception:

    def bad_django_TestCase(runner):
        return False