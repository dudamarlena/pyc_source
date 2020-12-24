# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/__init__.py
# Compiled at: 2018-05-07 05:29:41
# Size of source mod 2**32: 344 bytes
VERSION = (1, 3, 2, 'final', 0)

def get_version():
    """
    :return:
    """
    from tingyun.version import get_version
    return get_version(VERSION)