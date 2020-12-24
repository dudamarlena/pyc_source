# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/cisco/ios.py
# Compiled at: 2020-04-25 16:12:43
# Size of source mod 2**32: 779 bytes
from jinjamator.plugin_loader.content import py_load_plugins

def query(command, **kwargs):
    py_load_plugins(globals())
    kwargs['device_type'] = 'cisco_ios'
    return (ssh.query)(command, **kwargs)