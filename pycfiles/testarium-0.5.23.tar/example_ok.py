# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/makseq/Data/PROJECTS/testarium/unittests/example_ok.py
# Compiled at: 2018-11-18 10:32:21
"""
Testarium
Copyright (C) 2014 Maxim Tkachenko

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import testarium, testarium.score.fafr, random, json

@testarium.experiment.set_run
def MyRun(commit):
    c = commit.config
    dir = commit.dir
    pos = open(dir + '/pos.txt', 'w')
    neg = open(dir + '/neg.txt', 'w')
    for i in xrange(100):
        pos.write(str(random.random()) + '\n')

    for i in xrange(100):
        neg.write(str(random.random()) + '\n')

    return 0


@testarium.experiment.set_score
def MyScore(commit):
    d = testarium.score.fafr.Score(commit.dir)
    d['test'] = 1
    return d


def MyPrint(commit):
    try:
        a = str(commit.config['a'])
    except:
        a = ''

    score = str(commit.desc['score'])
    return (['name', 'a', 'score'], [commit.name, 'file:.testarium/testarium.json', score])


@testarium.testarium.set_compare
def MyCompare(self, other):
    if self._init:
        if self.desc['score'] > other.desc['score']:
            return -1
        else:
            if self.desc['score'] < other.desc['score']:
                return 1
            return 0

    else:
        return -1


def main():
    testarium.testarium.best_score_is_min()
    testarium.main()


if __name__ == '__main__':
    main()