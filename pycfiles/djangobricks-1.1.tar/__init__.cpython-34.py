# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-bricks/djangobricks/__init__.py
# Compiled at: 2014-11-12 11:57:53
# Size of source mod 2**32: 153 bytes
"""
When you need a wall.
"""
VERSION = (1, 0, 0)

def get_version():
    """Returns the version as a string."""
    return '.'.join(map(str, VERSION))