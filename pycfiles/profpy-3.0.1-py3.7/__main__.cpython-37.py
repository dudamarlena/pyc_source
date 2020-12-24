# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/__main__.py
# Compiled at: 2020-01-15 15:33:55
# Size of source mod 2**32: 4312 bytes
"""
__main__.py

Entrypoint for the profpy CLI tool suite. This gets installed on the user's path once profpy is installed. 
Users can call tools on the command line like so:
    profpy <tool> <args>
"""
import sys, argparse
from cli.run_app import run_app, run_app_argparser
from cli.flask_init import flask_init, flask_init_prompt, flask_init_argparser
from cli.stop_app import stop_app, stop_app_argparser
from cli.logs import logs, logs_argparser
_programs = [
 dict(name='flask-init', description='Initialize a Flask web app with profpy.web tools.'),
 dict(name='run-app', description='Run a dockerized web app that you created with one of the profpy init tools.'),
 dict(name='stop-app', description='Stop a dockerized web app that you created with one of the profpy init tools.'),
 dict(name='logs', description='Get the logs for an app you created with a profpy init tool.'),
 dict(name='help', description='Get info on profpy CLI tools.')]

class Cli(object):
    __doc__ = '\n    This class handles the calling of profpy CLI tools.\n    '

    def __init__(self):
        """
        Constructor. Evaluates the input.
        """
        parser = argparse.ArgumentParser(description='Profpy CLI tools.',
          usage='profpy <program> [<args>]')
        if not sys.argv[1:]:
            self.help()
        else:
            if sys.argv[1] == '-h':
                self.help()
            else:
                parser.add_argument('program', help='The CLI tool to use.', type=str)
                args = parser.parse_args(sys.argv[1:2])
                self._Cli__prog_args = sys.argv[2:]
                program = args.program.lower().replace('-', '_')
                hasattr(self, program) or print('Unrecognized program.')
                parser.print_help()
                sys.exit(1)
            getattr(self, program)()

    def logs(self):
        """
        Produce logs for a profpy-created web application.
        """
        logs(logs_argparser().parse_args(self._Cli__prog_args))

    def help(self):
        """
        A useful help screen that displays usage info and a list of available programs.
        """
        print('Profpy CLI tools.')
        print('Usage: profpy <program> [<args>]')
        print('Available programs:')
        for prog in _programs:
            print(f"\t{prog['name']} - {prog['description']}")

        sys.exit(0)

    def run_app(self):
        """
        Runs a web application using docker. 
        This will only work with apps that were initialized by a profpy init tool, i.e. "profpy flask-init".
        """
        run_app(run_app_argparser().parse_args(self._Cli__prog_args))

    def stop_app(self):
        """
        Stops a dockerized web application that was initialized via profpy CLI init tools. 
        """
        stop_app(stop_app_argparser().parse_args(self._Cli__prog_args))

    def flask_init(self):
        """
        Initialize a dockerized flask application. This app will utilize meinheld, gunicorn, Flask, and profpy. 
        Included in this app directory structure:
            - all docker componenets
            - an app directory with main.py (the controller), templates/, and static/ (which contains js/, css/, and images/)
            - a dba directory with initial setup tools for the database schema
            - a SAMPLE.env file and a .env file with an empty db_password variable
            - .gitignore
            - README.md
            - requirements.txt
            - a base Rowan-styled template system
                - the layout includes bootstrap4, datatables, and select2
        """
        parser = flask_init_argparser()
        if self._Cli__prog_args:
            flask_init(parser.parse_args(self._Cli__prog_args))
        else:
            flask_init(parser.parse_args(flask_init_prompt()))


def main():
    """
    CLI driver
    """
    try:
        Cli()
    except KeyboardInterrupt:
        print('Goodbye.')