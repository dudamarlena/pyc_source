# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_vagrant/__init__.py
# Compiled at: 2016-05-04 19:26:49
from .vm.vm import vm
from .image.image import image
from cloudmesh_client.common.Shell import Shell
from .version import __version__

def version(verbose=False):
    result = Shell.execute('vagrant', ['version'])
    if verbose:
        return result
    else:
        lines = result.split('\n')
        for line in lines:
            if 'Installed Version:' in line:
                return line.replace('Installed Version:', '').strip()

        return
        return