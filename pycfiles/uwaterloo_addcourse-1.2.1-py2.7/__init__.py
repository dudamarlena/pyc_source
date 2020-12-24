# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/__init__.py
# Compiled at: 2015-04-27 10:39:28
"""Repeatedly ask QUEST to add you into a particular course."""
from .version import __author__, __version__, __credits__

def addcourse(user, password, classlist):
    """Repeatedly query QUEST to add classes from classlist until one of
    them works.

    """
    from .course_adder import addcourse as _addcourse
    return _addcourse(user, password, classlist)


def numbers(course):
    """Query uwaterloo.ca for a list of class numbers that correspond to
    the lecture sections of course.

    """
    from .class_numbers import numbers as _numbers
    return _numbers(course)