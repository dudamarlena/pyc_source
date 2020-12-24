# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/scoring/scorer.py
# Compiled at: 2011-02-23 19:11:48


class Scorer(object):
    """Scorer Class

Base class for Scorer object classes, such as Choi and GodelPositional.
"""

    def __init__(self, *arg, **kwarg):
        pass

    def __call__(self, v):
        """Dummy function that will always return ``None``.  The `scored` method
will, by default, omit rows for which the score is ``None``, so using this
will likely result in an empty ``Matrics`` instance.
"""
        return