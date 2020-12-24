# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Defaults.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 9980 bytes
"""
ClusterShell Defaults module.

Manage library defaults.
"""
from __future__ import print_function
try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError

import os, sys
CFG_SECTION_TASK_DEFAULT = 'task.default'
CFG_SECTION_TASK_INFO = 'task.info'
CFG_SECTION_NODESET = 'nodeset'

def _task_print_debug(task, line):
    """Default task debug printing function."""
    print(line)


def _load_workerclass(workername):
    """
    Return the class pointer matching `workername`.

    The module is loaded if not done yet.
    """
    modname = 'ClusterShell.Worker.%s' % workername.capitalize()
    if modname.lower() not in [mod.lower() for mod in list(sys.modules)]:
        __import__(modname)
    return sys.modules[modname].WORKER_CLASS


def _local_workerclass(defaults):
    """Return default local worker class."""
    return _load_workerclass(defaults.local_workername)


def _distant_workerclass(defaults):
    """Return default distant worker class."""
    return _load_workerclass(defaults.distant_workername)


def config_paths(config_name):
    """Return default path list for a ClusterShell config file name."""
    return [
     '/etc/clustershell/%s' % config_name,
     os.path.expanduser('~/.local/etc/clustershell/%s' % config_name),
     os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), 'clustershell', config_name)]


def _converter_integer_tuple(value):
    """ConfigParser converter for tuple of integers"""
    return tuple(int(x) for x in value.split(',') if x.strip())


def _parser_get_integer_tuple(parser, section, option, **kwargs):
    """
    Compatible converter for parsing tuple of integers until we can use
    converters from new ConfigParser (Python 3.5+).
    """
    return _converter_integer_tuple((ConfigParser.get)(parser, section, option, **kwargs))


class Defaults(object):
    __doc__ = '\n    Class used to manipulate ClusterShell defaults.\n\n    The following attributes may be read at any time and also changed\n    programmatically, for most of them **before** ClusterShell objects\n    (Task or NodeSet) are initialized.\n\n    NodeSet defaults:\n\n    * fold_axis (tuple of axis integers; default is empty tuple ``()``)\n\n    Task defaults:\n\n    * stderr (boolean; default is ``False``)\n    * stdin (boolean; default is ``True``)\n    * stdout_msgtree (boolean; default is ``True``)\n    * stderr_msgtree (boolean; default is ``True``)\n    * engine (string; default is ``\'auto\'``)\n    * port_qlimit (integer; default is ``100``)\n    * local_workername (string; default is ``\'exec\'``)\n    * distant_workername (string; default is ``\'ssh\'``)\n    * debug (boolean; default is ``False``)\n    * print_debug (function; default is internal)\n    * fanout (integer; default is ``64``)\n    * grooming_delay (float; default is ``0.25``)\n    * connect_timeout (float; default is ``10``)\n    * command_timeout (float; default is ``0``)\n\n    Example of use::\n\n        >>> from ClusterShell.Defaults import DEFAULTS\n        >>> from ClusterShell.Task import task_self\n        >>> # Change default distant worker to rsh (WorkerRsh)\n        ... DEFAULTS.distant_workername = \'rsh\'\n        >>> task = task_self()\n        >>> task.run("uname -r", nodes="cs[01-03]")\n        <ClusterShell.Worker.Rsh.WorkerRsh object at 0x1f4a410>\n        >>> list((str(msg), nodes) for msg, nodes in task.iter_buffers())\n        [(\'3.10.0-229.7.2.el7.x86_64\', [\'cs02\', \'cs01\', \'cs03\'])]\n\n\n    The library default values of all of the above attributes may be changed\n    using the defaults.conf configuration file, except for *print_debug*\n    (cf. :ref:`defaults-config`). An example defaults.conf file should be\n    included with ClusterShell. Remember that this could affect all\n    applications using ClusterShell.\n    '
    _TASK_DEFAULT = {'stderr':False, 
     'stdin':True, 
     'stdout_msgtree':True, 
     'stderr_msgtree':True, 
     'engine':'auto', 
     'port_qlimit':100, 
     'auto_tree':True, 
     'local_workername':'exec', 
     'distant_workername':'ssh'}
    _TASK_DEFAULT_CONVERTERS = {'stderr':ConfigParser.getboolean, 
     'stdin':ConfigParser.getboolean, 
     'stdout_msgtree':ConfigParser.getboolean, 
     'stderr_msgtree':ConfigParser.getboolean, 
     'engine':ConfigParser.get, 
     'port_qlimit':ConfigParser.getint, 
     'auto_tree':ConfigParser.getboolean, 
     'local_workername':ConfigParser.get, 
     'distant_workername':ConfigParser.get}
    _TASK_INFO = {'debug':False, 
     'print_debug':_task_print_debug, 
     'fanout':64, 
     'grooming_delay':0.25, 
     'connect_timeout':10, 
     'command_timeout':0}
    _TASK_INFO_CONVERTERS = {'debug':ConfigParser.getboolean, 
     'fanout':ConfigParser.getint, 
     'grooming_delay':ConfigParser.getfloat, 
     'connect_timeout':ConfigParser.getfloat, 
     'command_timeout':ConfigParser.getfloat}
    _TASK_INFO_PKEYS_BL = [
     'engine', 'print_debug']
    _NODESET = {'fold_axis': ()}
    _NODESET_CONVERTERS = {'fold_axis': _parser_get_integer_tuple}

    def __init__(self, filenames):
        """Initialize Defaults from config filenames"""
        self._task_default = self._TASK_DEFAULT.copy()
        self._task_info = self._TASK_INFO.copy()
        self._task_info_pkeys_bl = list(self._TASK_INFO_PKEYS_BL)
        self._nodeset = self._NODESET.copy()
        config = ConfigParser()
        parsed = config.read(filenames)
        if parsed:
            self._parse_config(config)

    def _parse_config(self, config):
        """parse config"""
        for key, conv in self._TASK_DEFAULT_CONVERTERS.items():
            try:
                self._task_default[key] = conv(config, CFG_SECTION_TASK_DEFAULT, key)
            except (NoSectionError, NoOptionError):
                pass

        for key, conv in self._TASK_INFO_CONVERTERS.items():
            try:
                self._task_info[key] = conv(config, CFG_SECTION_TASK_INFO, key)
            except (NoSectionError, NoOptionError):
                pass

        for key, conv in self._NODESET_CONVERTERS.items():
            try:
                self._nodeset[key] = conv(config, CFG_SECTION_NODESET, key)
            except (NoSectionError, NoOptionError):
                pass

    def __getattr__(self, name):
        """Defaults attribute lookup"""
        if name in self._task_default:
            return self._task_default[name]
        else:
            if name in self._task_info:
                return self._task_info[name]
            if name in self._nodeset:
                return self._nodeset[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Defaults attribute assignment"""
        if name in ('_task_default', '_task_info', '_task_info_pkeys_bl', '_nodeset'):
            object.__setattr__(self, name, value)
        else:
            if name in self._task_default:
                self._task_default[name] = value
            else:
                if name in self._task_info:
                    self._task_info[name] = value
                else:
                    if name in self._nodeset:
                        self._nodeset[name] = value
                    else:
                        raise AttributeError(name)


DEFAULTS = Defaults(config_paths('defaults.conf'))