# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpHoudiniLib/loader.py
# Compiled at: 2020-01-16 21:52:53
# Size of source mod 2**32: 2046 bytes
"""
Initialization module for tpHoudiniLib
"""
from __future__ import print_function, division, absolute_import
import os, inspect, hou
from tpPyUtils import importer
logger = None

class tpHoudiniLib(importer.Importer, object):

    def __init__(self, *args, **kwargs):
        (super(tpHoudiniLib, self).__init__)(args, module_name='tpHoudiniLib', **kwargs)

    def get_module_path(self):
        """
        Returns path where tpHoudiniLib module is stored
        :return: str
        """
        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return

        return mod_dir


def init_dcc(do_reload=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """
    global logger
    tphoudini_importer = importer.init_importer(importer_class=tpHoudiniLib, do_reload=False)
    logger = tphoudini_importer.logger
    tphoudini_importer.import_modules()
    tphoudini_importer.import_packages(only_packages=True)
    if do_reload:
        tphoudini_importer.reload_all()


def init_ui(do_reload=False):
    global logger
    tphoudini_importer = importer.init_importer(importer_class=tpHoudiniLib, do_reload=False)
    logger = tphoudini_importer.logger
    tphoudini_importer.import_modules(skip_modules=['tpHoudiniLib.core'])
    tphoudini_importer.import_packages(only_packages=True, skip_modules=['tpHoudiniLib.core'])
    if do_reload:
        tphoudini_importer.reload_all()