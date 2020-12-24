# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRenamer/__init__.py
# Compiled at: 2019-12-22 00:17:48
# Size of source mod 2**32: 2608 bytes
"""
Initialization module for tpRenamer
"""
from __future__ import print_function, division, absolute_import
import os, inspect
from tpPyUtils import importer
from tpQtLib.core import resource as resource_utils
logger = None
resource = None
configs_manager = None

class tpRenamerResource(resource_utils.Resource, object):
    RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


class tpRenamer(importer.Importer, object):

    def __init__(self, *args, **kwargs):
        (super(tpRenamer, self).__init__)(args, module_name='tpRenamer', **kwargs)

    def get_module_path(self):
        """
        Returns path where tpRenamer module is stored
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

    def get_configs_path(self):
        """
        Returns path where base tpNodeGraph configurations are located
        :return: str
        """
        return os.path.join(self.get_module_path(), 'configs')

    def create_configuration_manager(self):
        """
        Creates manager that handles tpNodeGraph configuration
        :return:
        """
        global configs_manager
        from tpQtLib.core import config
        configs_manager = config.ConfigurationManager(config_paths=(self.get_configs_path()))


def init(do_reload=False, dev=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """
    global logger
    global resource
    tprenamer_importer = importer.init_importer(importer_class=tpRenamer, do_reload=do_reload, debug=dev)
    logger = tprenamer_importer.logger
    resource = tpRenamerResource
    tprenamer_importer.import_modules()
    tprenamer_importer.import_packages(only_packages=True)
    if do_reload:
        tprenamer_importer.reload_all()
    tprenamer_importer.create_configuration_manager()


def run(do_reload=False):
    init(do_reload=do_reload)
    from tpRenamer.core import renamer
    win = renamer.run()
    return win