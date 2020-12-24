# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/log.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1329 bytes
import sys, logging
from pocsuite3.lib.core.enums import CUSTOM_LOGGING
logging.addLevelName(CUSTOM_LOGGING.SYSINFO, '*')
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, '+')
logging.addLevelName(CUSTOM_LOGGING.ERROR, '-')
logging.addLevelName(CUSTOM_LOGGING.WARNING, '!')
LOGGER = logging.getLogger('pocsuite')
LOGGER_HANDLER = None
try:
    from pocsuite3.thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
    disableColor = False
    for argument in sys.argv:
        if 'disable-col' in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName('*')] = (None, 'cyan', False)
        LOGGER_HANDLER.level_map[logging.getLevelName('+')] = (None, 'green', False)
        LOGGER_HANDLER.level_map[logging.getLevelName('-')] = (None, 'red', False)
        LOGGER_HANDLER.level_map[logging.getLevelName('!')] = (None, 'yellow', False)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter('\r[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S')
LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)