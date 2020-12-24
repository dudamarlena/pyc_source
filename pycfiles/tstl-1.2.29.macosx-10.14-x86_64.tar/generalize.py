# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tstl/generalize.py
# Compiled at: 2019-02-11 12:34:52
from __future__ import print_function
import sys, time, os, subprocess, traceback, argparse
from collections import namedtuple
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)
if '--help' not in sys.argv:
    import sut as SUT

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', metavar='filename', type=str, default=None, help='Path to the test to be reduced.')
    parser.add_argument('--noFresh', action='store_true', help='Do not perform fresh value generalization.')
    parser.add_argument('--noCheck', action='store_true', help='Do not check properties.')
    parser.add_argument('--matchException', action='store_true', help='Force test to fail with same exception as original (does not work for sandboxes).')
    parser.add_argument('--coverage', action='store_true', help='Reduce with respect to maintaining code coverage, not failure.')
    parser.add_argument('-k', '--keepLast', action='store_true', help='Keep last action the same when reducing/normalizing: slippage avoidance heuristic.')
    parser.add_argument('--uncaught', action='store_true', help='Allow uncaught exceptions in actions (for coverage-based reduction).')
    parser.add_argument('--verbose', type=str, default=None, help='Level of verbosity for reduction.')
    parser.add_argument('--sandbox', action='store_true', help='Use sandbox reduction.')
    parser.add_argument('--quietSandbox', action='store_true', help='Run sandbox in a quieter mode.')
    parser.add_argument('--timeout', type=int, default=None, help='Timeout for sandbox reductions (only works on unix-like systems).')
    parsed_args = parser.parse_args(sys.argv[1:])
    return (parsed_args, parser)


def make_config(pargs, parser):
    """
    Process the raw arguments, returning a namedtuple object holding the
    entire configuration, if everything parses correctly.
    """
    pdict = pargs.__dict__
    key_list = list(pdict.keys())
    arg_list = [ pdict[k] for k in key_list ]
    Config = namedtuple('Config', key_list)
    nt_config = Config(*arg_list)
    return nt_config


def sandboxReplay(test):
    if '--quietSandbox' not in sys.argv:
        print('ATTEMPTING SANDBOX REPLAY WITH', len(test), 'STEPS')
    tmpName = 'tmptest.' + str(os.getpid()) + '.test'
    tmptest = open(tmpName, 'w')
    for s in test:
        tmptest.write(s[0] + '\n')

    tmptest.close()
    cmd = 'tstl_replay ' + tmpName
    if '--noCheck' in sys.argv:
        cmd += ' --noCheck'
    if timeout is not None:
        cmd = 'ulimit -t ' + timeout + '; ' + cmd
    start = time.time()
    subprocess.call([cmd], shell=True)
    if '--quietSandbox' not in sys.argv:
        print('ELAPSED:', time.time() - start)
    for l in open('replay.out'):
        if 'TEST REPLAYED SUCCESSFULLY' in l:
            if '--quietSandbox' not in sys.argv:
                print('TEST SUCCEEDS')
            return False

    if '--quietSandbox' not in sys.argv:
        print('TEST FAILS')
    print('SANDBOX RUN FAILS: TEST LENGTH NOW', len(test))
    return True


def main():
    global timeout
    parsed_args, parser = parse_args()
    config = make_config(parsed_args, parser)
    print(('Generalizing using config={}').format(config))
    sut = SUT.sut()
    timeout = config.timeout
    if not config.coverage:
        try:
            sut.stopCoverage()
        except BaseException:
            pass

    t = sut.loadTest(config.infile)
    f = None
    if config.matchException:
        print('RUNNING TO OBTAIN FAILURE FOR EXCEPTION MATCHING...')
        if not sut.fails(t):
            raise AssertionError
            f = sut.failure()
            print('ERROR:', f)
            print('TRACEBACK:')
            traceback.print_tb(f[2], file=sys.stdout)
        if not config.sandbox:
            pred = lambda x: sut.failsCheck(x, failure=f)
            pred = config.noCheck or (lambda x: sut.fails(x, failure=f))
    else:
        pred = sandboxReplay
    if config.coverage:
        print('EXECUTING TEST TO OBTAIN COVERAGE...')
        sut.replay(t, checkPropcheckProp=not config.noCheck, catchUncaught=config.uncaught)
        b = set(sut.currBranches())
        s = set(sut.currStatements())
        print('PRESERVING', len(b), 'BRANCHES AND', len(s), 'STATEMENTS')
        pred = sut.coversAll(s, b, checkProp=not config.noCheck, catchUncaught=config.uncaught)
    print('GENERALIZING...')
    start = time.time()
    sut.generalize(t, pred, verbose=config.verbose, fresh=not config.noFresh, keepLast=config.keepLast)
    print('GENERALIZED IN', time.time() - start, 'SECONDS')
    return