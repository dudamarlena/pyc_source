# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/utils/marker_files.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 595 bytes
import os.path
DELETE_MARKER_MESSAGE = 'This file is placed here by pip to indicate the source was put\nhere by pip.\n\nOnce this package is successfully installed this source code will be\ndeleted (unless you remove this file).\n'
PIP_DELETE_MARKER_FILENAME = 'pip-delete-this-directory.txt'

def write_delete_marker_file(directory):
    """
    Write the pip delete marker file into this directory.
    """
    filepath = os.path.join(directory, PIP_DELETE_MARKER_FILENAME)
    with open(filepath, 'w') as (marker_fp):
        marker_fp.write(DELETE_MARKER_MESSAGE)