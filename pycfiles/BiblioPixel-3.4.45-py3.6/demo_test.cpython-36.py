# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/commands/demo_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 497 bytes
import os, unittest
from unittest import mock
from bibliopixel.commands import demo
from bibliopixel.main import args, project_flags

class TestDemo(unittest.TestCase):

    def test_demo_projects(self):
        with mock.patch('bibliopixel.animation.animation.Animation.FAIL_ON_EXCEPTION', True):
            ARGS = args.set_args('test', [], demo)
            for k, v in demo.demo_table.DEMO_TABLE.items():
                demo.make_runnable_animation(v, ARGS)