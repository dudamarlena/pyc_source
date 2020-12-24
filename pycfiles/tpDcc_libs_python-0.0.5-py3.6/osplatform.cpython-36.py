# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/osplatform.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 5473 bytes
"""
Utility methods related to cross-platform functionality
"""
from __future__ import print_function, division, absolute_import
import os, sys, getpass, platform, subprocess

class Platforms(object):
    Windows = 'Windows'
    Linux = 'Linux'
    Mac = 'MacOS'


def get_platform():
    pl = Platforms.Windows
    if 'linux' in sys.platform:
        pl = Platforms.Linux
    else:
        if sys.platform == 'darwin':
            pl = Platforms.Mac
    return pl


def get_home_directory(platform):
    if platform == Platforms.Windows:
        os.environ['TMPDIR'] = os.getenv('TEMP')
        os.environ['HOME'] = os.getenv('HOMEPATH')
        return os.getenv('HOMEPATH')
    else:
        if platform == Platforms.Linux:
            return os.getenv('HOME')
        if platform == Platforms.Mac:
            return os.getenv('HOME')


def is_linux():
    """
    Check to see if current platform is Linux
    :return: bool
    """
    platform = get_platform()
    return platform == Platforms.Linux


def is_mac():
    """
    Check to see if current platform is Mac
    :return: bool
    """
    platform = get_platform()
    return platform == Platforms.Mac


def is_windows():
    """
    Check to see if current platform is Windows
    :return: bool
    """
    platform = get_platform()
    return platform == Platforms.Windows


def get_user(lower=True):
    """
    Returns the current user
    :param lower: bool
    :return: str
    """
    username = getpass.getuser()
    if lower:
        return username.lower()
    else:
        return username


def get_permission(filepath):
    """
    Returns the current permission level
    :param filepath: str
    """
    if os.access(filepath, os.R_OK | os.W_OK | os.X_OK):
        return True
    try:
        os.chmod(filepath, 509)
        return True
    except Exception:
        return False


def init_env_var(name):
    """
    Initializes a new environment variable if the variable does not exists.
    If it does not exists, nothing happens
    :param name: str, name of the new environment variable
    """
    if name not in os.environ:
        os.environ[name] = ''


def set_env_var(name, value):
    """
    Set the value of an environment variable
    :param name: str, name of the environment variable to set
    :param value: variant, value to initialize environment variable with, empty string by default
    """
    if name not in os.environ:
        init_env_var(name)
    try:
        os.environ[name] = str(value)
    except Exception as e:
        import traceback
        print('{} | {} | name: {} | value: {}'.format(str(e), traceback.format_exc(), name, value))


def get_env_var(name):
    """
    Returns the value of an environment variable
    :param name: str, name of the environment variable
    """
    if name in os.environ:
        return os.environ[name]


def append_env_var(name, value):
    """
    Append string value to the end of the environment variable
    :param name: str, name of the environment variable to set
    :param value: variant, value to initialize environment variable with, empty string by default
    """
    env_value = get_env_var(name=name)
    try:
        env_value += str(value)
    except Exception:
        pass

    set_env_var(name=name, value=env_value)


def get_system_config_directory():
    """
    Returns platform specific configuration directory
    """
    if sys.platform.startswith('darwin'):
        config_directory = os.path.join(os.path.expanduser('~'), 'Library', 'Preferences')
    else:
        if os.name == 'nt':
            config_directory = os.getenv('APPDATA') or os.path.expanduser('~')
        else:
            config_directory = os.getenv('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config')
    return config_directory


def open_folder(path):
    """
    Open folder using OS default settings
    :param path: str, folder path we want to open
    """
    if sys.platform.startswith('darwin'):
        subprocess.Popen(['open', path])
    else:
        if os.name == 'nt':
            os.startfile(path)
        else:
            if os.name == 'posix':
                subprocess.Popen(['xdg-open', path])
            else:
                raise NotImplementedError('OS not supported: {}'.format(os.name))


def open_file(file_path):
    """
    Open file using OS default settings
    :param file_path: str, file path we want to open
    """
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', file_path))
    else:
        if os.name == 'nt':
            os.startfile(file_path)
        else:
            if os.name == 'posix':
                subprocess.call(('xdg-open', file_path))
            else:
                raise NotImplementedError('OS not supported: {}'.format(os.name))


def machine_info():
    """
    Returns dictionary with information about the current machine
    :return: dict
    """
    machine_dict = {'pythonVersion':sys.version, 
     'node':platform.node(), 
     'OSRelease':platform.release(), 
     'OSVersion':platform.platform(), 
     'processor':platform.processor(), 
     'machineType':platform.machine(), 
     'env':os.environ, 
     'syspaths':sys.path, 
     'executable':sys.executable}
    return machine_dict


def get_architecture():
    """
    Returns architecture of current OS
    :return: str
    """
    if get_platform() == Platforms.Mac:
        if sys.maxsize > 4294967296:
            return '64bit'
        else:
            return '32bit'
    else:
        return platform.architecture()[0]