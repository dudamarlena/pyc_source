# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tstl/tstl_afl.py
# Compiled at: 2019-02-11 12:34:52
from __future__ import print_function
import sys, os, struct, random, afl
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)
if '--help' not in sys.argv:
    import sut as SUT

def makeInt(s):
    try:
        return int(s)
    except BaseException:
        return

    return


def runTest():
    bytesin = os.read(0, 1048576)
    if swarm:
        R = random.Random()
        if len(bytesin) < 4:
            os._exit(0)
        R.seed(struct.unpack('<L', bytesin[0:4])[0])
        sut.standardSwarm(R)
        bytesin = bytesin[4:]
    test = sut.bytesToTest(bytesin)
    for a in test:
        if a[1]():
            if showActions:
                print(sut.prettyName(a[0]))
            ok = sut.safely(a)
            if not noSave and not ok:
                i = 0
                saveFile = 'aflfail.' + str(os.getpid()) + '.' + str(i) + '.test'
                while os.path.exists(saveFile):
                    i += 1
                    saveFile = 'aflfail.' + str(os.getpid()) + '.' + str(i) + '.test'

                sut.saveTest(sut.test(), saveFile)
            assert ok
            checkResult = noCheck or sut.check()
            if not noSave and not checkResult:
                i = 0
                saveFile = 'aflfail.' + str(os.getpid()) + '.' + str(i) + '.test'
                while os.path.exists(saveFile):
                    i += 1
                    saveFile = 'aflfail.' + str(os.getpid()) + '.' + str(i) + '.test'

                sut.saveTest(sut.test(), saveFile)
            if not checkResult:
                raise AssertionError

    if alwaysSave:
        i = 0
        saveFile = 'afltest.' + str(os.getpid()) + '.' + str(i) + '.test'
        while os.path.exists(saveFile):
            i += 1
            saveFile = 'afltest.' + str(os.getpid()) + '.' + str(i) + '.test'

        sut.saveTest(sut.test(), saveFile)


def main():
    global alwaysSave
    global noCheck
    global noSave
    global showActions
    global sut
    global swarm
    if '--help' in sys.argv:
        print('Usage:  tstl_afl [--noCheck] [--swarm] [--verbose] [--showActions] [--noSave] [--alwaysSave]')
        print('Options:')
        print(' --noCheck:      do not run property checks')
        print(' --swarm         use first four bytes to determine a swarm configuration')
        print(' --verbose:      make actions verbose')
        print(' --showActions:  show actions in test')
        print(" --noSave:       don't save failing tests as standard TSTL tests")
        print(' --alwaysSave:   save even non-failing tests')
        sys.exit(0)
    sut = SUT.sut()
    try:
        sut.stopCoverage()
    except BaseException:
        pass

    sut.restart()
    swarm = '--swarm' in sys.argv
    showActions = '--showActions' in sys.argv
    if '--verbose' in sys.argv:
        sut.verbose(True)
    noSave = '--noSave' in sys.argv
    alwaysSave = '--alwaysSave' in sys.argv
    noCheck = '--noCheck' in sys.argv
    persist = '--persist' in sys.argv
    if not persist:
        afl.init()
        runTest()
    else:
        while afl.loop():
            runTest()
            sut.restart()

    os._exit(0)