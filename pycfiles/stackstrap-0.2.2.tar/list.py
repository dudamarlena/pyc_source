# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/evelo/Documents/Repos/stackstrap/stackstrap/commands/template/list.py
# Compiled at: 2014-01-05 21:41:09
from stackstrap.commands import Command
from stackstrap.template import Template

class List(Command):
    """List all templates"""
    name = 'list'

    def setup_parser(self, parser):
        pass

    def main(self, args):
        for template in Template.available():
            self.log.info(template)