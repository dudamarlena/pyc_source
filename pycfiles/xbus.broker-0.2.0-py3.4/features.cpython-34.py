# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/core/features.py
# Compiled at: 2016-06-27 03:37:38
# Size of source mod 2**32: 182 bytes
"""Features Xbus recipients (workers / consumers) can support.
"""
from enum import Enum
RecipientFeature = Enum('RecipientFeature', 'clearing immediate_reply ')