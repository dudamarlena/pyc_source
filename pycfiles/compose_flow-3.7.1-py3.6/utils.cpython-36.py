# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 408 bytes
import os
MODULE_DIR = os.path.dirname(__file__)

def get_content(relative_path: str) -> str:
    """
    Returns the content of the given relative path

    Args:
        relative_path: the path relative to the tests/files/ directory

    Returns:
        the file contents
    """
    full_path = os.path.join(MODULE_DIR, 'files', relative_path)
    with open(full_path) as (fh):
        return fh.read()