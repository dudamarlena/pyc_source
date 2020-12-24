# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/cisco/aci/apic/ssh.py
# Compiled at: 2020-04-24 07:59:04
# Size of source mod 2**32: 1459 bytes
from jinjamator.plugin_loader.content import py_load_plugins

def run(command, **kwargs):
    py_load_plugins(globals())
    kwargs['device_type'] = 'cisco_nxos'
    kwargs['cmd_verify'] = False
    kwargs['strip_command'] = True
    self._parent.configuration['ssh_username'] = self._parent.configuration.get('apic_username') or self._parent.configuration.get('ssh_username') or self._parent.handle_undefined_var('apic_username')
    self._parent.configuration['ssh_host'] = self._parent.configuration.get('apic_ip') or self._parent.handle_undefined_var('apic_ip')
    self._parent.configuration['ssh_password'] = self._parent.configuration.get('apic_password') or self._parent.configuration.get('ssh_password') or self._parent.handle_undefined_var('apic_password')
    return (ssh.run)(command, **kwargs)