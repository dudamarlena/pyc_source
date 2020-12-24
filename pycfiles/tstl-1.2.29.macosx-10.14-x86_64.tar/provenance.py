# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tstl/provenance.py
# Compiled at: 2019-02-11 12:34:52
from __future__ import print_function
import sys, sut, glob
sut = sut.sut()

def abstraction(s):
    if len(s) <= 3:
        return (sut.actionClass(s),)
    else:
        return (
         sut.actionClass(s), s[3])


seedFiles = sys.argv[1]
test = sys.argv[2]
newTestName = sys.argv[3]
abstract = '--abstract' in sys.argv
seeds = []
for f in glob.glob(seedFiles):
    t = sut.loadTest(f)
    if abstract:
        t = list(map(abstraction, t))
    seeds.append((t, f))

original = sut.loadTest(test)
t = list(original)
if abstract:
    t = list(map(abstraction, t))
pos = 0
possible = []
while pos < len(t):
    relevant = []
    for seed in seeds:
        for i in range(0, len(seed[0])):
            if seed[0][i][0] == t[pos][0]:
                relevant.append((seed, i))

    print(pos, t[pos][0], [ (x[0][1], x[1]) for x in relevant ])
    pos += 1
    possible.append(relevant)

print()
print()
newTest = []
pos = 1
previous = possible[0]
while pos < len(possible):
    endPos = pos
    ok = True
    while ok and endPos < len(possible):
        ok = False
        preImageReduce = [ x for x in possible[endPos] if (
         x[0], x[1] - 1) in previous
                         ]
        if len(preImageReduce) > 0:
            endPos += 1
            ok = True
            previous = preImageReduce
        else:
            print(pos - 1, '-', endPos - 1, [ (x[0][1], x[1]) for x in previous ])
            for i in range(pos - 1, endPos):
                print('    ', i, t[i][0], end=' ')
                if previous != []:
                    annotation = previous[0][0][1] + ':' + str(previous[0][1] - (endPos - 1 - i))
                else:
                    annotation = ''
                print('ANNOTATION:', annotation)
                newTest.append(t[i] + (annotation,))

    if endPos < len(possible):
        previous = possible[endPos]
    pos = endPos + 1

sut.saveTest(newTest, newTestName)