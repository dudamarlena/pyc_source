# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\hiscore.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1841 bytes
from __future__ import division, print_function, unicode_literals
__all__ = [
 'hiscore']

class HiScoreData(object):
    POINTS, NAME, LVL = range(3)
    HISCORE_FILENAME = 'hi_scores.txt'
    MAX = 10

    def __init__(self):
        super(HiScoreData, self).__init__()
        self.load()

    def load(self):
        self.hi_scores = []
        try:
            f = open(self.HISCORE_FILENAME)
            for line in f.readlines():
                if line.startswith('#'):
                    pass
                else:
                    score, name, lvl = line.split(',')
                    self.hi_scores.append((int(score), name, int(lvl)))

            f.close()
        except IOError:
            pass

    def save(self):
        try:
            f = open(self.HISCORE_FILENAME, 'w')
            for i in self.hi_scores:
                f.write('%d,%s,%d\n' % (i[0], i[1], i[2]))

            f.close()
        except Exception as e:
            try:
                print('Could not save hi scores')
                print(e)
            finally:
                e = None
                del e

    def add(self, score, name, lvl):
        for l in name:
            if not l.isalnum():
                name = name.replace(l, '_')
            self.hi_scores.append((int(score), name, int(lvl)))
            self.hi_scores.sort()
            self.hi_scores.reverse()
            self.hi_scores = self.hi_scores[:self.MAX]
            self.save()

    def is_in(self, score):
        if len(self.hi_scores) < self.MAX:
            return True
        if score > self.hi_scores[(-1)][0]:
            return True
        return False

    def get(self, max=10):
        return self.hi_scores[:max]


hiscore = HiScoreData()