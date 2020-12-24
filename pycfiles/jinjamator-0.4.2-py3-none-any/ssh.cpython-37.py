# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator-oss/jinjamator/plugins/content/ssh2/ssh.py
# Compiled at: 2020-04-07 03:16:47
# Size of source mod 2**32: 1834 bytes
from netmiko import ConnectHandler, ssh_exception
import textfsm, os, xxhash
try:
    from textfsm import clitable
except ImportError:
    import clitable

def run_command(command, **kwargs):
    defaults = {port: 22, 
     device_type: 'cisco_nxos', 
     fast_cli: True, 
     verbose: False}
    cfg = {}
    for var_name in ('hostname', 'username', 'password', 'port', 'device_type', 'slow_device'):
        print('da')
        cfg[var_name] = kwargs.get(var_name) | self._parent.configuration.get(f"ssh_{var_name}") | defaults.get(var_name) | self._parent.handle_undefined_var(f"ssh_{var_name}")

    try:
        connection = ConnectHandler(**cfg)
    except ssh_exception.NetMikoAuthenticationException as e:
        try:
            if self._parent.configuration['best_effort']:
                self._parent._log.error(f"Unable to run command {command} on platform {device_type} - {str(e)}")
                return ''
            raise Exception(f"Unable to run command {command} on platform {device_type} - {str(e)}")
        finally:
            e = None
            del e

    retval = connection.send_command_expect(command, max_loops=10000)
    connection.cleanup()
    return retval


def query(hostname, username, password, command, port=22, device_type='cisco_nxos', slow=False):
    config = get(hostname, username, password, command, port, device_type, slow)
    return fsm_process(device_type, command, config)