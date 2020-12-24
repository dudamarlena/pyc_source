# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tstl/markov.py
# Compiled at: 2019-02-11 12:34:52
from __future__ import print_function
import sys, os
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)
if '--help' not in sys.argv:
    import sut as SUT

def main():
    if '--help' in sys.argv:
        print('Usage:  tstl_markov <outfile> <prefix size> <test files> [--notRaw]')
        print('Options:')
        print(' --notRaw:      corpus files are not raw TSTL tests, but action classes')
        sys.exit(0)
    sut = SUT.sut()
    classes = []
    for a in sut.actions():
        if sut.actionClass(a) not in classes:
            classes.append(sut.actionClass(a))

    n = int(sys.argv[2])
    outfile = sys.argv[1]
    corpfiles = sys.argv[3:]
    corpfiles = [ x for x in corpfiles if x != '--notRaw' ]
    tests = []
    test = []
    for f in corpfiles:
        for l in open(f):
            if '--notRaw' in sys.argv:
                test.append(l[:-1])
            else:
                test.append(sut.actionClass(sut.playable(l[:-1])))

        if test != []:
            tests.append(test)
            test = []

    chains = {}
    for t in tests:
        for pos in range(n + 1, len(t)):
            prefix = tuple(t[pos - n:pos])
            if prefix not in chains:
                chains[prefix] = []
            chains[prefix].append(t[pos])

    mout = open(outfile, 'w')
    mout.write(str(n) + '\n')
    for c in chains:
        print('PREFIX:', c)
        mout.write('START CLASS\n')
        for ac in c:
            mout.write(ac + '\n')

        mout.write('END CLASS\n')
        counts = {}
        total = 0.0
        for suffix in chains[c]:
            total += 1
            if suffix not in counts:
                counts[suffix] = 0
            counts[suffix] += 1

        for suffix in counts:
            print(suffix, counts[suffix] / total)
            mout.write(str(counts[suffix] / total) + ' %%%% ' + suffix + '\n')

    mout.close()