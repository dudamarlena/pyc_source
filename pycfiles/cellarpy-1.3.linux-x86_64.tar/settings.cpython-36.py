# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/settings.py
# Compiled at: 2017-10-28 11:14:16
# Size of source mod 2**32: 2498 bytes
import logging, os
from os import path

def setwritabledirectory(folders):

    def iswritable(directory):
        if not path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                return False

        return os.access(directory, os.W_OK | os.X_OK | os.R_OK)

    for dir in folders:
        if iswritable(dir):
            return dir

    logging.debug('No writable dir was found amongst: ' + str(folders))
    raise Exception('No writable dir was found amongst: ' + str(folders))


def setreadablefile(folders, filename):

    def isreadable(directory, filename):
        if path.isfile(path.join(directory, filename)):
            return os.access(path.join(directory, filename), os.R_OK)
        else:
            return False

    for dir in folders:
        if isreadable(dir, filename):
            return path.join(dir, filename)

    logging.debug('No readable conf file was found amongst: ' + str(folders))
    raise Exception('No readable conf file was found amongst: ' + str(folders))


def load_logfile(logfile=None, dirs=[]):
    fromenv = os.getenv('CELLAR_LOGS', None)
    if fromenv:
        logfile = path.basename(fromenv)
        dirs = [path.dirname(fromenv)]
    log_dir = setwritabledirectory(dirs)
    logging.basicConfig(level=(logging.DEBUG), filename=(path.join(log_dir, logfile)),
      format='%(asctime)s +%(msecs)d [%(process)d] %(levelname)s %(message)s',
      datefmt='%d/%b/%Y:%H:%M:%S')
    logging.debug('Log file start')


def load_settings(settingsfile=None, dirs=[], storage_dirs=[]):
    fromenv = os.getenv('CELLAR_SETTINGS', None)
    if fromenv:
        settingsfile = path.basename(fromenv)
        dirs = [path.dirname(fromenv)]
    fromenv = os.getenv('CELLAR_STORAGE', None)
    if fromenv:
        storage_dirs = fromenv.split(';')
    config_file = setreadablefile(dirs, settingsfile)
    with open(config_file) as (fd):
        import json
        settings = json.load(fd)
    if 'storage' in settings:
        for name, folder in settings['storage'].items():
            settings['storage'][name] = setwritabledirectory([folder] + [path.join(storage, name) for storage in storage_dirs])
            if name == 'database' and settings['sqlite'][name][0] != '/':
                settings['sqlite'][name] = path.join(settings['storage'][name], settings['sqlite'][name])

    logging.debug('Settings loaded')
    return settings