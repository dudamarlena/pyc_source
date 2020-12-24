# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/app.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
import sys, os.path, argparse, logging.config, locale, io, importlib
from ..command.sub import __all__ as all_subcommands
from ..console import Console
from ..context import Context
from ..context.tools import set_dynamic
from ..tools import get_moya_dir, is_moya_dir, nearest_word
from ..errors import ElementNotFoundError
from ..compat import text_type
from ..command.subcommand import SubCommandMeta
from ..multiwsgi import Service
from .. import db
from .. import settings
from .. import errors
from .. import __version__ as version
from fs.opener import open_fs
import logging
logging.raiseExceptions = False

class NoProjectError(Exception):
    pass


class Command(object):
    description = b''

    def __init__(self):
        self._console = None
        self.subcommands = {}
        return

    def make_subcommands(self):
        self.subcommands = {name:cls(self) for name, cls in SubCommandMeta.registry.items()}


class MoyaArgumentParser(argparse.ArgumentParser):
    """Some enhancements to argparse"""

    def _check_value(self, action, value):
        if action.choices is not None and value not in action.choices:
            nearest = nearest_word(value, action.choices)
            if nearest:
                msg = (b"invalid choice: '{}' (did you mean '{}')?\n").format(value, nearest)
            else:
                msg = (b"invalid choice: '{}'\n").format(value)
            self.print_usage()
            sys.stderr.write(msg)
            sys.exit(-1)
        return


class Moya(Command):
    """Pilot for Moya web application server

Project commands may be called by giving the element reference as the first
parameter, e.g.

    moya auth#command.adduser -h

To list all available commands for a given application, omit the libname:

    moya auth#
"""

    def __init__(self, fs=None, location=None):
        super(Moya, self).__init__()
        self._location_fs = fs
        self._location = location
        self._master_settings = None
        return

    @property
    def console(self):
        if self._console is None:
            color = self.moyarc.get_bool(b'console', b'color', True)
            self._console = Console(nocolors=not color)
        return self._console

    def get_default(self, name, default=None):
        return self.moyarc.get(b'defaults', name, default)

    def get_argparse(self):
        parser = MoyaArgumentParser(prog=self.__class__.__name__.lower(), description=getattr(self, b'__doc__', b''), formatter_class=argparse.RawDescriptionHelpFormatter, epilog=b'Need help? http://moyaproject.com')
        parser.add_argument(b'-v', b'--version', action=b'version', version=version)
        parser.add_argument(b'-d', b'--debug', dest=b'debug', action=b'store_true', default=False, help=b'enables debug output')
        parser.add_argument(b'--logging', dest=b'logging', default=b'logging.ini', help=b'set logging file')
        subparsers = parser.add_subparsers(title=b'available sub-commands', dest=b'subcommand', help=b'sub-command help')
        for name, subcommand in sorted(self.subcommands.items(), key=lambda item: item[0]):
            subparser = subparsers.add_parser(name, help=subcommand.help, description=getattr(subcommand, b'__doc__', None))
            subcommand.add_arguments(subparser)

        return parser

    def get_settings(self):
        settings = self.args.settings
        moya_service = os.environ.get(b'MOYA_SERVICE_PROJECT', None)
        if moya_service is not None and self.master_settings is not None:
            settings = self.master_settings.get(b'service', b'ini', None)
        if not settings:
            settings = os.environ.get(b'MOYA_PROJECT_INI', None) or self.moyarc.get(b'defaults', b'ini', b'settings.ini').strip()
        if not settings:
            return []
        else:
            ini_list = [ s.strip() for s in settings.splitlines() if s.strip() ]
            return ini_list

    @property
    def master_settings(self):
        if self._master_settings is not None:
            return self._master_settings
        else:
            moya_service = os.environ.get(b'MOYA_SERVICE_PROJECT', None)
            if moya_service is None:
                self._master_settings = None
            else:
                self._master_settings = Service.get_project_settings(moya_service)
            return self._master_settings

    @property
    def location(self):
        if self._location is not None:
            return self._location
        else:
            location = None
            if self.master_settings:
                location = self.master_settings.get(b'service', b'location', None)
            location = self.args.location or location or os.environ.get(b'MOYA_PROJECT', None)
            if location is None:
                location = b'./'
            if location and b'://' in location:
                return location
            try:
                location = get_moya_dir(location)
            except ValueError:
                raise NoProjectError(b'Moya project directory not found, run this command from a project directory or specify --location')

            if not is_moya_dir(location):
                raise NoProjectError(b"Location is not a moya project (no 'moya' file found)")
            self._location = location
            return location

    @property
    def location_fs(self):
        if self._location_fs is None:
            self._location_fs = open_fs(self.location)
        return self._location_fs

    def debug(self, text):
        """Write debug text, if enabled through command line switch"""
        if self.args.debug:
            self.console(text).nl()

    def error(self, text):
        """Write an error to the console"""
        self.console.error(text)

    def run(self):
        try:
            with io.open(os.path.expanduser(b'~/.moyarc'), b'rt') as (f):
                self.moyarc = settings.SettingsContainer.read_from_file(f)
        except IOError:
            self.moyarc = settings.SettingsContainer()

        try:
            encoding = sys.stdin.encoding or locale.getdefaultlocale()[1]
        except:
            encoding = sys.getdefaultencoding()

        argv = [ (isinstance(v, text_type) or v.decode)(encoding, b'replace') if 1 else v for v in sys.argv ]
        if len(argv) > 1 and argv[1].count(b'#') == 1:
            return self.project_invoke(argv[1])
        else:
            if len(argv) > 1 and argv[1] in all_subcommands:
                importlib.import_module(b'.' + argv[1], b'moya.command.sub')
            else:
                for name in all_subcommands:
                    importlib.import_module(b'.' + name, b'moya.command.sub')

                self.make_subcommands()
                parser = self.get_argparse()
                self.args = parser.parse_args(argv[1:])
                if self.args.subcommand is None:
                    parser.print_usage()
                    return 1
                subcommand = self.subcommands[self.args.subcommand]
                subcommand.args = self.args
                subcommand.console = self.console
                subcommand.moyarc = self.moyarc
                subcommand.moya_command = self
                subcommand.master_settings = self.master_settings
                try:
                    return subcommand.run()
                except KeyboardInterrupt as e:
                    self.console.nl()
                    if self.args.debug:
                        self.console.exception(e, tb=True)
                        self.console.div()
                    return -1
                except Exception as e:
                    if self.args.debug and hasattr(e, b'__moyaconsole__'):
                        e.__moyaconsole__(self.console)
                    else:
                        if self.args.debug:
                            self.console.div()
                        self.console.exception(e, tb=self.args.debug)
                        if self.args.debug:
                            self.console.div()
                    return -1

            return

    def project_invoke(self, element_ref, application=None, root_vars=None):
        parser = argparse.ArgumentParser(prog=self.__class__.__name__.lower() + b' ' + element_ref, description=b'Call command %s in moya project' % element_ref, add_help=False)
        parser.add_argument(b'-h', b'--help', dest=b'help', action=b'store_true', default=False, help=b'print help information')
        parser.add_argument(b'-d', b'--debug', dest=b'debug', action=b'store_true', default=False, help=b'enables debug output')
        parser.add_argument(b'-V', b'--verbose', dest=b'verbose', action=b'store_true', default=False, help=b'enables verbose output')
        parser.add_argument(b'--logging', dest=b'logging', default=None, help=b'path to logging configuration file', metavar=b'LOGGINGINI')
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
        parser.add_argument(b'-b', b'--breakpoint', dest=b'breakpoint', action=b'store_true', default=False, help=b'Start debugging at first element')
        args, remaining = parser.parse_known_args(sys.argv[2:])
        self.args = args
        show_help = args.help
        from .. import pilot
        from ..wsgi import WSGIApplication
        if application is None:
            try:
                application = WSGIApplication(self.location_fs, self.get_settings(), disable_autoreload=True)
            except Exception as e:
                self.console.exception(e)
                return -1

        archive = application.archive
        context = Context()
        application.populate_context(context)
        set_dynamic(context)
        context[b'.console'] = self.console
        if root_vars is not None:
            context.root.update(root_vars)
        if element_ref.endswith(b'#'):
            app_name = element_ref[:-1]
            try:
                app = archive.find_app(app_name)
            except errors.UnknownAppError:
                self.error(b"No app called '%s' -- try 'moya apps'" % app_name)
                return -1

            commands = []
            for element in app.lib.get_elements_by_type(b'command'):
                commands.append((b'moya ' + element_ref + element.libname, element.synopsis(context)))

            if not commands:
                self.console.text(b'No commands available in %s' % app)
                return 0
            commands.sort()
            self.console.text(b'%s command(s) available in %s' % (len(commands), app), bold=True, fg=b'yellow')
            if commands:
                self.console.table(commands, header_row=('command', 'synopsis'))
            return 0
        try:
            app, command_element = archive.get_app_element(element_ref)
        except errors.UnknownAppError:
            appname = element_ref.partition(b'#')[0]
            self.error((b"No app called '{}' -- try 'moya apps' to list available applications").format(appname))
            return -1
        except ElementNotFoundError:
            appname = element_ref.partition(b'#')[0]
            self.error((b"Command '{}' not found -- try 'moya {}#' to list available commands ").format(element_ref, appname))
            return -1

        synopsis = command_element.synopsis(context)
        parser.description = synopsis
        command_element.update_parser(parser, context)
        if show_help:
            parser.print_help()
            return 0
        else:
            args = parser.parse_args(remaining)
            ret = None
            try:
                context.root[b'server'] = application.server
                archive.populate_context(context)
                with pilot.manage(context):
                    if self.args.breakpoint:
                        ret = archive.debug_call(element_ref, context, app, args=vars(args))
                    else:
                        ret = archive.call(element_ref, context, app, args=vars(args))
                    for thread in context.get(b'._threads', []):
                        thread.wait()

                    context.safe_delete(b'._threads')
                    db.commit_sessions(context)
            except KeyboardInterrupt:
                self.console.nl().div(b'user exit')
                ret = -2
            except Exception as e:
                if hasattr(e, b'__moyaconsole__'):
                    e.__moyaconsole__(self.console)
                else:
                    if self.args.debug:
                        self.console.div()
                    self.console.exception(e, tb=self.args.debug)
                    if self.args.debug:
                        self.console.div()
                ret = -2

            return ret


def main():
    moya = Moya()
    return moya.run()


if __name__ == b'__main__':
    sys.exit(main())