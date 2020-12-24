# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/nago/nago/extensions/plugins.py
# Compiled at: 2013-12-04 13:19:15
""" Run local nagios plugins """
import nago.core
from nago.core import nago_access
import nago.settings, os.path, pynag.Utils, subprocess

@nago_access()
def get(search='unsigned'):
    """ List all available plugins"""
    plugins = []
    for i in os.walk('/usr/lib/nagios/plugins'):
        for f in i[2]:
            plugins.append(f)

    return plugins


@nago_access()
def run(plugin_name, *args, **kwargs):
    """ Run a specific plugin """
    plugindir = nago.settings.get_option('plugin_dir')
    plugin = plugindir + '/' + plugin_name
    if not os.path.isfile(plugin):
        raise ValueError('Plugin %s not found' % plugin)
    command = [plugin] + list(args)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate('through stdin to stdout')
    result = {}
    result['stdout'] = stdout
    result['stderr'] = stderr
    result['return_code'] = p.returncode
    return result