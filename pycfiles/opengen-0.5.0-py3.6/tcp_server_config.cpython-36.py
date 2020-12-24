# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/config/tcp_server_config.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 1315 bytes


class TcpServerConfiguration:

    def __init__(self, bind_ip='127.0.0.1', bind_port=8333):
        """
        Configuration of the TCP server

        :param bind_ip: IP address of generated TCP server. The default
        value is "127.0.0.1" (localhost). Use "0.0.0.0" for the generated
        TCP server to bind on all IPs.

        :param bind_port: Port on which the generated TCP server will bind.
        The default is 8333. Make sure you use an available port and avoid using
        privileged ports (i.e., 1 to 1024), well-known ports that are potentially
        used by other services and you should also avoid ephemeral ports
        (32768 to 65535 on Linux, 1025 to 5000 on Windows)

        :returns: new instance of TcpServerConfiguration, which can then be
        provided to an instance of `OpEnOptimizerBuilder` via `enable_tcp_interface`
        """
        self._TcpServerConfiguration__bind_ip = bind_ip
        self._TcpServerConfiguration__bind_port = bind_port

    @property
    def bind_ip(self):
        """
        IP at which the TCP server should bind, as a string
        :return: TCP server IP
        """
        return self._TcpServerConfiguration__bind_ip

    @property
    def bind_port(self):
        """
        Port at which the TCP server should bind, as int
        :return: TCP server port
        """
        return self._TcpServerConfiguration__bind_port