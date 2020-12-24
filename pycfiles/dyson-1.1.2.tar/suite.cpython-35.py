# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/cli/suite.py
# Compiled at: 2016-11-12 17:50:06
# Size of source mod 2**32: 1388 bytes
import os
from dyson.cli import CLI
from dyson.errors import DysonError
from dyson.suites import Suite
from dyson.utils.dataloader import DataLoader
from dyson.vars import VariableManager, load_extra_vars, load_aut_vars, load_vars

class SuiteCLI(CLI):

    def parse(self):
        self.parser = CLI.base_parser('%prog suite.yml ...', datafile_opts=True)
        self.parser.add_option('-b', '--browser', help='Specify which browser to run. e.g. chrome, firefox')
        super(SuiteCLI, self).parse()

    def run(self):
        super(SuiteCLI, self).run()
        for suite in self.args:
            if not os.path.exists(suite):
                raise DysonError('Suite file %s does not exist' % suite)

        dataloader = DataLoader()
        variablemanager = VariableManager()
        variablemanager.extra_vars = load_extra_vars(loader=dataloader, options=self.options)
        variablemanager.aut_vars = load_aut_vars(loader=dataloader, options=self.options, variable_manager=variablemanager)
        variablemanager.vars = load_vars(loader=dataloader, options=self.options, variable_manager=variablemanager)
        for suite in self.args:
            Suite(suite, data_loader=dataloader, variable_manager=variablemanager, report=self.report).run()