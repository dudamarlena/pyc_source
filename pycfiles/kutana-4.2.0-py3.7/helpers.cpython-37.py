# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/helpers.py
# Compiled at: 2020-05-02 08:54:53
# Size of source mod 2**32: 299 bytes
import os.path

def get_path(root, path):
    """
    Shortcut for ``os.path.join(os.path.dirname(root), path)``.

    :param root: root path
    :param path: path to file or folder
    :returns: path to file or folder relative to root
    """
    return os.path.join(os.path.dirname(root), path)