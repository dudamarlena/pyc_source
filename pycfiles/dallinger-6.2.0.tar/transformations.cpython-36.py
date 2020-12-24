# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/transformations.py
# Compiled at: 2020-04-24 19:15:49
# Size of source mod 2**32: 1054 bytes
"""
Define custom transformations.

See class Transformation in models.py for the base class Transformation. This
file stores a list of all the subclasses of Transformation made available by
default. Note that they don't necessarily tell you anything about the nature
in which two Info's relate to each other, but if used sensibly they will do so.
"""
from .models import Transformation

class Replication(Transformation):
    __doc__ = 'An instance of one info being identically copied into another.'
    __mapper_args__ = {'polymorphic_identity': 'replication'}


class Mutation(Transformation):
    __doc__ = 'An instance of one info being tranformed into another + mutations.'
    __mapper_args__ = {'polymorphic_identity': 'mutation'}


class Compression(Transformation):
    __doc__ = 'An instance of one info being compressed into another.'
    __mapper_args__ = {'polymorphic_identity': 'compression'}


class Response(Transformation):
    __doc__ = 'An instance of one info being a response to another.'
    __mapper_args__ = {'polymorphic_identity': 'response'}