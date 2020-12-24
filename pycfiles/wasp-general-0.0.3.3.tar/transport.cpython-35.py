# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/transport.py
# Compiled at: 2018-03-06 15:22:10
# Size of source mod 2**32: 11828 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
import socket, struct
from wasp_general.verify import verify_type, verify_value
from wasp_general.config import WConfig
from wasp_general.network.primitives import WIPV4SocketInfo, WIPV4Address, WNetworkIPV4

class WNetworkNativeTransportProto(metaclass=ABCMeta):
    __doc__ = ' This is interface for classes, that implement transport logic for network communication. "Native" means\n\tthat these classes use socket objects directly.\n\n\tTODO: remove this!\n\t'

    @abstractmethod
    @verify_type(config=WConfig)
    def server_socket(self, config):
        """ Return server socket. This socket is used for receiving requests and sending results. It is
                important, that the result can be polled by a IOLoop instance.

                :param config: server configuration
                :return: socket.socket
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(config=WConfig, close_fd=bool)
    def close_server_socket(self, config, close_fd=True):
        """ Close previously opened server socket. If no socket is opened - do nothing.

                :param config: server configuration
                :param close_fd: should this function close socket fd, or will it close by an external function?. It            is safer to pass True here.
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(config=WConfig)
    def client_socket(self, config):
        """ Return client socket. This socket is used for sending request and receiving results. It is
                important, that the result can be polled by a IOLoop instance.

                :param config: client configuration
                :return: socket.socket
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(config=WConfig, close_fd=bool)
    def close_client_socket(self, config, close_fd=True):
        """ Close previously opened client socket. If no socket is opened - do nothing.

                :param config: client configuration
                :param close_fd: should this function close socket fd, or will it close by an external function?. It            is safer to pass True here.
                :return: None
                """
        raise NotImplementedError('This method is abstract')

    @verify_type(config=WConfig)
    def target_socket(self, config):
        """ Return socket information with server address. Mostly used for address validation.

                :param config: client configuration
                :return: WIPV4SocketInfo
                """
        raise NotImplementedError('This method is abstract')

    @verify_type(config=WConfig)
    def bind_socket(self, config):
        """ Return socket information with address that server binds to.

                :param config: server configuration
                :return: WIPV4SocketInfo
                """
        raise NotImplementedError('This method is abstract')


class WNetworkNativeTransportSocketConfig:
    __doc__ = ' Represent socket configuration settings.\n\n\tTODO: remove this!\n\t'

    @verify_type(section=str, address_option=str, port_option=str)
    @verify_value(section=lambda x: len(x) > 0, address_option=lambda x: len(x) > 0, port_option=lambda x: len(x) > 0)
    def __init__(self, section, address_option, port_option):
        """ Construct new configuration settings

                :param section: section name
                :param address_option: address option name
                :param port_option: port option name
                """
        self.section = section
        self.address_option = address_option
        self.port_option = port_option


class WNetworkNativeTransport(WNetworkNativeTransportProto, metaclass=ABCMeta):
    __doc__ = " Basic WNetworkNativeTransportProto implementation. This class isn't ready to use, but it has general\n\timplementation for the most WNetworkNativeTransportProto methods.\n\n\tTODO: refactor this!\n\t"

    @verify_type(target_socket_config=WNetworkNativeTransportSocketConfig)
    @verify_type(bind_socket_config=WNetworkNativeTransportSocketConfig)
    def __init__(self, target_socket_config, bind_socket_config):
        """ Create new transport

                :param target_socket_config: configuration for client socket
                :param bind_socket_config: configuration for server socket
                """
        self._WNetworkNativeTransport__target_socket_config = target_socket_config
        self._WNetworkNativeTransport__bind_socket_config = bind_socket_config
        self._WNetworkNativeTransport__server_socket = None
        self._WNetworkNativeTransport__client_socket = None

    @verify_type(config=WConfig)
    def target_socket(self, config):
        """ :meth:`.WNetworkNativeTransportProto.server_socket` method implementation
                """
        address = config[self._WNetworkNativeTransport__target_socket_config.section][self._WNetworkNativeTransport__target_socket_config.address_option]
        port = config.getint(self._WNetworkNativeTransport__target_socket_config.section, self._WNetworkNativeTransport__target_socket_config.port_option)
        target = WIPV4SocketInfo(address, port)
        if target.address() is None or target.port() is None:
            raise ValueError('Invalid target address or port')
        return target

    @verify_type(config=WConfig)
    def bind_socket(self, config):
        """ :meth:`.WNetworkNativeTransportProto.bind_socket` method implementation
                """
        address = config[self._WNetworkNativeTransport__bind_socket_config.section][self._WNetworkNativeTransport__bind_socket_config.address_option]
        port = config.getint(self._WNetworkNativeTransport__bind_socket_config.section, self._WNetworkNativeTransport__bind_socket_config.port_option)
        return WIPV4SocketInfo(address, port)

    @abstractmethod
    def _create_socket(self):
        """ Create general socket object, that can be used for client and/or server usage

                :return: socket.socket
                """
        raise NotImplementedError('This method is abstract')

    @verify_type(config=WConfig)
    def create_server_socket(self, config):
        """ Create socket for server. (By default, same as WNetworkNativeTransport._create_socket)

                :param config: server configuration
                :return: socket.socket
                """
        return self._create_socket()

    @verify_type(config=WConfig)
    def create_client_socket(self, config):
        """ Create socket for client. (By default, same as WNetworkNativeTransport._create_socket)

                :param config: client configuration
                :return: socket.socket
                """
        return self._create_socket()

    @verify_type(config=WConfig)
    def server_socket(self, config):
        """ :meth:`.WNetworkNativeTransportProto.server_socket` method implementation
                """
        if self._WNetworkNativeTransport__server_socket is None:
            self._WNetworkNativeTransport__server_socket = self.create_server_socket(config)
            si = self.bind_socket(config).pair()
            self._WNetworkNativeTransport__server_socket.bind(si)
            self._WNetworkNativeTransport__server_socket.listen()
            print('Bind: ' + str(self))
            print('Bind! to: ' + str(si))
        return self._WNetworkNativeTransport__server_socket

    @verify_type(config=WConfig, close_fd=bool)
    def close_server_socket(self, config, close_fd=True):
        """ :meth:`.WNetworkNativeTransportProto.close_server_socket` method implementation
                """
        if close_fd is True:
            print('Bind closed: ' + str(self))
            self._WNetworkNativeTransport__server_socket.close()
        self._WNetworkNativeTransport__server_socket = None

    @verify_type(config=WConfig)
    def client_socket(self, config):
        """ :meth:`.WNetworkNativeTransportProto.client_socket` method implementation
                """
        if self._WNetworkNativeTransport__client_socket is None:
            self._WNetworkNativeTransport__client_socket = self.create_client_socket(config)
        return self._WNetworkNativeTransport__client_socket

    @verify_type(config=WConfig, close_fd=bool)
    def close_client_socket(self, config, close_fd=True):
        """ :meth:`.WNetworkNativeTransportProto.close_client_socket` method implementation
                """
        if close_fd is True:
            self._WNetworkNativeTransport__client_socket.close()
        self._WNetworkNativeTransport__client_socket = None


class WUDPNetworkNativeTransport(WNetworkNativeTransport, metaclass=ABCMeta):
    __doc__ = ' Basic UDP transport implementation\n\n\tTODO: refactor this!\n\t'

    def _create_socket(self):
        """ Create general UDP-socket

                :return: socket.socket
                """
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class WTCPNetworkNativeTransport(WNetworkNativeTransport):
    __doc__ = ' Basic TCP transport implementation\n\n\tTODO: refactor this!\n\t'

    def _create_socket(self):
        """ Create general TCP-socket

                :return: socket.socket
                """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class WBroadcastNetworkTransport(WUDPNetworkNativeTransport):
    __doc__ = ' Network transport, that uses IPv4 broadcast (UDP) communication\n\n\tTODO: refactor this!\n\t'

    @verify_type('paranoid', target_socket_config=WNetworkNativeTransportSocketConfig)
    @verify_type('paranoid', bind_socket_config=WNetworkNativeTransportSocketConfig)
    def __init__(self, target_socket_config, bind_socket_config):
        """ Create new broadcast transport
                """
        WNetworkNativeTransport.__init__(self, target_socket_config, bind_socket_config)

    @verify_type('paranoid', config=WConfig)
    def target_socket(self, config):
        """ This method overrides :meth:`.WNetworkNativeTransport.target_socket` method. Do the same thing as
                basic method do, but also checks that the result address is IPv4 address.

                :param config: beacon configuration
                :return: WIPV4SocketInfo
                """
        target = WNetworkNativeTransport.target_socket(self, config)
        if isinstance(target.address(), WIPV4Address) is False:
            raise ValueError('Invalid address for broadcast transport')
        return target

    @verify_type('paranoid', config=WConfig)
    def create_client_socket(self, config):
        """ Create client broadcast socket

                :param config: client configuration
                :return: socket.socket
                """
        client_socket = WUDPNetworkNativeTransport.create_client_socket(self, config)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return client_socket


class WMulticastNetworkTransport(WUDPNetworkNativeTransport):
    __doc__ = ' Network transport, that uses IPv4 multicast communication\n\n\tTODO: refactor this!\n\t'

    @verify_type('paranoid', target_socket_config=WNetworkNativeTransportSocketConfig)
    @verify_type('paranoid', bind_socket_config=WNetworkNativeTransportSocketConfig)
    def __init__(self, target_socket_config, bind_socket_config):
        """ Create new multicast transport
                """
        WUDPNetworkNativeTransport.__init__(self, target_socket_config, bind_socket_config)

    @verify_type('paranoid', config=WConfig)
    def target_socket(self, config):
        """ This method overrides :meth:`.WNetworkNativeTransport.target_socket` method. Do the same thing as
                basic method do, but also checks that the result address is IPv4 multicast address.

                :param config: beacon configuration
                :return: WIPV4SocketInfo
                """
        target = WUDPNetworkNativeTransport.target_socket(self, config)
        if WNetworkIPV4.is_multicast(target.address()) is False:
            raise ValueError('IP multicast address not RFC compliant')
        return target

    @verify_type('paranoid', config=WConfig)
    def create_server_socket(self, config):
        """ Create server multicast socket. Socket will be joined to the multicast-group (same as it is
                specified in client configuration, same as client does)

                :param config: server configuration
                :return: socket.socket
                """
        server_socket = WUDPNetworkNativeTransport.create_server_socket(self, config)
        group = socket.inet_aton(str(self.target_socket(config).address()))
        group_membership = struct.pack('4sL', group, socket.INADDR_ANY)
        server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, group_membership)
        return server_socket