# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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