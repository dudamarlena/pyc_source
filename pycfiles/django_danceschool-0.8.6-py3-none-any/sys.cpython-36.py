# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/utils/sys.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 451 bytes
"""
This file contains helper functions used at the time that various apps are loaded
"""
import sys

def isPreliminaryRun():
    """
    Check the arguments passed at runtime to ensure that this
    program is not being run to perform migrations or load data.
    """
    prelim_params = [
     'loaddata', 'makemigrations', 'migrate']
    for param in prelim_params:
        if param in sys.argv:
            return True

    return False