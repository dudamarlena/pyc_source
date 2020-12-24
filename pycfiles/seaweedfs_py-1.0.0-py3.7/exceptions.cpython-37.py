# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/seaweedfs/exceptions.py
# Compiled at: 2019-11-17 02:23:02
# Size of source mod 2**32: 383 bytes
"""
@author:    george wang
@datetime:  2019-11-17
@file:      exception.py
@contact:   georgewang1994@163.com
@desc:      exception of seaweedfs
"""

class SeaweedfsError(Exception):
    pass


class JSONDecodeError(SeaweedfsError):
    pass


class PostError(SeaweedfsError):
    pass


class ParamNoneError(SeaweedfsError):
    pass