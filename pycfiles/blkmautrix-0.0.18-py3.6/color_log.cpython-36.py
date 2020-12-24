# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/color_log.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1805 bytes
from logging import Formatter, LogRecord
from copy import copy
PREFIX = '\x1b['
LEVEL_COLORS = {'DEBUG':'37m', 
 'INFO':'36m', 
 'WARNING':'33;1m', 
 'ERROR':'31;1m', 
 'CRITICAL':f"37;1m{PREFIX}41m"}
MAU_COLOR = PREFIX + '32m'
AIOHTTP_COLOR = PREFIX + '36m'
MXID_COLOR = PREFIX + '33m'
RESET = '\x1b[0m'

class ColorFormatter(Formatter):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def _color_name(self, module: str) -> str:
        as_api = 'mau.as.api'
        if module.startswith(as_api):
            return f"{MAU_COLOR}{as_api}{RESET}.{MXID_COLOR}{module[len(as_api) + 1:]}{RESET}"
        if module.startswith('mau.'):
            try:
                next_dot = module.index('.', len('mau.'))
                return MAU_COLOR + module[:next_dot] + RESET + '.' + MXID_COLOR + module[next_dot + 1:] + RESET
            except ValueError:
                return MAU_COLOR + module + RESET

        else:
            if module.startswith('aiohttp'):
                return AIOHTTP_COLOR + module + RESET
            return module

    def format(self, record):
        colored_record = copy(record)
        colored_record.name = self._color_name(record.name)
        try:
            levelname = record.levelname
            colored_record.levelname = PREFIX + LEVEL_COLORS[levelname] + levelname + RESET
        except KeyError:
            pass

        return super().format(colored_record)