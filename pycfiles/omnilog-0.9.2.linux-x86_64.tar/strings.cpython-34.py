# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/strings.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 1101 bytes


class Strings(object):
    APP_NAME = 'Omnilog'
    APP_RESTARTING = 'Restarting app ...'
    APP_SHUTDOWN = 'Shuting down app ...'
    CONFIG_ERROR = 'Config error , check config. Shutting down ...'
    CONFIG_CHANGE = 'Config changes detected ... setting new config.'
    CONFIG_FILE_ERROR = 'Cannot load config.'
    CONFIG_CHANGES = 'Config changes detected ... setting new config.'
    SSH_ERROR = 'SSH error , check config.'
    KEYBOARD_INTERRUPTION = 'keyboard interruption detected.'
    UNHANDLED_EXCEPTION = 'UNHANDLED EXCEPTION .... shuting down....'
    SUB_SYSTEM_START = 'Starting subsystem'
    IO_ERROR = 'IO error detected.Shutting down.'
    LOG_PROCESSED = 'Log processed.'
    IPC_RECEIVED = ' - IPC - Received '
    PARSER_VALID_LOG_REACHED = 'Valid log reached, passing it to queue.'
    WEBPANEL_PUBLISH = 'Valid log reached, passing it to queue.'
    SKELETON_DIR_CREATED = 'Skeleton created in your home dir ... shutting down ...'
    SKELETON_DIR = 'Skeleton exists, aborting ...'
    SKELETON_URL_ERROR = 'Cannot contact external resources for skeleton ... go github.'