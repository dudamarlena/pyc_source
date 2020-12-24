# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sorno/fileutil.py
# Compiled at: 2019-08-09 12:21:44
# Size of source mod 2**32: 498 bytes
"""
Utility functions for dealing with files
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import magic

def is_text_file(filepath):
    """
    Check if a file is a text file using libmagic.

    Args:
        filepath: A string. The path to the file being inspected.

    Returns:
        True if the file is a text file.
    """
    f = magic.from_file(filepath)
    return 'text' in f