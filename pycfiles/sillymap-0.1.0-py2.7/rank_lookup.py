# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/rank_lookup.py
# Compiled at: 2017-04-04 08:29:05
from collections import defaultdict
import warnings

class Rank:
    """Rank table corresponding to http://alexbowe.com/fm-index/ except 0-indexed.

    The rank(i,c) is the number of occurencies of c within text[0:(i+1)]

    public methods:
    add_text(text) -- initialize the rank for text.
    rank(i,c) -- returns rank of character c in intercal [0:i] 

    ex:

    rank = Rank()
    rank.add_text("ipssm$pissii")
    rank.rank(-1,i) = 0
    rank.rank("ipssm$pissii")[0,i] = 1
    rank.rank("ipssm$pissii")[11,s] = 4
    """

    def __init__(self):
        self.rank_dict = {}
        self.constructed = False

    def add_text(self, text):
        char_count = defaultdict(int)
        for i, c in enumerate(text):
            char_count[c] += 1
            for char, count in char_count.items():
                if i not in self.rank_dict:
                    self.rank_dict[i] = {}
                self.rank_dict[i][char] = count

        self.constructed = True

    def rank(self, i, c):
        if not self.constructed:
            warnings.warn('Fetched rank before text was added, this will always return 0')
        if i not in self.rank_dict:
            return 0
        if c not in self.rank_dict[i]:
            return 0
        return self.rank_dict[i][c]