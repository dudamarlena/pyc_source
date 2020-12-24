# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/apps.py
# Compiled at: 2015-11-29 05:52:18
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...console import Cell

class Apps(SubCommand):
    """List project applications"""
    help = b'get application information'

    def add_arguments(self, parser):
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to projects settings file')
        return parser

    def run(self):
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True, master_settings=self.master_settings)
        archive = application.archive
        table = []
        for name, app in sorted(archive.apps.items()):
            table.append([
             name,
             app.lib.long_name,
             Cell(app.lib.version, bold=True, fg=b'magenta')])

        self.console.table(table, [
         b'app', b'lib', b'version'])