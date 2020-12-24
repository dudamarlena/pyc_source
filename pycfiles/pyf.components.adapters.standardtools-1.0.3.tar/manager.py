# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/componentized/error/manager.py
# Compiled at: 2011-02-05 06:39:28


class ManagerError(Exception):
    """the base class for all exceptions raised by Nostromo Manager
    """


class DataPathError(ManagerError):
    pass