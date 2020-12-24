# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/constants.py
# Compiled at: 2016-03-06 16:56:09
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