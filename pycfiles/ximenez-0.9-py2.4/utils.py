# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/utils.py
# Compiled at: 2007-11-23 17:36:03
"""Define various utility functions.

$Id: utils.py 26 2007-11-23 22:36:07Z damien.baty $
"""
import imp, os.path

def getPluginInstance(plugin, kind=None):
    """Retrieve a plug-in instance from ``plugin``.

    ``plugin`` may be:

    - the path (file path) to a Python module which defines a plug-in.

    - a (possibly dotted) module name from the set of built-in Ximenez
    plug-ins. In this case, ``kind`` must be either ``actions`` or
    ``collectors` (because these are the names of the related
    sub-packages in Ximenez).
    """
    if os.path.exists(plugin):
        module = imp.load_source('plugin', plugin)
    elif not kind:
        raise ImportError('Plugin-in kind is missing.')
    module_path = ('.').join(('ximenez', kind, plugin))
    module = __import__(module_path)
    for component in module_path.split('.')[1:]:
        module = getattr(module, component)

    return module.getInstance()