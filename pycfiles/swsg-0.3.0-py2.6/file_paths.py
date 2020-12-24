# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/swsg/file_paths.py
# Compiled at: 2010-11-29 08:26:31
from os import getenv, path
XDG_DATA_HOME = getenv('XDG_DATA_HOME', path.expanduser(path.join('~', '.local', 'share')))
XDG_CONFIG_HOME = getenv('XDG_CONFIG_HOME', path.expanduser(path.join('~', '.config')))
GLOBAL_CONFIGFILE = path.join(XDG_CONFIG_HOME, 'swsg')
PROJECT_DATA_DIR = path.join(XDG_DATA_HOME, 'swsg')
LOGFILE = path.join(PROJECT_DATA_DIR, 'swsg.log')
DEFAULT_PROJECTS_FILE_NAME = path.join(PROJECT_DATA_DIR, 'projects.shelve')