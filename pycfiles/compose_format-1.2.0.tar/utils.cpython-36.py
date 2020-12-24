# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils.py
# Compiled at: 2020-05-06 10:05:57
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