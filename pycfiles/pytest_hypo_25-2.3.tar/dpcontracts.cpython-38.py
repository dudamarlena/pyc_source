# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\dpcontracts.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2036 bytes
"""
-----------------------
hypothesis[dpcontracts]
-----------------------

This module provides tools for working with the :pypi:`dpcontracts` library,
because `combining contracts and property-based testing works really well
<https://hillelwayne.com/talks/beyond-unit-tests/>`_.

It requires ``dpcontracts >= 0.4``.
"""
from dpcontracts import PreconditionError
from hypothesis import reject
from hypothesis.errors import InvalidArgument
from hypothesis.internal.reflection import proxies

def fulfill(contract_func):
    """Decorate ``contract_func`` to reject calls which violate preconditions,
    and retry them with different arguments.

    This is a convenience function for testing internal code that uses
    :pypi:`dpcontracts`, to automatically filter out arguments that would be
    rejected by the public interface before triggering a contract error.

    This can be used as ``builds(fulfill(func), ...)`` or in the body of the
    test e.g. ``assert fulfill(func)(*args)``.
    """
    if not hasattr(contract_func, '__contract_wrapped_func__'):
        raise InvalidArgument('There are no dpcontracts preconditions associated with %s' % (
         contract_func.__name__,))

    @proxies(contract_func)
    def inner--- This code section failed: ---

 L.  54         0  SETUP_FINALLY        14  'to 14'

 L.  55         2  LOAD_DEREF               'contract_func'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kwargs'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  56        14  DUP_TOP          
               16  LOAD_GLOBAL              PreconditionError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    38  'to 38'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  57        28  LOAD_GLOBAL              reject
               30  CALL_FUNCTION_0       0  ''
               32  POP_TOP          
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            20  '20'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

Parse error at or near `POP_TOP' instruction at offset 24

    return inner