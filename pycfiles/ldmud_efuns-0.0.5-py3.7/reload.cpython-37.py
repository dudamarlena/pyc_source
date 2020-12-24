# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldmudefuns/reload.py
# Compiled at: 2020-04-05 17:07:06
# Size of source mod 2**32: 1650 bytes
import importlib, pkg_resources, site, sys, os, configparser, ldmud

def reload_modules():
    """
    SYNOPSIS
            void python_reload()

    DESCRIPTION
            Reloads all Python efuns. All packages providing the "ldmud_efuns"
            entry point are loaded. If they were already loaded, they are reloaded.
            Then the entry point is executed to register the efuns.

            Before reloading the function on_reload() is called in the module.

    SEE ALSO
            python_efun_help(E)
    """
    importlib.reload(site)
    ws = pkg_resources.WorkingSet()
    modules = dict(sys.modules)
    reloaded = set()
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    efunconfig = config['efuns']
    for entry_point in ws.iter_entry_points('ldmud_efun'):
        if efunconfig.getboolean(entry_point.name, True):
            names = entry_point.module_name.split('.')
            for module in ('.'.join(names[:pos]) for pos in range(len(names), 0, -1)):
                if not module not in modules:
                    if module in reloaded:
                        break
                    try:
                        sys.modules[module].on_reload()
                    except:
                        pass

                    del sys.modules[module]
                    reloaded.add(module)
                    print('Reload module', module)

            ldmud.register_efun(entry_point.name, entry_point.load())


def register():
    ldmud.register_efun('python_reload', reload_modules)