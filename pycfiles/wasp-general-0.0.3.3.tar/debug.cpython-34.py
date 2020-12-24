# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/debug.py
# Compiled at: 2017-04-24 15:00:28
# Size of source mod 2**32: 3154 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_type
from wasp_general.network.web.proto import WWebRequestProto, WWebResponseProto, WWebTargetRouteProto

class WWebDebugInfo(metaclass=ABCMeta):
    __doc__ = ' This is API prototype for web-service debugging process\n\t'

    @abstractmethod
    def session_id(self):
        """ Create new token, that is used for session identification

                :return: any type
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(request=WWebRequestProto, protocol_version=str, protocol=str)
    def request(self, session_id, request, protocol_version, protocol):
        """ Dump client request

                :param session_id: session origin
                :param request: client request
                :param protocol_version: client protocol version (like 0.9/1.0/1.1/2)
                :param protocol: client protocol (like http/https)
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(response=WWebResponseProto)
    def response(self, session_id, response):
        """ Dump server response to client

                :param session_id: session origin
                :param response: server response
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(target_route=(WWebTargetRouteProto, None))
    def target_route(self, session_id, target_route):
        """ Dump target route

                :param session_id: session origin
                :param target_route: target route
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(exc=Exception)
    def exception(self, session_id, exc):
        """ Dump raised exception (may be called more then once)

                :param session_id: session origin
                :param exc: raised exception
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def finalize(self, session_id):
        """ Client session finalization. This method is called whenever exceptions were risen or not

                :param session_id: session origin
                :return: None
                """
        raise NotImplementedError('This method is abstract')