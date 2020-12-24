# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-logmanager/flask_logmanager/__init__.py
# Compiled at: 2019-07-30 10:51:57
"""
    Module flask_logmanager
"""
__version_info__ = (0, 2, 11)
__version__ = ('.').join([ str(val) for val in __version_info__ ])
__namepkg__ = 'flask-logmanager'
__desc__ = 'Flask LogManager module'
__urlpkg__ = 'https://github.com/fraoustin/flask-logmanager.git'
__entry_points__ = {}
from logging import Logger, getLogger, DEBUG
try:
    from logging import _nameToLevel, _levelToName
    loggingLevel = _nameToLevel
    for k in _levelToName:
        loggingLevel[k] = _levelToName[k]

except:
    from logging import _levelNames as loggingLevel

from logging import getLogger, Logger
loggerDict = Logger.manager.loggerDict
from flask_logmanager.main import *