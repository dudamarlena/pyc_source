# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/utils/marker_files.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 741 bytes
import os.path
DELETE_MARKER_MESSAGE = 'This file is placed here by pip to indicate the source was put\nhere by pip.\n\nOnce this package is successfully installed this source code will be\ndeleted (unless you remove this file).\n'
PIP_DELETE_MARKER_FILENAME = 'pip-delete-this-directory.txt'

def has_delete_marker_file(directory):
    return os.path.exists(os.path.join(directory, PIP_DELETE_MARKER_FILENAME))


def write_delete_marker_file(directory):
    """
    Write the pip delete marker file into this directory.
    """
    filepath = os.path.join(directory, PIP_DELETE_MARKER_FILENAME)
    with open(filepath, 'w') as (marker_fp):
        marker_fp.write(DELETE_MARKER_MESSAGE)