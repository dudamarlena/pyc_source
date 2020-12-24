# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scripy/setup/config.py
# Compiled at: 2010-02-06 06:59:54
"""
load_yaml - load YAML file.
"""
__all__ = [
 'load_yaml']
import yaml, yamlog
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .. import system
_log = yamlog.logger(__name__)

def load_yaml(filename):
    """Load the YAML configuration file.

    ...

    Parameters
    ----------
    filename : str
        The file name of YAML document.

    Returns
    -------
    config : object
        The corresponding Python object.

    Raises
    ------
    StandardError
        If tle file can not be read.
    YAMLError
        If there is an error with the sintaxis.

    """
    try:
        f = open(filename, 'r')
        config = yaml.load_all(f, Loader=Loader)
    except yaml.YAMLError, err:
        f.close()
        _log.error('can not load YAML file')
        _log.debug(str(err))
        raise yaml.YAMLError(str(err))
    except StandardError, err:
        _log.error('can not load YAML file')
        _log.debug(str(err))
        raise StandardError(str(err))
    else:
        f.close()
        return config