# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/libs.py
# Compiled at: 2015-11-29 05:52:18
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...console import Cell
import sys

class Libs(SubCommand):
    """List libraries installed in the project"""
    help = b'get library information'

    def add_arguments(self, parser):
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to projects settings file')
        parser.add_argument(b'--org', dest=b'org', default=None, metavar=b'ORGANIZATION', help=b'show only libraries with from a specific organization')
        parser.add_argument(b'-f', b'--freeze', dest=b'freeze', action=b'store_true', help=b'output project library requirements')
        return parser

    def run(self):
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True, master_settings=self.master_settings)
        archive = application.archive
        table = []
        if args.org:
            prefix = args.org.lstrip(b'.') + b'.'
        else:
            prefix = None
        libs = sorted(archive.libs.values(), key=lambda lib: lib.long_name)
        if prefix is not None:
            libs = [ lib for lib in libs if lib.long_name.startswith(prefix) ]
        if args.freeze:
            lib_freeze = (b'\n').join((b'{}=={}').format(lib.long_name, lib.version) for lib in libs) + b'\n'
            sys.stdout.write(lib_freeze)
            return 0
        else:
            for lib in libs:
                name = lib.long_name
                if prefix is not None and not name.startswith(prefix):
                    continue
                table.append([
                 name,
                 Cell(lib.version, bold=True, fg=b'magenta'),
                 Cell(lib.install_location, bold=True, fg=b'blue')])

            self.console.table(table, header_row=[b'lib', b'version', b'location'])
            return