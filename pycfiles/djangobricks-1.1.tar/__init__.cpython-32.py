# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-bricks/djangobricks/__init__.py
# Compiled at: 2015-01-27 06:21:36
"""
When you need a wall.
"""
VERSION = (1, 1, 0)

def get_version():
    """Returns the version as a string."""
    return '.'.join(map(str, VERSION))