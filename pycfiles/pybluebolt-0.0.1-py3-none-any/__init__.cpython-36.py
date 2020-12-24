# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ialbert/web/pyblue-central/pyblue/__init__.py
# Compiled at: 2019-04-02 09:13:54
# Size of source mod 2**32: 263 bytes
import sys
VERSION = '2019.04.02'
CURRENT_VERSION = sys.version_info
REQUIRED_VERSION = (3, 6)
if CURRENT_VERSION < REQUIRED_VERSION:
    sys.exit('This program requires Python: {} or above. You have version: {}'.format(REQUIRED_VERSION, CURRENT_VERSION))