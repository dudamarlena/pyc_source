# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/util/environment.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 2291 bytes
import os, sys
settings = {}
IS_WIN = sys.platform.startswith('win')
IS_OSX = sys.platform == 'darwin'
IS_LINUX = sys.platform == 'linux'

def infer_app_data_dir():
    home = os.path.expanduser('~')
    app_data_dir_suffix = ['OT One App 2', 'otone_data']
    app_data = None
    if IS_OSX:
        app_data = os.path.join(home, 'Library', 'Application Support')
    else:
        if IS_WIN:
            app_data = os.path.join(os.environ.get('APPDATA', ''))
        if IS_LINUX:
            app_data = os.path.join(home, '.config')
        return app_data or os.getcwd()
    app_data = (os.path.join)(app_data, *app_data_dir_suffix)
    if os.path.exists(app_data):
        return app_data
    return os.getcwd()


def refresh():
    """
    Refresh environment.settings dict
    """
    APP_DATA_DIR = os.environ.get('APP_DATA_DIR', infer_app_data_dir())
    settings.clear()
    settings.update({'APP_DATA_DIR':APP_DATA_DIR, 
     'LOG_DIR':os.path.join(APP_DATA_DIR, 'logs'), 
     'LOG_FILE':os.path.join(APP_DATA_DIR, 'logs', 'api.log'), 
     'CONTAINERS_DIR':os.path.join(APP_DATA_DIR, 'containers'), 
     'CONTAINERS_FILE':os.path.join(APP_DATA_DIR, 'containers', '_containers_create.json'), 
     'CALIBRATIONS_DIR':os.path.join(APP_DATA_DIR, 'calibrations'), 
     'CALIBRATIONS_FILE':os.path.join(APP_DATA_DIR, 'calibrations', 'calibrations.json'), 
     'APP_IS_ALIVE_URL':'http://localhost:31950'})
    return settings


def get_path(key):
    """
    For a given key returns a full path and
    creates the path if missing. The caller is guaranteed
    the path exists if exception is not thrown.

    For *_DIR it will create a directory, for *_FILE it will
    create a directory tree to the file. Throws exception if neither.
    """
    if key not in settings:
        raise ValueError('Key "{}" not found in environment settings'.format(key))
    elif key.endswith('_DIR'):
        path = settings[key]
    else:
        if key.endswith('_FILE'):
            path, _ = os.path.split(settings[key])
        else:
            raise ValueError('Expected key suffix as _DIR or _FILE. "{}" received'.format(key))
    if not os.path.exists(path):
        os.makedirs(path)
    return settings[key]


refresh()