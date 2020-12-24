# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/path_part.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 167 bytes


class PathPartDdv:
    __doc__ = '\n    The relative path that follows the root path of the `PathDdv`.\n    '

    def value(self) -> str:
        raise NotImplementedError()