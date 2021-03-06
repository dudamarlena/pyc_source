# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/test_summary.py
# Compiled at: 2015-03-19 14:45:48
import os.path

def build_summary_cmd(target, source, env):
    """
        Build a text file with the status results for all of the unit tests in sources.
        sources should point to an array of strings corresponding to .status files.
        """
    some_failed = False
    targets = {}
    for node in source:
        path = str(node)
        name, targ, ext = parse_name(path)
        if ext != '.status':
            print 'Ignoring non-status file %s, this file should not be in this list' % path
        if targ not in targets:
            targets[targ] = []
        targets[targ].append((name, path))

    with open(str(target[0]), 'w') as (f):
        f.write('Test Summary\n')
        for targ, tests in targets.iteritems():
            num_tests = len(tests)
            results = map(lambda x: test_passed(x[1]), tests)
            tagged_tests = zip(tests, results)
            failed = filter(lambda x: x[1] == False, tagged_tests)
            passed = filter(lambda x: x[1] == True, tagged_tests)
            num_passed = len(passed)
            if num_passed != num_tests:
                some_failed = True
            f.write('\n## Target %s ##\n' % targ)
            f.write('%d/%d tests passed (%d%% pass rate)\n' % (num_passed, num_tests, num_passed * 100 / num_tests))
            for fail in failed:
                f.write('Test %s FAILED\n' % fail[0][0])

    with open(str(target[0]), 'r') as (f):
        for line in f.readlines():
            print line.rstrip()

    if some_failed:
        return 1


def test_passed(path):
    with open(path, 'r') as (f):
        contents = f.read()
        result = contents.lstrip().rstrip()
        if result == 'PASSED':
            return True
        if result == 'FAILED':
            return False
        raise ValueError('Invalid value in test status file %s, contents were %s' % (path, result))


def parse_name(path):
    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    name, target = name.split('@', 1)
    return (
     name, target, ext)