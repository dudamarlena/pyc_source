# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/neorg/config.py
# Compiled at: 2011-06-07 15:12:54
import os
from neorg import NEORG_HIDDEN_DIR, CONFIG_FILE

class DefaultConfig(object):
    DEBUG = False
    DATABASE = '%(neorg)s/neorg.db'
    DATADIRPATH = '%(root)s'
    SEARCHINDEX = '%(neorg)s/searchindex'
    SECRET_KEY = None


def neorgpath(dirpath):
    return os.path.join(dirpath, NEORG_HIDDEN_DIR)


def confpath(dirpath):
    return os.path.join(dirpath, NEORG_HIDDEN_DIR, CONFIG_FILE)


def expandall(path):
    return os.path.expandvars(os.path.expanduser(path))


def expand_magic_words(config):
    magic = {'neorg': config['NEORG_DIR'], 
       'root': config['NEORG_ROOT']}
    for key in ['DATABASE', 'DATADIRPATH', 'HELPDIRPATH', 'SEARCHINDEX']:
        if key in config:
            config[key] = expandall(config[key] % magic)


def set_neorg_dir(config, dirpath):
    config.update(NEORG_ROOT=dirpath, NEORG_DIR=os.path.join(dirpath, NEORG_HIDDEN_DIR))


def load_config(app, dirpath=None):
    if dirpath is None:
        dirpath = '.'
    dirpath = os.path.abspath(dirpath)
    app.config.from_pyfile(confpath(dirpath))
    set_config(app.config, dirpath)
    return


def set_config(config, dirpath):
    set_neorg_dir(config, dirpath)
    config['DATADIRURL'] = '/_data'
    expand_magic_words(config)


DEFAULT_CONFIG_FILE = "SECRET_KEY = 'development key'\nDATADIRPATH = '%(root)s'\n"

def init_config_file(dirpath=None):
    if dirpath is None:
        dirpath = '.'
    dirpath = os.path.abspath(dirpath)
    _neorgpath = neorgpath(dirpath)
    if not os.path.isdir(_neorgpath):
        os.mkdir(_neorgpath, 448)
    file(confpath(dirpath), 'w').write(DEFAULT_CONFIG_FILE)
    return