# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_ctrl_chars.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest
from . import PexpectTestCase
import time, os

class TestCtrlChars(PexpectTestCase.PexpectTestCase):

    def test_control_chars(self):
        """FIXME: Python unicode was too hard to figure out, so
        this tests only the true ASCII characters. This is lame
        and should be fixed. I'm leaving this script here as a
        placeholder so that it will remind me to fix this one day.
        This is what it used to do:
        This tests that we can send all 256 8-bit ASCII characters
        to a child process."""
        return 0
        child = pexpect.spawn('python getch.py')
        try:
            for i in range(256):
                child.send(chr(i))
                child.expect('%d\r\n' % i)

        except Exception as e:
            msg = 'Did not echo character value: ' + str(i) + '\n'
            msg = msg + str(e)
            self.fail(msg)

    def test_sendintr(self):
        try:
            child = pexpect.spawn('python getch.py')
            time.sleep(0.5)
            child.sendintr()
            child.expect('3\r\n')
        except Exception as e:
            msg = 'Did not echo character value: 3\n'
            msg = msg + str(e)
            self.fail(msg)

    def test_bad_sendcontrol_chars(self):
        """This tests that sendcontrol will return 0 for an unknown char. """
        child = pexpect.spawn('python getch.py')
        retval = child.sendcontrol('1')
        assert retval == 0, 'sendcontrol() should have returned 0 because there is no such thing as ctrl-1.'

    def test_sendcontrol(self):
        """This tests that we can send all special control codes by name.
        """
        child = pexpect.spawn('python getch.py')
        for i in 'abcdefghijklmnopqrstuvwxyz':
            child.sendcontrol(i)
            child.expect('[0-9]+\r\n')

        child.sendcontrol('@')
        child.expect('0\r\n')
        child.sendcontrol('[')
        child.expect('27\r\n')
        child.sendcontrol('\\')
        child.expect('28\r\n')
        child.sendcontrol(']')
        child.expect('29\r\n')
        child.sendcontrol('^')
        child.expect('30\r\n')
        child.sendcontrol('_')
        child.expect('31\r\n')
        child.sendcontrol('?')
        child.expect('127\r\n')


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(TestCtrlChars, 'test')