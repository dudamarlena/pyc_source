# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/example.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1049 bytes
"""
Example-related classes.

@author: anze.vavpetic@ijs.si
"""

class Example:
    __doc__ = '\n    Represents an example with its score, label, id and annotations.\n    '
    ClassLabeled = 'class'
    Ranked = 'ranked'

    def __init__(self, id, label, score, annotations=[], weights={}):
        self.id = id
        self.label = label
        self.score = score
        if type(score) not in [str]:
            self.target_type = Example.Ranked
        else:
            self.target_type = Example.ClassLabeled
        self.annotations = annotations
        self.weights = weights

    def __str__(self):
        if self.target_type == Example.Ranked:
            return '<id=%d, score=%.5f, label=%s>' % (self.id,
             self.score,
             self.label)
        return '<id=%d, class=%s, label=%s>' % (self.id,
         self.score,
         self.label)