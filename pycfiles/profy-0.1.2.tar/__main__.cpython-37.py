# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/__main__.py
# Compiled at: 2020-01-15 15:33:55
# Size of source mod 2**32: 4312 bytes
__doc__ = "\n__main__.py\n\nEntrypoint for the profpy CLI tool suite. This gets installed on the user's path once profpy is installed. \nUsers can call tools on the command line like so:\n    profpy <tool> <args>\n"
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
    """Cli"""

    def __init__(self):
        """
        Constructor. Evaluates the input.
        """
        parser = argparse.ArgumentParser(description='Profpy CLI tools.',
          usage='profpy <program> [<args>]')
        if not sys.argv[1:]:
            self.help()
        elif sys.argv[1] == '-h':
            self.help()
        parser.add_argument('program', help='The CLI tool to use.', type=str)
        args = parser.parse_args(sys.argv[1:2])
        self._Cli__prog_args = sys.argv[2:]
        program = args.program.lower().replace('-', '_')
        if not hasattr(self, program):
            print('Unrecognized program.')
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