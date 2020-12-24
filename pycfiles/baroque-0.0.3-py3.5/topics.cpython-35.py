# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/exceptions/topics.py
# Compiled at: 2017-03-13 15:18:21
# Size of source mod 2**32: 153 bytes


class UnregisteredTopicError(Exception):
    __doc__ = 'Raised when attempting to publish events on a topic that is not registered\n    on the broker'