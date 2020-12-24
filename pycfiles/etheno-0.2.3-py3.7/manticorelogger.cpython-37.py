# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/manticorelogger.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 886 bytes
ETHENO_LOGGER = None

@property
def manticore_verbosity():
    return ETHENO_LOGGER.log_level


@property
def DEFAULT_LOG_LEVEL():
    return ETHENO_LOGGER.log_level


def set_verbosity(setting):
    pass


all_loggers = set()