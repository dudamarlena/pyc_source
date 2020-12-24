# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nick/Downloads/simplenotifications/simplenotifications/tests/test_notify.py
# Compiled at: 2019-07-26 22:44:38
# Size of source mod 2**32: 2263 bytes
"""simplenotifications

This module tests the functionality of the desktop notifications module. It
can only perform tests for the operating system environment you are currently
using. For example, if you are using a GNU/Linux based system, the tests for
the Windows 10 platform will not execute since the notifications rely on system
dependent libraries.
"""
from unittest import TestCase
from simplenotifications import notify
import os, json, time

class TestNotify(TestCase):

    def test_notify_title(self):
        notify('example')
        time.sleep(0.1)

    def test_notify_message(self):
        notify('example', 'this is the message')
        time.sleep(0.1)

    def test_notify_timeout(self):
        notify('example', 'this is the message', 5)
        time.sleep(0.1)

    def test_notify_evil_strings(self):
        with open(os.path.join(os.path.dirname(__file__), 'resources', 'evilstrings', 'blns.json')) as (json_file):
            evil_strings = json.load(json_file)
        for string in evil_strings:
            try:
                notify(str(string), str(string))
            except TypeError:
                pass
            except UnicodeEncodeError:
                pass

            time.sleep(0.1)


if __name__ == '__main__':
    TestNotify().test_notify_title()
    TestNotify().test_notify_message()
    TestNotify().test_notify_timeout()
    TestNotify().test_notify_evil_strings()