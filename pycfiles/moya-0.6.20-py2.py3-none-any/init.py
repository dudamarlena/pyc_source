# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/init.py
# Compiled at: 2017-07-05 11:32:30
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from ...command import SubCommand
from ...console import Cell
from ...wsgi import WSGIApplication
from ... import namespaces
from ... import db
try:
    import readline
except ImportError:
    pass

class Init(SubCommand):
    """initialize a site for first use"""
    help = b'initialize a site for first use'

    def add_arguments(self, parser):
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings')
        return

    def run(self):
        args = self.args
        console = self.console
        application = WSGIApplication(self.location, self.get_settings(), validate_db=True, disable_autoreload=True, master_settings=self.master_settings)
        archive = application.archive
        self.console.div(b'syncing database')
        db.sync_all(archive, self.console, summary=False)
        commands = [ command for command in archive.get_elements_by_type(namespaces.default, b'command') if command._init
                   ]
        commands.sort(key=lambda c: c._priority, reverse=True)
        fail = None
        for command in commands:
            if fail:
                break
            for app_name in archive.apps_by_lib[command.lib.long_name]:
                app = archive.apps[app_name]
                app_id = command.get_appid(app=app)
                console.div(command._synopsis)
                result = self.moya_command.project_invoke(app_id, application=application, root_vars={b'init': True})
                if result != 0:
                    fail = result
                    break

        console.nl()
        if not fail:
            msg = b'Site is ready for use!\nRun "moya runserver" from the project directory.'
            console.table([[Cell(msg, fg=b'green', bold=True)]])
        else:
            msg = b'A command failed to complete -- check above for any error messages.'
            console.table([[Cell(msg, fg=b'red', bold=True)]])
        return