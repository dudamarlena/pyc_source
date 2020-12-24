# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/split_explicit_groups.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.textutils import find_first_level_groups
from guessit.patterns import group_delimiters
import functools, logging
log = logging.getLogger(__name__)

def process(mtree):
    """return the string split into explicit groups, that is, those either
    between parenthese, square brackets or curly braces, and those separated
    by a dash."""
    for c in mtree.children:
        groups = find_first_level_groups(c.value, group_delimiters[0])
        for delimiters in group_delimiters:
            flatten = lambda l, x: l + find_first_level_groups(x, delimiters)
            groups = functools.reduce(flatten, groups, [])

        c.split_on_components(groups)