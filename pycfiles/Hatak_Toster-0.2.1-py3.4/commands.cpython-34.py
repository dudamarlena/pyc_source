# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/toster/commands.py
# Compiled at: 2014-10-11 13:53:11
# Size of source mod 2**32: 459 bytes
import sys
from .runner import TestRunner
from hatak.command import Command

class TosterCommand(Command):

    def __init__(self, fixtures):
        super().__init__('toster', 'tests')
        self.fixtures = fixtures

    def __call__(self, args):
        self.app.factory.run_module('tests')
        self.app.factory.run_module_without_errors('tests')
        sys.argv.pop(0)
        TestRunner(self.app, self.fixtures)()