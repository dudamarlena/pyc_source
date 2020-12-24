# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/tests/delete_test_command_line.py
# Compiled at: 2013-08-05 10:20:44
from unittest import TestCase
from funniest.cmd import main

class TestCmd(TestCase):

    def test_basic(self):
        main()