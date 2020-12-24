# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rdisq/payload.py
# Compiled at: 2020-03-07 02:12:19
# Size of source mod 2**32: 245 bytes
__author__ = 'smackware'
from collections import namedtuple
RequestPayload = namedtuple('RequestPayload', 'task_id timeout args kwargs')
ResponsePayload = namedtuple('ResponsePayload', 'returned_value raised_exception processing_time_seconds')