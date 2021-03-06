# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/loader.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 4400 bytes
"""
Initialization module for tpDcc.libs.qt
"""
from __future__ import print_function, division, absolute_import
import os, sys, inspect, logging
main = __import__('__main__')

def init(do_reload=False, dev=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    :param dev: bool, Whether artellapipe is initialized in dev mode or not
    """
    from tpDcc.libs.qt import register
    from tpDcc.libs.python import importer
    logger = create_logger()

    class tpQtLib(importer.Importer):

        def __init__(self, *args, **kwargs):
            (super(tpQtLib, self).__init__)(args, module_name='tpDcc.libs.qt', **kwargs)

        def get_module_path(self):
            """
            Returns path where tpQtLib module is stored
            :return: str
            """
            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    try:
                        import tpDcc.libs.qt
                        mod_dir = tpDcc.libs.qt.__path__[0]
                    except Exception:
                        return

            return mod_dir

        def update_paths(self):
            """
            Adds path to system paths at startup
            """
            paths_to_update = [
             self.externals_path()]
            for p in paths_to_update:
                if os.path.exists(p) and p not in sys.path:
                    sys.path.append(p)

        def externals_path(self):
            """
            Returns the paths where tpPyUtils externals packages are stored
            :return: str
            """
            return os.path.join(self.get_module_path(), 'externals')

    def init_dcc(do_reload=False):
        """
        Checks DCC we are working on an initializes proper variables
        """
        global Dcc
        if 'cmds' in main.__dict__:
            from tpDcc.dccs.maya import loader
            loader.init_ui(do_reload=do_reload)
        else:
            if 'MaxPlus' in main.__dict__:
                from tpDcc.dccs.max import loader
                loader.init_ui(do_reload=do_reload)
            else:
                if 'hou' in main.__dict__:
                    from tpDcc.dccs.houdini import loader
                    loader.init_ui(do_reload=do_reload)
                else:
                    if 'nuke' in main.__dict__:
                        from tpDcc.dccs.nuke import loader
                    else:
                        from tpDcc.core import dcc
                        Dcc = dcc.UnknownDCC
                        logger.warning('No DCC found, using abstract one!')
        from tpDcc.managers import callbacks
        callbacks.CallbacksManager.initialize()

    qt_importer = importer.init_importer(importer_class=tpQtLib, do_reload=False)
    qt_importer.update_paths()
    register.register_class('logger', logger)
    qt_importer.import_modules(skip_modules=['tpDcc.libs.qt.externals'])
    qt_importer.import_packages(only_packages=True, skip_modules=['tpDcc.libs.qt.externals'], order=[
     'tpDcc.libs.qt.core', 'tpDcc.libs.qt.widgets'])
    if do_reload:
        qt_importer.reload_all()
    init_dcc(do_reload=do_reload)
    register_resources()


def create_logger():
    """
    Returns logger of current module
    """
    logging.config.fileConfig((get_logging_config()), disable_existing_loggers=False)
    logger = logging.getLogger('tpDcc-libs-qt')
    return logger


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """
    tppyutils_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs'))
    if not os.path.isdir(tppyutils_logger_dir):
        os.makedirs(tppyutils_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """
    create_logger_directory()
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def register_resources():
    """
    Registers tpDcc.libs.qt resources path
    """
    import tpDcc
    resources_manager = tpDcc.ResourcesMgr()
    resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
    resources_manager.register_resource(resources_path, key='tpDcc-libs-qt')