# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jordansuchow/Dropbox/Berkeley/Projects/Current/Wallace/wallace/information.py
# Compiled at: 2016-07-28 05:24:16
"""Subclasses of information."""
from .models import Info

class Gene(Info):
    """A gene."""
    __mapper_args__ = {'polymorphic_identity': 'gene'}


class Meme(Info):
    """A meme."""
    __mapper_args__ = {'polymorphic_identity': 'meme'}


class State(Info):
    """A state."""
    __mapper_args__ = {'polymorphic_identity': 'state'}