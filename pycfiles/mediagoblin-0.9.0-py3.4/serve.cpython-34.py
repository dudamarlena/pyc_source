# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/serve.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2375 bytes
from __future__ import print_function
from paste.deploy import loadapp, loadserver

class ServeCommand(object):

    def loadserver(self, server_spec, name, relative_to, **kwargs):
        return loadserver(server_spec, name=name, relative_to=relative_to, **kwargs)

    def loadapp(self, app_spec, name, relative_to, **kwargs):
        return loadapp(app_spec, name=name, relative_to=relative_to, **kwargs)

    def daemonize(self):
        pass

    def restart_with_reloader(self):
        pass

    def restart_with_monitor(self, reloader=False):
        pass

    def run(self):
        print('Running...')


def parser_setup(subparser):
    subparser.add_argument('config', metavar='CONFIG_FILE')
    subparser.add_argument('command', choices=[
     'start', 'stop', 'restart', 'status'], nargs='?', default='start')
    subparser.add_argument('-n', '--app-name', dest='app_name', metavar='NAME', help='Load the named application (default main)')
    subparser.add_argument('-s', '--server', dest='server', metavar='SERVER_TYPE', help='Use the named server.')
    subparser.add_argument('--reload', dest='reload', action='store_true', help='Use auto-restart file monitor')


def serve(args):
    serve_cmd = ServeCommand()
    serve_cmd.run()