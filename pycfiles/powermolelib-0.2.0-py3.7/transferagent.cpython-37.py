# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolelib/powermolelib/transferagent.py
# Compiled at: 2020-05-11 17:44:59
# Size of source mod 2**32: 6979 bytes
__doc__ = '\nMain code for transferagent.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\nNOTE: The TransferAgent class is responsible to purge the stream (ie. index in stream is at COMMAND_PROMPT)\n\n'
import inspect, logging, os.path, pexpect
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

class LoggerMixin:
    """LoggerMixin"""

    def __init__(self):
        logger_basename = 'agent'
        self._logger = logging.getLogger(f"{logger_basename}.{self.__class__.__name__}")


class TransferAgent(LoggerMixin):
    """TransferAgent"""

    def __init__(self, path_ssh_cfg_minitor, all_hosts):
        super().__init__()
        self.all_hosts = all_hosts
        self.child = None
        self.path_ssh_cfg_minitor = path_ssh_cfg_minitor

    def __str__(self):
        return 'TransferAgent'

    def create_ssh_config(self):
        """______________."""
        pass

    @property
    def _path_to_agent_module(self):
        running_script = inspect.getframeinfo(inspect.currentframe()).filename
        running_script_dir = os.path.dirname(os.path.abspath(running_script))
        path_file = os.path.join(running_script_dir, 'payload', 'agent.py')
        self._logger.debug('minitoragent.py resides in: %s', running_script_dir)
        return path_file

    def _generate_ssh_runtime_param(self):
        last_host = self.all_hosts[(-1)]
        if len(self.all_hosts) == 1:
            order_of_hosts = f"{self.all_hosts[0]}"
        else:
            order_of_hosts = ''
            for i, host in enumerate(self.all_hosts):
                if i == 0:
                    order_of_hosts += (f"{host}")
                else:
                    order_of_hosts += f",{host}"

        runtime_param = f"scp -v -F {self.path_ssh_cfg_minitor} -o 'ProxyJump {order_of_hosts}' {self._path_to_agent_module} "
        runtime_param += f"{last_host}:/tmp"
        self._logger.debug(runtime_param)
        return runtime_param

    def start(self):
        """_______________________."""
        result = True
        try:
            try:
                self.child = pexpect.spawn((self._generate_ssh_runtime_param()), env={'TERM': 'dumb'})
                self._logger.debug('going through the stream to match patterns')
                for hostname in self.all_hosts:
                    index = self.child.expect([
                     f"Authenticated to {hostname}", 'Last failed login:', 'Last login:', 'socket error',
                     'not accessible', 'fingerprint', 'open failed: connect failed:', 'No such file', pexpect.TIMEOUT])
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
                    else:
                        if index == 7:
                            continue
                        if index == 8:
                            self._logger.error('TIMEOUT exception was thrown. ssh could probably not connect to %s', hostname)
                            self.child.terminate()
                            result = False
                        else:
                            self._logger.error('unknown state reached')
                            result = False

            except pexpect.exceptions.ExceptionPexpect:
                self._logger.error('EOF is read; ssh has exited abnormally')
                self.child.terminate()
                result = False

        finally:
            return

        return result