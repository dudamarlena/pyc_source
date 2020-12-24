# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/threads/sub_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 965 bytes
import functools, time, unittest
from bibliopixel.util.threads import sub
from .. import mark_tests
WAIT_FOR_SUB = 0.1

def pause(delay=0.01):
    time.sleep(delay)


def run(input, output, *arg, **kwds):
    pause()
    output.put('first')
    if arg != (1, 2, 3):
        raise ValueError('1 2 3')
    if kwds != dict(a=1):
        raise ValueError('a=1')
    pause()
    output.put('second')


class SubTest(unittest.TestCase):

    def do_test(self, use_subprocess):
        s, input, output = sub.run(run,
          1, 2, 3, a=1, use_subprocess=use_subprocess)
        self.assertTrue(s.is_alive())
        self.assertEqual(output.get(), 'first')
        self.assertTrue(s.is_alive())
        self.assertEqual(output.get(), 'second')
        pause(WAIT_FOR_SUB)
        self.assertFalse(s.is_alive())

    @mark_tests.fails_on_windows
    def test_subprocess(self):
        self.do_test(True)

    def test_threading(self):
        self.do_test(False)