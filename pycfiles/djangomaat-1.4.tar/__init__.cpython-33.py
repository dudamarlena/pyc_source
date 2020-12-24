# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/__init__.py
# Compiled at: 2015-02-03 06:24:56
# Size of source mod 2**32: 211 bytes
"""
Application that optimizes large ordered data set retrieving when using MySql.
"""
VERSION = (1, 3, 1)

def get_version():
    """Returns the version as a string."""
    return '.'.join(map(str, VERSION))