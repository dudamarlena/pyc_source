# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_runner.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 2351 bytes
import os, sys
from glob import glob
import unittest
thisdir = os.path.dirname(__file__)

class ScriptTestCase(unittest.TestCase):

    def __init__(self, methodname='run_tests', filename=None):
        unittest.TestCase.__init__(self, methodname)
        self.filename = filename

    def run_tests(self):
        env = globals().copy()
        env.update(__file__=(self.filename))
        with open(self.filename) as (fd):
            exec(compile(fd.read(), self.filename, 'exec'), env)

    def id(self):
        return self.filename

    def __str__(self):
        return self.filename.split('tests/')[(-1)]

    def __repr__(self):
        return "ScriptTestCase(filename='%s')" % self.filename


def test(verbosity=1, stream=sys.stdout):
    tests = [test for test in glob(os.path.join(thisdir, '*.py')) if not test.endswith('__.py') if not test.endswith(os.path.basename(__file__))]
    ts = unittest.TestSuite()
    for test in tests:
        ts.addTest(ScriptTestCase(filename=(os.path.abspath(test))))

    with open(os.devnull, 'w') as (devnull):
        if not verbosity:
            stream = devnull
        ttr = unittest.TextTestRunner(verbosity=verbosity, stream=stream)
        dest_fd = devnull.fileno()
        stderr_fd = sys.stderr.fileno()
        with os.fdopen(os.dup(stderr_fd), 'wb') as (copied):
            sys.stdout.flush()
            sys.stderr.flush()
            try:
                sys.stdout = devnull
                os.dup2(dest_fd, stderr_fd)
                results = ttr.run(ts)
            finally:
                sys.stdout.flush()
                sys.stderr.flush()
                sys.stdout = sys.__stdout__
                os.dup2(copied.fileno(), stderr_fd)

    return results


if __name__ == '__main__':
    results = test()
    if results.errors or results.failures:
        sys.exit(1)