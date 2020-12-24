# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/importance_score_map.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2152 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from enum import Enum

class DetailLevel(Enum):
    __doc__ = 'Detail level of the presentation of a node in the graph.'
    highest = 1
    very_high = 2
    high = 3
    medium = 4
    low = 5
    lowest = 6


class ImportanceScoreMap:
    __doc__ = 'Turn NodeImportance into a score based on DetailLevel.\n\n    The score says how visible object with given importance should be on\n    given detail level. The larger the number, the more prominent the object.\n\n    The detail and importance values are aligned like this:\n\n    detail        importance\n    ------        ----------\n    highest       lowest\n    very_high     very_low\n    high          low\n    medium        normal\n    low           n/a\n    lowest        n/a\n\n    This means that when, e.g., detail is set to:\n\n    - `lowest`, then the consecutive importance values receive the following\n       scores: `lowest`: -5, `very_low`: -4, `low`: -3, `normal`: -2\n    - `medium`, then the consecutive importance values receive the following\n       scores: `lowest`: -3, `very_low`: -2, `low`: -1, `normal`: 0\n    - `very_high`, then the consecutive importance values receive the following\n       scores: `lowest`: -1, `very_low`: 0, `low`: 1, `normal`: 2\n    '

    def __init__(self, detail_level):
        """Args:
            detail_level (DetailLevel):
        """
        self._ImportanceScoreMap__detail = detail_level

    def get_score(self, importance):
        """Args:
            importance (NodeImportance):
        """
        return importance.value - self._ImportanceScoreMap__detail.value