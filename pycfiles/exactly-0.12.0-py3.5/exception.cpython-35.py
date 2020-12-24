# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/exception.py
# Compiled at: 2016-10-05 11:03:11
# Size of source mod 2**32: 184 bytes


class ImplementationError(Exception):

    def __init__(self, message: str):
        self._ImplementationError__message = message

    @property
    def message(self) -> str:
        return self._ImplementationError__message