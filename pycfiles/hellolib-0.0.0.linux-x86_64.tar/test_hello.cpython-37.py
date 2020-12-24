# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/hello/tests/test_hello.py
# Compiled at: 2019-09-18 20:38:57
# Size of source mod 2**32: 377 bytes
import testtools, hello

class TestHello(testtools.TestCase):

    def test_say_hello_with_no_name(self):
        expected = 'hello!'
        actual = hello.say_hello()
        self.assertEqual(expected, actual)

    def test_say_hello_with_a_name(self):
        expected = 'hello, bob!'
        actual = hello.say_hello('bob')
        self.assertEqual(expected, actual)