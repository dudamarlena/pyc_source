# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/DataClayObjMethods.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 3665 bytes
""" Class description goes here. """
from decorator import decorate
import logging, six, traceback
from dataclay.commonruntime.Runtime import getRuntime
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)

def _dclayMethod--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              verbose
                4  LOAD_STR                 'Calling function %s'
                6  LOAD_FAST                'f'
                8  LOAD_ATTR                __name__
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  POP_TOP          

 L.  19        14  LOAD_GLOBAL              getRuntime
               16  CALL_FUNCTION_0       0  '0 positional arguments'
               18  LOAD_METHOD              is_exec_env
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  STORE_FAST               'is_exec_env'

 L.  20        24  SETUP_EXCEPT        100  'to 100'

 L.  21        26  LOAD_FAST                'is_exec_env'
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_FAST                'self'
               32  LOAD_METHOD              is_loaded
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  POP_JUMP_IF_TRUE     56  'to 56'
             38_0  COME_FROM            28  '28'

 L.  22        38  LOAD_FAST                'is_exec_env'
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_FAST                'self'
               44  LOAD_METHOD              is_persistent
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  POP_JUMP_IF_FALSE    56  'to 56'
             50_0  COME_FROM            40  '40'

 L.  23        50  LOAD_FAST                'f'
               52  LOAD_ATTR                _dclay_local
               54  POP_JUMP_IF_FALSE    72  'to 72'
             56_0  COME_FROM            48  '48'
             56_1  COME_FROM            36  '36'

 L.  24        56  LOAD_FAST                'f'
               58  LOAD_FAST                'self'
               60  BUILD_TUPLE_1         1 
               62  LOAD_FAST                'args'
               64  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               66  LOAD_FAST                'kwargs'
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  RETURN_VALUE     
             72_0  COME_FROM            54  '54'

 L.  26        72  LOAD_GLOBAL              getRuntime
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  LOAD_METHOD              execute_implementation_aux
               78  LOAD_FAST                'f'
               80  LOAD_ATTR                __name__
               82  LOAD_FAST                'self'
               84  LOAD_FAST                'args'
               86  LOAD_FAST                'self'
               88  LOAD_METHOD              get_hint
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  CALL_METHOD_4         4  '4 positional arguments'
               94  RETURN_VALUE     
               96  POP_BLOCK        
               98  JUMP_FORWARD        130  'to 130'
            100_0  COME_FROM_EXCEPT     24  '24'

 L.  27       100  DUP_TOP          
              102  LOAD_GLOBAL              Exception
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   128  'to 128'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L.  28       114  LOAD_GLOBAL              traceback
              116  LOAD_METHOD              print_exc
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  POP_TOP          

 L.  29       122  RAISE_VARARGS_0       0  'reraise'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           106  '106'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            98  '98'

Parse error at or near `POP_BLOCK' instruction at offset 96


def _dclayEmptyMethod(f, self, *args, **kwargs):
    """Similar to dclayMethod, but without actual Python implementation."""
    logger.verbose'Calling (languageless) function %s'f.__name__
    return getRuntime.execute_implementation_auxf.__name__selfargsself.get_hint


class dclayMethod(object):
    __doc__ = 'Class-based decorator for DataClayObject method decoration'

    def __init__(self, **kwargs):
        """Provide the argument type information

        The programmer is expected to set the same kwargs as the function,
        in addition to the `return_` special method return type.

        The typical usage is:

            @dclayMethod(a=int,
                         b='some.path.to.Class',  # this is valid (str)
                         c=imported.path.to.Class, # this is also valid
                         return_=None)
            def foo_bar(a, b, c):
                ...

        The method should be inside a DataClayObject derived class. See both
        DataClayObject class implementation and ExecutionGateway metaclass for
        more information about the internal behaviour.
        """
        self._method_args = kwargs

    def __call__(self, f):
        if six.PY2:
            logger.verbose('Preparing dataClay method `%s` with arguments: %s', f.func_name, self._method_args)
        else:
            if six.PY3:
                logger.verbose('Preparing dataClay method `%s` with arguments: %s', f.__name__, self._method_args)
        decorated_func = decorate(f, _dclayMethod)
        decorated_func._dclay_entrypoint = f
        decorated_func._dclay_ret = self._method_args.pop'return_'None
        decorated_func._dclay_args = self._method_args
        decorated_func._dclay_method = True
        is_local = self._method_args.pop'_local'False
        f._dclay_local = is_local
        decorated_func._dclay_local = is_local
        decorated_func._dclay_readonly = False
        return decorated_func


def dclayEmptyMethod(f):
    """Simple (parameter-less) decorator for languageless methods."""
    decorated_func = decorate(f, _dclayEmptyMethod)
    decorated_func._dclay_method = True
    decorated_func._dclay_readonly = False
    return decorated_func