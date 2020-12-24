# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\failwith.py
# Compiled at: 2013-01-14 06:47:43
"""Modify a function to return a default value in case of error."""
from functools import wraps
import logging
from contextlib import contextmanager
import numpy as np

class NullHandler(logging.Handler):
    """Null handler to use as default."""

    def emit(self, record):
        pass


logger = logging.getLogger('failwith')
logger.addHandler(NullHandler())

@contextmanager
def silenced(logger, level=logging.CRITICAL):
    """
    Silence a logger for the duration of the 'with' block.
    
    >>> import sys
    >>> logger = logging.Logger("test_silenced")
    >>> logger.addHandler(logging.StreamHandler(sys.stdout))
    >>> logger.error("Error as usual.")
    Error as usual.
    >>> with silenced(logger):
    ...     logger.error("Silenced error.")
    >>> logger.error("Back to normal.")
    Back to normal.
    
    You may specify a different temporary level if you like.
    
    >>> with silenced(logger, logging.INFO):
    ...     logger.error("Breaking through the silence.")
    Breaking through the silence.
    """
    oldlevel = logger.level
    try:
        logger.setLevel(level)
        yield logger
    finally:
        logger.setLevel(oldlevel)


def nans_like--- This code section failed: ---

 L.  95         0  SETUP_EXCEPT         30  'to 33'

 L.  96         3  LOAD_GLOBAL           0  'dict'
                6  LOAD_GENEXPR             '<code_object <genexpr>>'
                9  MAKE_FUNCTION_0       0  None
               12  LOAD_FAST             0  'x'
               15  LOAD_ATTR             1  'iteritems'
               18  CALL_FUNCTION_0       0  None
               21  GET_ITER         
               22  CALL_FUNCTION_1       1  None
               25  CALL_FUNCTION_1       1  None
               28  RETURN_VALUE     
               29  POP_BLOCK        
               30  JUMP_FORWARD        194  'to 227'
             33_0  COME_FROM             0  '0'

 L.  97        33  DUP_TOP          
               34  LOAD_GLOBAL           2  'AttributeError'
               37  COMPARE_OP           10  exception-match
               40  POP_JUMP_IF_FALSE   226  'to 226'
               43  POP_TOP          
               44  POP_TOP          
               45  POP_TOP          

 L.  98        46  SETUP_EXCEPT        131  'to 180'

 L.  99        49  LOAD_GLOBAL           3  'np'
               52  LOAD_ATTR             4  'copy'
               55  LOAD_FAST             0  'x'
               58  CALL_FUNCTION_1       1  None
               61  STORE_FAST            1  'xc'

 L. 100        64  SETUP_EXCEPT         19  'to 86'

 L. 101        67  LOAD_FAST             0  'x'
               70  LOAD_ATTR             5  '__array_wrap__'
               73  LOAD_FAST             1  'xc'
               76  CALL_FUNCTION_1       1  None
               79  STORE_FAST            1  'xc'
               82  POP_BLOCK        
               83  JUMP_FORWARD         17  'to 103'
             86_0  COME_FROM            64  '64'

 L. 102        86  DUP_TOP          
               87  LOAD_GLOBAL           2  'AttributeError'
               90  COMPARE_OP           10  exception-match
               93  POP_JUMP_IF_FALSE   102  'to 102'
               96  POP_TOP          
               97  POP_TOP          
               98  POP_TOP          

 L. 103        99  JUMP_FORWARD          1  'to 103'
              102  END_FINALLY      
            103_0  COME_FROM           102  '102'
            103_1  COME_FROM            83  '83'

 L. 104       103  LOAD_CONST               'nan is only defined for float types, not %s'
              106  LOAD_FAST             1  'xc'
              109  LOAD_ATTR             6  'dtype'
              112  BINARY_MODULO    
              113  STORE_FAST            2  'msg'

 L. 105       116  LOAD_FAST             1  'xc'
              119  LOAD_ATTR             6  'dtype'
              122  LOAD_ATTR             7  'kind'
              125  LOAD_CONST               'i'
              128  COMPARE_OP            2  ==
              131  UNARY_NOT        
              132  POP_JUMP_IF_TRUE    144  'to 144'
              135  LOAD_ASSERT              AssertionError
              138  LOAD_FAST             2  'msg'
              141  RAISE_VARARGS_2       2  None

 L. 106       144  LOAD_FAST             1  'xc'
              147  LOAD_ATTR             9  'view'
              150  LOAD_GLOBAL           3  'np'
              153  LOAD_ATTR            10  'float'
              156  CALL_FUNCTION_1       1  None
              159  LOAD_ATTR            11  'fill'
              162  LOAD_GLOBAL           3  'np'
              165  LOAD_ATTR            12  'nan'
              168  CALL_FUNCTION_1       1  None
              171  POP_TOP          

 L. 107       172  LOAD_FAST             1  'xc'
              175  RETURN_VALUE     
              176  POP_BLOCK        
              177  JUMP_ABSOLUTE       227  'to 227'
            180_0  COME_FROM            46  '46'

 L. 108       180  DUP_TOP          
              181  LOAD_GLOBAL          13  'TypeError'
              184  COMPARE_OP           10  exception-match
              187  POP_JUMP_IF_FALSE   222  'to 222'
              190  POP_TOP          
              191  POP_TOP          
              192  POP_TOP          

 L. 109       193  BUILD_LIST_0          0 
              196  LOAD_FAST             0  'x'
              199  GET_ITER         
              200  FOR_ITER             18  'to 221'
              203  STORE_FAST            3  'i'
              206  LOAD_GLOBAL          14  'nans_like'
              209  LOAD_FAST             3  'i'
              212  CALL_FUNCTION_1       1  None
              215  LIST_APPEND           2  None
              218  JUMP_BACK           200  'to 200'
              221  RETURN_VALUE     
              222  END_FINALLY      
            223_0  COME_FROM           222  '222'
              223  JUMP_FORWARD          1  'to 227'
              226  END_FINALLY      
            227_0  COME_FROM           226  '226'
            227_1  COME_FROM            30  '30'

Parse error at or near `POP_BLOCK' instruction at offset 176


def failwith(default=None):
    """
    Modify a function to return a default value in case of error.
    
    >>> @failwith("Default")
    ... def f(x):
    ...     raise Exception("Failure")
    >>> f(1)
    'Default'
    
    Exceptions are logged, but the default handler doesn't do anything.
    This example adds a handler so exceptions are logged to :data:`sys.stdout`.
    
    >>> import sys
    >>> logger.addHandler(logging.StreamHandler(sys.stdout))
    >>> f(2)
    Failure in <function f at 0x...>. Default: Default. args = (2,), kwargs = {}
    Traceback (most recent call last):...
    Exception: Failure
    'Default'
    
    >>> del logger.handlers[-1] # Removing the handler added by the doctest
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception:
                msg = 'Failure in %s. Default: %s. args = %s, kwargs = %s'
                logger.exception(msg, func, default, args, kwargs)
                result = default

            return result

        return wrapper

    return decorator


def failwithnanlikefirst(func):
    """
    Like :func:`failwith`, but the default is set to `nan` + result on first evaluation.
    
    >>> @failwithnanlikefirst
    ... def f(x):
    ...     return 1.0 / x
    >>> f(1)
    1.0
    >>> f(0)
    array(nan)
    
    Exceptions are logged, but the default handler doesn't do anything.
    This example adds a handler so exceptions are logged to :data:`sys.stdout`.
    
    >>> import sys
    >>> logger.addHandler(logging.StreamHandler(sys.stdout))
    >>> f(0)
    Failure in <function f at 0x...>. Default: nan. args = (0,), kwargs = {}
    Traceback (most recent call last):...
    ZeroDivisionError: float division...
    array(nan)
    
    If the first evaluation fails, the exception is logged with an explanatory 
    note, then re-raised. 
    
    >>> @failwithnanlikefirst
    ... def g():
    ...     raise Exception("Failure")
    >>> try:
    ...     g()                         
    ... except Exception, exc:
    ...     print "Caught exception:", exc 
    <function g at 0x...> failed on first evaluation, or result could not be 
    interpreted as array of float. args = (), kwargs = {}
    Traceback (most recent call last):...Exception: Failure
    Caught exception: Failure
    """
    d = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not d:
            try:
                result = func(*args, **kwargs)
                d['default'] = nans_like(result)
            except Exception:
                msg = '%s failed on first evaluation, '
                msg += 'or result could not be interpreted as array of float. '
                msg += 'args = %s, kwargs = %s'
                logger.exception(msg, func, args, kwargs)
                raise

        else:
            try:
                result = func(*args, **kwargs)
            except Exception:
                msg = 'Failure in %s. Default: %s. args = %s, kwargs = %s'
                logger.exception(msg, func, d['default'], args, kwargs)
                result = d['default']

        return result

    return wrapper


def failwithnan_asfor(*args, **kwargs):
    """
    Like :func:`failwith`, but the default is set to `nans_like(func(*args, **kwargs))`.
    
    >>> @failwithnan_asfor(2.0, 3)
    ... def f(value, length):
    ...     return [value] * length
    >>> f()
    array([ nan,  nan,  nan])
    """

    def decorator(func):
        default = nans_like(func(*args, **kwargs))
        return failwith(default)(func)

    return decorator


def failwithdefault_asfor(*args, **kwargs):
    """
    Like :func:`failwith`, but the default is set to `func(*args, **kwargs)`.
    
    >>> @failwithdefault_asfor(2, 3)
    ... def f(value, length):
    ...     return [value] * length
    >>> f()
    [2, 2, 2]
    """

    def decorator(func):
        default = func(*args, **kwargs)
        return failwith(default)(func)

    return decorator


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)