# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/tools/setup/lib/pip.py
# Compiled at: 2016-09-29 19:43:16
# Size of source mod 2**32: 1248 bytes
import pip, importlib

def install_packages(_package_names):
    """
    Install the packages listed if not present
    :param _package_names: A list of the packages
    :return:
    """
    _installed = []
    for _curr_package in _package_names:
        if importlib.util.find_spec(_curr_package) is None:
            print(_curr_package + ' not installed, installing...')
            pip.main(['install', _curr_package])
            print(_curr_package + ' installed...')
            _installed.append(_curr_package)
        else:
            print(_curr_package + ' already installed, skipping...')

    return _installed


def uninstall_packages(_package_names):
    """
    Install the packages listed if not present
    :param _package_names: A list of the packages
    :return:
    """
    _removed = []
    for _curr_package in _package_names:
        if importlib.util.find_spec(_curr_package) is not None:
            print(_curr_package + ' installed, uninstalling...')
            pip.main(['uninstall', _curr_package, '--yes'])
            print(_curr_package + ' uninstalled...')
            _removed.append(_curr_package)
        else:
            print(_curr_package + ' not installed, skipping...')

    return _removed