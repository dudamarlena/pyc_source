# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_version.py
# Compiled at: 2019-12-31 04:08:59
# Size of source mod 2**32: 303 bytes


def get_version():
    return '10.0.1.0'


def is_objects_java_release():
    try:
        from . import _jsuperpy as supermap
    except ImportError as e:
        try:
            from . import _csuperpy as supermap
        finally:
            e = None
            del e

    if supermap.internal_tag() == 'iobjects-java':
        return True
    return False