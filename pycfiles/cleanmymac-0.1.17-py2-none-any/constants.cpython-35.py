# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/constants.py
# Compiled at: 2016-03-06 16:56:09
# Size of source mod 2**32: 1555 bytes
TARGET_ENTRY_POINT = 'cleanmymac.target'
GLOBAL_CONFIG_FILE = '.cleanmymac.yaml'
TYPE_TARGET_CMD = 'cmd'
TYPE_TARGET_DIR = 'dir'
VALID_TARGET_TYPES = frozenset([
 TYPE_TARGET_DIR,
 TYPE_TARGET_CMD])
UNIT_KB = 1024
UNIT_MB = UNIT_KB * 1024
UNIT_GB = UNIT_MB * 1024
PROGRESSBAR_ADVANCE_DELAY = 0.25
DESCRIBE_CLEAN = 'clean'
DESCRIBE_UPDATE = 'update'
VALID_DESCRIBE_MESSAGES = frozenset([
 DESCRIBE_CLEAN,
 DESCRIBE_UPDATE])