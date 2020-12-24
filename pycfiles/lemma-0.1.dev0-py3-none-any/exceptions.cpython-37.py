# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/lemma/lemma/exceptions.hy
# Compiled at: 2020-04-11 21:00:31
# Size of source mod 2**32: 142 bytes


class LeError(Exception):
    pass


class LeRuntimeError(LeError):
    pass


class LeSyntaxError(LeError):
    pass


class LeEquationError(LeError):
    pass