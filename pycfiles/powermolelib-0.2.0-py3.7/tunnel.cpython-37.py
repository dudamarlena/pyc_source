# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolelib/powermolelib/tunnel.py
# Compiled at: 2020-05-11 17:44:48
# Size of source mod 2**32: 8291 bytes
__doc__ = '\nMain code for tunnel.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\nNOTE: The Tunnel classes are responsible to purge the stream (ie. index in stream is at COMMAND_PROMPT)\n\n'
import logging, pexpect
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '10-05-2019'
__copyright__ = 'Copyright 2020, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
COMMAND_PROMPT = '[#$] '
LOCAL_HEARTBEAT_PORT = 11600
LOCAL_AGENT_PORT = 44191
LOCAL_COMMAND_PORT = 11800
LOCAL_PROXY_PORT = 8080
LOCAL_TRANSFER_PORT = 11700

class LoggerMixin:
    """LoggerMixin"""

    def __init__(self):
        logger_basename = 'agent'
        self._logger = logging.getLogger(f"{logger_basename}.{self.__class__.__name__}")


class Tunnel(LoggerMixin):
    """Tunnel"""

    def __init__(self, path_ssh_cfg_minitor, mode, all_hosts, forward_connections=None):
        """Initialize the Tunnel object."""
        super().__init__()
        self.host_port_proxy_server = 44192
        self.host_port_heartbeat_responder = 44193
        self.host_port_file_server = 44194
        self.host_port_command_server = 44195
        self.host_port_agent = 44191
        self.forward_connections = forward_connections
        self.mode = mode
        self.all_hosts = all_hosts
        self.child = None
        self.local_agent_port = LOCAL_AGENT_PORT
        self.local_heartbeat_port = LOCAL_HEARTBEAT_PORT
        self.path_ssh_cfg_minitor = path_ssh_cfg_minitor

    def __str__(self):
        return 'Tunnel'

    def _generate_ssh_runtime_param(self):
        last_host = self.all_hosts[(-1)]
        var_param = None
        if self.mode == 'FOR':
            var_param = f"{self.forward_connections} "
        elif self.mode == 'TOR':
            var_param = f"-L{LOCAL_PROXY_PORT}:{last_host}:{self.host_port_proxy_server} "
        elif self.mode == 'INTERACTIVE':
            var_param = f"-L{LOCAL_COMMAND_PORT}:{last_host}:{self.host_port_command_server} "
        elif self.mode == 'FILE':
            var_param = f"-L{LOCAL_TRANSFER_PORT}:{last_host}:{self.host_port_file_server} "
        if len(self.all_hosts) == 2:
            order_of_hosts = f"{self.all_hosts[0]} {self.all_hosts[1]}"
        else:
            order_of_hosts = ''
            for i, host in enumerate(self.all_hosts):
                if i == 0:
                    order_of_hosts += (f"{host}")
                elif i < len(self.all_hosts) - 1:
                    order_of_hosts += f",{host}"
                else:
                    order_of_hosts += f" {host}"

        runtime_param = f"ssh -v -F {self.path_ssh_cfg_minitor} -L{LOCAL_AGENT_PORT}:{last_host}:{self.host_port_agent} -L{LOCAL_HEARTBEAT_PORT}:{last_host}:{self.host_port_heartbeat_responder} "
        runtime_param += var_param
        runtime_param += f"-J {order_of_hosts}"
        self._logger.debug(runtime_param)
        return runtime_param

    def start(self):
        """__________________."""
        result = True
        try:
            try:
                self.child = pexpect.spawn((self._generate_ssh_runtime_param()), env={'TERM': 'dumb'})
                self._logger.debug('going through the stream to match patterns')
                for hostname in self.all_hosts:
                    index = self.child.expect([
                     f"Authenticated to {hostname}", 'Last failed login:', 'Last login:', 'socket error',
                     'not accessible', 'fingerprint', 'open failed: connect failed:', pexpect.TIMEOUT])
                    if index == 0:
                        self._logger.info('authenticated to %s', hostname)
                    elif index == 1:
                        self._logger.debug('there were failed login attempts')
                    elif index == 2:
                        self._logger.debug('there where no failed login attempts')
                    elif index == 3:
                        self._logger.error('socket error. probable cause: SSH service on proxy or target machine disabled')
                        self.child.terminate()
                        result = False
                    elif index == 4:
                        self._logger.error('the identity file is not accessible')
                        self.child.terminate()
                        result = False
                    elif index == 5:
                        self._logger.warning('warning: hostname automatically added to list of known hosts')
                        self.child.sendline('yes')
                    elif index == 6:
                        self._logger.error('ssh could not connect to %s', hostname)
                        self.child.terminate()
                        result = False
                    elif index == 7:
                        self._logger.error('TIMEOUT exception was thrown. ssh could probably not connect to %s', hostname)
                        self.child.terminate()
                        result = False
                    else:
                        self._logger.error('unknown state reached')
                        result = False

                self.child.expect(COMMAND_PROMPT)
            except pexpect.exceptions.ExceptionPexpect:
                self._logger.error('EOF is read; ssh has exited abnormally')
                self.child.terminate()
                result = False

        finally:
            return

        return result

    def stop(self):
        """Closes the tunnel essentially by terminating the program SSH."""
        if self.child.isalive():
            self._logger.debug('ssh is alive, terminating')
            self.child.terminate()
        self._logger.debug('ssh terminated')
        return True