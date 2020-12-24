# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/verbout.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 672 bytes
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import DEBUG as verbose

def verbout(stat, content_info):
    """
    This module is for giving a verbose
                output.
    """
    if verbose:
        print(stat + content_info)