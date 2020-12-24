# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/cisco/nxos.py
# Compiled at: 2020-04-15 04:18:28
# Size of source mod 2**32: 780 bytes
from jinjamator.plugin_loader.content import py_load_plugins

def query(command, **kwargs):
    py_load_plugins(globals())
    kwargs['device_type'] = 'cisco_nxos'
    return (ssh.query)(command, **kwargs)