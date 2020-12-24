# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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