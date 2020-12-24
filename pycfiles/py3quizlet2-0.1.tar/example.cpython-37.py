# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/hedwig/core/example.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1049 bytes
__doc__ = '\nExample-related classes.\n\n@author: anze.vavpetic@ijs.si\n'

class Example:
    """Example"""
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