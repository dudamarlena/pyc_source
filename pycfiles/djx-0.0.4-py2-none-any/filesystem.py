# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/utils/filesystem.py
# Compiled at: 2019-02-14 00:35:06
import os, os.path
from pip._internal.utils.compat import get_path_uid

def check_path_owner(path):
    if not hasattr(os, 'geteuid'):
        return True
    else:
        previous = None
        while path != previous:
            if os.path.lexists(path):
                if os.geteuid() == 0:
                    try:
                        path_uid = get_path_uid(path)
                    except OSError:
                        return False

                    return path_uid == 0
                else:
                    return os.access(path, os.W_OK)

            else:
                previous, path = path, os.path.dirname(path)

        return False