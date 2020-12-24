# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/option.py
# Compiled at: 2019-12-08 21:20:00
import os, sys, glob, logging, inspect
from clocwalk.libs.core.data import paths
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.exception import SyntaxException
from clocwalk.libs.core.exception import GenericException

def _setPluginFunctions():
    """
    Loads plugin detecting functions from script(s)
    """
    plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, '*.py'))
    if not plugins:
        plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, '*.pyc'))
    for found in plugins:
        dirname, filename = os.path.split(found)
        dirname = os.path.abspath(dirname)
        if filename in ('__init__.py', '__init__.pyc'):
            continue
        if filename.endswith('.pyc'):
            pluginName = filename[:-4]
        else:
            pluginName = filename[:-3]
        logger.debug("loading plugin script '%s'" % pluginName)
        if dirname not in sys.path:
            sys.path.insert(0, dirname)
        try:
            module = __import__(pluginName)
        except ImportError as msg:
            raise SyntaxException("cannot import plugin script '%s' (%s)" % (pluginName, msg))

        _ = dict(inspect.getmembers(module))
        if 'start' not in _:
            errMsg = "missing function 'start(**kwargs)' "
            errMsg += "in start script '%s'" % found
            raise GenericException(errMsg)
        else:
            kb.pluginFunctions.append((_['start'], _.get('__product__', pluginName)))


def _setConfigFile():
    """

    :return:
    """
    import yaml
    with open(paths.config_path) as (fp):
        conf.cloc = yaml.load(fp, Loader=yaml.FullLoader)


def setVerbosity():
    """
    This function set the verbosity of output messages.
    """
    if conf.verbose is None:
        conf.verbose = 1
    conf.verbose = int(conf.verbose)
    if conf.verbose == 0:
        logger.setLevel(logging.ERROR)
    elif conf.verbose == 1:
        logger.setLevel(logging.INFO)
    elif conf.verbose >= 2:
        logger.setLevel(logging.DEBUG)
    return


def init():
    """
    Set attributes into both configuration and knowledge base singletons
    based upon command line and configuration file options.
    """
    setVerbosity()
    _setPluginFunctions()
    _setConfigFile()