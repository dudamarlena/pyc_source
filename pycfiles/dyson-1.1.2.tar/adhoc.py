# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/cli/adhoc.py
# Compiled at: 2016-11-06 19:29:59
from dyson.cli import CLI

class AdHocCLI(CLI):

    def parse(self):
        self.parser = CLI.base_parser('%prog something', datafile_opts=True)
        super(AdHocCLI, self).parse()