# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/session.py
# Compiled at: 2017-04-24 15:00:28
# Size of source mod 2**32: 2941 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_subclass, verify_type
from wasp_general.network.primitives import WIPV4SocketInfo
from wasp_general.network.web.proto import WWebSessionProto, WWebResponseProto
from wasp_general.network.web.request import WWebRequest

class WWebSessionAdapter(WWebSessionProto):

    def client_address(self):
        return WIPV4SocketInfo(*self.accepted_socket().getpeername())

    def server_address(self):
        return WIPV4SocketInfo(*self.accepted_socket().getsockname())

    @abstractmethod
    def accepted_socket(self):
        raise NotImplementedError('This method is abstract')


class WWebSessionBase(WWebSessionAdapter, metaclass=ABCMeta):
    __doc__ = ' Basic :class:`.WWebSessionProto` implementation. This class clarifies prototype and appends several methods\n\t'

    @verify_subclass(request_cls=WWebRequest)
    def __init__(self, request_cls=WWebRequest):
        """ Construct class

                :param request_cls: request class to use
                """
        self._WWebSessionBase__request_cls = request_cls

    @verify_type(request_line=str)
    def read_request_line--- This code section failed: ---

 L.  77         0  LOAD_FAST                'self'
                3  LOAD_ATTR                _WWebSessionBase__request_cls
                6  LOAD_ATTR                parse_request_line
                9  LOAD_FAST                'self'
               12  LOAD_FAST                'request_line'
               15  CALL_FUNCTION_2       2  '2 positional, 0 named'
               18  STORE_FAST               'request'

 L.  79        21  LOAD_FAST                'self'
               24  LOAD_ATTR                protocol_version
               27  CALL_FUNCTION_0       0  '0 positional, 0 named'
               30  STORE_FAST               'protocol_version'

 L.  80        33  LOAD_FAST                'protocol_version'
               36  LOAD_STR                 '0.9'
               39  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    81  'to 81'

 L.  81        45  LOAD_FAST                'request'
               48  LOAD_ATTR                method
               51  CALL_FUNCTION_0       0  '0 positional, 0 named'
               54  LOAD_STR                 'GET'
               57  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE   135  'to 135'

 L.  82        63  LOAD_GLOBAL              Exception
               66  LOAD_STR                 'HTTP/0.9 standard violation'
               69  CALL_FUNCTION_1       1  '1 positional, 0 named'
               72  RAISE_VARARGS_1       1  'exception'
               75  JUMP_ABSOLUTE       135  'to 135'
               78  JUMP_FORWARD        135  'to 135'
               81  ELSE                     '135'

 L.  83        81  LOAD_FAST                'protocol_version'
               84  LOAD_STR                 '1.0'
               87  COMPARE_OP               ==
               90  POP_JUMP_IF_TRUE    135  'to 135'
               93  LOAD_FAST                'protocol_version'
               96  LOAD_STR                 '1.1'
               99  COMPARE_OP               ==
            102_0  COME_FROM            90  '90'
              102  POP_JUMP_IF_FALSE   108  'to 108'

 L.  84       105  JUMP_FORWARD        135  'to 135'
              108  ELSE                     '135'

 L.  85       108  LOAD_FAST                'protocol_version'
              111  LOAD_STR                 '2'
              114  COMPARE_OP               ==
              117  POP_JUMP_IF_FALSE   123  'to 123'

 L.  86       120  JUMP_FORWARD        135  'to 135'
              123  ELSE                     '135'

 L.  88       123  LOAD_GLOBAL              RuntimeError
              126  LOAD_STR                 'Unsupported HTTP-protocol'
              129  CALL_FUNCTION_1       1  '1 positional, 0 named'
              132  RAISE_VARARGS_1       1  'exception'
            135_0  COME_FROM           120  '120'
            135_1  COME_FROM           105  '105'
            135_2  COME_FROM            78  '78'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 102