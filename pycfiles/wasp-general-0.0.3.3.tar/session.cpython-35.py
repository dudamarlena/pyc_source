# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
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
    def read_request_line(self, request_line):
        """ Read HTTP-request line

                :param request_line: line to parse
                        for HTTP/0.9 is GET <Request-URI>
                        for HTTP/1.0 and 1.1 is <METHOD> <Request-URI> HTTP/<HTTP-Version>, where HTTP-Version is 1.0
                        or 1.1.
                        for HTTP/2: binary headers are used
                """
        request = self._WWebSessionBase__request_cls.parse_request_line(self, request_line)
        protocol_version = self.protocol_version()
        if protocol_version == '0.9':
            if request.method() != 'GET':
                raise Exception('HTTP/0.9 standard violation')
        else:
            if protocol_version == '1.0' or protocol_version == '1.1':
                pass
            else:
                if protocol_version == '2':
                    pass
                else:
                    raise RuntimeError('Unsupported HTTP-protocol')