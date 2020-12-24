# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ialbert/web/pyblue-central/pyblue/__init__.py
# Compiled at: 2019-04-02 09:13:54
# Size of source mod 2**32: 263 bytes
import sys
VERSION = '2019.04.02'
CURRENT_VERSION = sys.version_info
REQUIRED_VERSION = (3, 6)
if CURRENT_VERSION < REQUIRED_VERSION:
    sys.exit('This program requires Python: {} or above. You have version: {}'.format(REQUIRED_VERSION, CURRENT_VERSION))