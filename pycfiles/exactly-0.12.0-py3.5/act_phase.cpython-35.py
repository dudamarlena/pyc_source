# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/processing/act_phase.py
# Compiled at: 2019-01-29 09:32:34
# Size of source mod 2**32: 371 bytes
from exactly_lib.test_case.actor import Actor

class ActPhaseSetup(tuple):
    __doc__ = '\n    TODO: Believe that the Actor can completely replace this class\n    (since the other members probably will be refactored away)\n    '

    def __new__(cls, actor: Actor):
        return tuple.__new__(cls, (actor,))

    @property
    def actor(self) -> Actor:
        return self[0]