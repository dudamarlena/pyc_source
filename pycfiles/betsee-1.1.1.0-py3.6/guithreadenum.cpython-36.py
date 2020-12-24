# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/thread/guithreadenum.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 2017 bytes
"""
Low-level **thread enumeration** (e.g., :class:`enum.Enum` subclass describing
different types of multithreading behaviour) functionality.
"""
from betse.util.type.enums import make_enum
ThreadWorkerState = make_enum(class_name='ThreadWorkerState',
  member_names=('IDLE', 'RUNNING', 'PAUSED', 'DELETED'))