# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/loader.py
# Compiled at: 2020-04-26 16:42:29
# Size of source mod 2**32: 9829 bytes
"""
Initialization module for tpDcc
"""
from __future__ import print_function, division, absolute_import
import os, inspect, logging.config
from tpDcc import register
from tpDcc.libs.python import python
from tpDcc.abstract import dcc as abstract_dcc, shelf as abstract_shelf, menu as abstract_menu
if python.is_python2():
    import pkgutil as loader
else:
    import importlib as loader
main = __import__('__main__')

class DccCallbacks(object):
    Shutdown = (
     'Shutdown', {'type': 'simple'})
    Tick = ('Tick', {'type': 'simple'})
    ScenePreCreated = ('ScenePreCreated', {'type': 'simple'})
    ScenePostCreated = ('ScenePreCreated', {'type': 'simple'})
    SceneNewRequested = ('SceneNewRequested', {'type': 'simple'})
    SceneNewFinished = ('SceneNewFinished', {'type': 'simple'})
    SceneSaveRequested = ('SceneSaveRequested', {'type': 'simple'})
    SceneSaveFinished = ('SceneSaveFinished', {'type': 'simple'})
    SceneOpenRequested = ('SceneOpenRequested', {'type': 'simple'})
    SceneOpenFinished = ('SceneOpenFinished', {'type': 'simple'})
    UserPropertyPreChanged = ('UserPropertyPreChanged', {'type': 'filter'})
    UserPropertyPostChanged = ('UserPropertyPostChanged', {'type': 'filter'})
    NodeSelect = ('NodeSelect', {'type': 'filter'})
    NodeAdded = ('NodeAdded', {'type': 'filter'})
    NodeDeleted = ('NodeDeleted', {'type': 'filter'})


class Dccs(object):
    Unknown = 'unknown'
    Standalone = 'standalone'
    Houdini = 'houdini'
    Maya = 'maya'
    Max = 'max'
    Nuke = 'nuke'

    @staticmethod
    def get_available_dccs():
        return {k:v for k, v in Dccs.__class__.__dict__.items() if not k.startswith('__') if not k.startswith('__')}


def init(do_reload=False, dev=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    :param dev: bool, Whether artellapipe is initialized in dev mode or not
    """
    from tpDcc.libs.python import importer
    from tpDcc import register
    logger = create_logger()
    register.register_class('logger', logger)

    class tpDcc(importer.Importer):

        def __init__(self, *args, **kwargs):
            (super(tpDcc, self).__init__)(args, module_name='tpDcc', **kwargs)

        def get_module_path(self):
            """
            Returns path where tpDcc module is stored
            :return: str
            """
            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    try:
                        import tpDcc
                        mod_dir = tpDcc.__path__[0]
                    except Exception:
                        return

            return mod_dir

    try:
        if do_reload:
            import tpDcc as tp
            parent = tp.Dcc.get_main_window()
            if parent:
                for child in parent.children():
                    if isinstance(child, tp.Window):
                        child.close()
                        child.setParent(None)
                        child.deleteLater()

    except Exception:
        pass

    from tpDcc.libs import python
    python.init(do_reload=do_reload)
    dcclib_importer = importer.init_importer(importer_class=tpDcc, do_reload=False)
    dcclib_importer.import_modules(skip_modules=['tpDcc.dccs', 'tpDcc.libs', 'tpDcc.tools'])
    dcclib_importer.import_packages(only_packages=True,
      order=[
     'tpDcc.core'],
      skip_modules=['tpDcc.dccs', 'tpDcc.libs', 'tpDcc.tools'])
    if do_reload:
        dcclib_importer.reload_all()
    init_dcc(do_reload=do_reload)
    from tpDcc.libs.qt import loader
    loader.init(do_reload=do_reload)
    init_dcc_ui(do_reload=do_reload)
    init_managers(dev=dev, do_reload=do_reload)
    from tpDcc.managers import callbacks
    callbacks.CallbacksManager.initialize()
    from tpDcc.libs.nameit import loader
    loader.init(do_reload=do_reload)


def init_dcc(do_reload=False):
    """
    Checks DCC we are working on an initializes proper variables
    """
    if 'cmds' in main.__dict__:
        from tpDcc.dccs.maya import loader
        loader.init_dcc(do_reload=do_reload)
    else:
        if 'MaxPlus' in main.__dict__:
            from tpDcc.dccs.max import loader
            loader.init_dcc(do_reload=do_reload)
        else:
            if 'hou' in main.__dict__:
                from tpDcc.dccs.houdini import loader
                loader.init_dcc(do_reload=do_reload)
            else:
                if 'nuke' in main.__dict__:
                    from tpDcc.dccs.nuke import loader
                    loader.init_dcc(do_reload=do_reload)
                else:
                    from tpDcc import register
                    from tpDcc.dccs.standalone.core import dcc
                    register.register_class('Dcc', dcc.StandaloneDcc)


def init_dcc_ui(do_reload=False):
    """
    Checks DCC we are working on an initializes proper variables
    """
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
            elif 'nuke' in main.__dict__:
                from tpDcc.dccs.nuke import loader
                loader.init_ui(do_reload=do_reload)


def init_managers(dev=True, do_reload=False):
    """
    Initializes all tpDcc managers
    """
    import tpDcc
    from tpDcc import config
    from tpDcc import toolsets
    tpDcc.ConfigsMgr().register_package_configs('tpDcc', os.path.dirname(config.__file__))
    core_config = tpDcc.ConfigsMgr().get_config('tpDcc-core')
    if not core_config:
        tpDcc.logger.warning('tpDcc-core configuration file not found! Make sure that you have tpDcc-config package installed!')
        return
    tools_to_load = core_config.get('tools', list())
    tpDcc.ToolsMgr().load_package_tools('tpDcc', tools_to_load=tools_to_load, dev=dev)
    if do_reload:
        tpDcc.ToolsMgr().reload_tools()
    tpDcc.ToolsetsMgr().register_path('tpDcc', os.path.dirname(toolsets.__file__))
    tpDcc.ToolsetsMgr().load_registered_toolsets('tpDcc', tools_to_load=tools_to_load, dev=dev, do_reload=do_reload)


def create_logger():
    """
    Returns logger of current module
    """
    logging.config.fileConfig((get_logging_config()), disable_existing_loggers=False)
    logger = logging.getLogger('tpDcc-core')
    return logger


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """
    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """
    create_logger_directory()
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def is_unknown():
    """
    Check if current environment is unknown or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Unknown


def is_standalone():
    """
    Check if current environment is standalone or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Standalone


def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Nuke


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Maya


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Max


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """
    import tpDcc
    return tpDcc.Dcc.get_name() == Dccs.Houdini


def callbacks():
    """
    Return a full list of callbacks based on DccCallbacks dictionary
    :return: list<str>
    """
    new_list = list()
    for k, v in DccCallbacks.__dict__.items():
        if not k.startswith('__'):
            if k.endswith('__'):
                pass
            else:
                new_list.append(v[0])

    return new_list


register.register_class('Dcc', abstract_dcc.AbstractDCC())
register.register_class('Menu', abstract_menu.AbstractMenu)
register.register_class('Shelf', abstract_shelf.AbstractShelf)
register.register_class('Dccs', Dccs)
register.register_class('DccCallbacks', DccCallbacks)
register.register_class('callbacks', callbacks)
register.register_class('is_unknown', is_unknown)
register.register_class('is_standalone', is_standalone)
register.register_class('is_maya', is_maya)
register.register_class('is_max', is_max)
register.register_class('is_houdini', is_houdini)
register.register_class('is_nuke', is_nuke)