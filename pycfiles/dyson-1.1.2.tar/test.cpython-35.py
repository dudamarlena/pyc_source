# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/cli/test.py
# Compiled at: 2016-11-12 21:44:40
# Size of source mod 2**32: 1431 bytes
import os
from dyson.cli import CLI
from dyson.errors import DysonError
from dyson.tests import Test
from dyson.utils.dataloader import DataLoader
from dyson.vars import VariableManager, load_extra_vars, load_aut_vars, load_vars

class TestCLI(CLI):

    def parse(self):
        self.parser = CLI.base_parser('%prog tests/smoke/steps/main.yml ...', datafile_opts=True)
        self.parser.add_option('-b', '--browser', help='Specify which browser to run. e.g. chrome, firefox')
        super(TestCLI, self).parse()

    def run(self):
        super(TestCLI, self).run()
        for test in self.args:
            if not os.path.exists(test):
                raise DysonError('Test file %s does not exist' % test)

        dataloader = DataLoader()
        variablemanager = VariableManager()
        variablemanager.extra_vars = load_extra_vars(loader=dataloader, options=self.options)
        variablemanager.aut_vars = load_aut_vars(loader=dataloader, options=self.options, variable_manager=variablemanager)
        variablemanager.vars = load_vars(loader=dataloader, options=self.options, variable_manager=variablemanager)
        for test in self.args:
            self.report.add_test(Test(test, data_loader=dataloader, variable_manager=variablemanager).run())
            self.report.render()