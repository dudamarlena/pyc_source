# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/pkg_resources/py31compat.py
# Compiled at: 2019-09-10 15:18:29
import os, errno, sys

def _makedirs_31(path, exist_ok=False):
    try:
        os.makedirs(path)
    except OSError as exc:
        if not exist_ok or exc.errno != errno.EEXIST:
            raise


needs_makedirs = sys.version_info < (3, 2, 5) or (3, 3) <= sys.version_info < (3, 3,
                                                                               6) or (3,
                                                                                      4) <= sys.version_info < (3,
                                                                                                                4,
                                                                                                                1)
makedirs = _makedirs_31 if needs_makedirs else os.makedirs