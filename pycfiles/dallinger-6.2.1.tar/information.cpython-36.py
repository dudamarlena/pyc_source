# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/information.py
# Compiled at: 2020-04-26 19:37:24
# Size of source mod 2**32: 452 bytes
"""Subclasses of information."""
from .models import Info

class Gene(Info):
    __doc__ = 'A gene.'
    __mapper_args__ = {'polymorphic_identity': 'gene'}


class Meme(Info):
    __doc__ = 'A meme.'
    __mapper_args__ = {'polymorphic_identity': 'meme'}


class State(Info):
    __doc__ = 'A state.'
    __mapper_args__ = {'polymorphic_identity': 'state'}


class TrackingEvent(Info):
    __doc__ = 'A state.'
    __mapper_args__ = {'polymorphic_identity': 'tracking'}