# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/chrisecho/test.py
# Compiled at: 2016-03-22 08:29:40
import unittest
from chrisecho import Echo

class EchoTest(unittest.TestCase):

    def test(self):
        x = Echo()
        self.assertEqual(x.doit('Hello World'), 'Hello World')

    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_2(self):
        self.assertGreater(2, 1)

    def test_json(self):
        x = Echo()
        self.assertEqual(x.do_request()['count'], 0)


def main():
    unittest.main()


if __name__ == '__main__':
    main()