# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/utils.py
# Compiled at: 2015-01-27 08:46:21


def auto_increment(start_value=0):
    """Returns an iterator over an auto increment value."""
    value = start_value - 1
    while True:
        value += 1
        yield value