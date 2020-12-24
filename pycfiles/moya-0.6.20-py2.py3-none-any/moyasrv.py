# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/moyasrv.py
# Compiled at: 2016-03-13 09:33:33
from __future__ import unicode_literals
from __future__ import print_function
import argparse, os, sys, io, glob, tempfile
from moya.compat import text_type
from moya.settings import SettingsContainer
from moya.console import Console
DEFAULT_HOME_DIR = b'/etc/moya/'
DEFAULT_CONF = b'\n[projects]\nread = ./sites-enabled/*.ini\nlogging = logging.ini\n'
DEFAULT_LOGGING = b'\n# Logging conf for production\n# Only errors and request information is written to stdout\n\n[logger:root]\nhandlers=syslog\n\n[logger:moya]\nhandlers=syslog\nlevel=DEBUG\npropagate=no\n\n[logger:moya.startup]\nlevel=INFO\nhandlers=syslog\npropagate=no\n\n[logger:moya.srv]\nlevel=INFO\nhandlers=syslog\npropagate=no\n\n[logger:moya.request]\nlevel=DEBUG\nhandlers=null\npropagate=no\n\n[handler:stdout]\nclass=StreamHandler\nformatter=simple\nargs=(sys.stdout,)\n\n[handler:syslog]\nformatter = simple\nclass = moya.logtools.MoyaSysLogHandler\n\n[formatter:simple]\nformat=:%(name)s:%(levelname)s: %(message)s\ndatefmt=[%d/%b/%Y %H:%M:%S]\n\n[formatter:format_referer]\nformat=%(asctime)s %(message)s\ndatefmt=[%d/%b/%Y %H:%M:%S]\n\n'
BASH_TOOLS = b'\nmoyacd () {\n    cd $(moya-srv where $1)\n}\n\nalias moya-cd=moyacd\nPS1="\\`if [ \\"\\$MOYA_SERVICE_PROJECT\\" != \\"\\" ]; then echo \\"<\\$MOYA_SERVICE_PROJECT>\\"; fi\\`$PS1"\nexport PS1\n'

class CommandError(Exception):
    pass


class MoyaSrv(object):
    """Moya Service"""

    def get_argparse(self):
        parser = argparse.ArgumentParser(prog=b'moya-srv', description=self.__doc__)
        parser.add_argument(b'-d', b'--debug', dest=b'debug', action=b'store_true', help=b'enable debug information (show tracebacks)')
        parser.add_argument(b'--home', dest=b'home', metavar=b'PATH', default=None, help=b'moya service directory')
        subparsers = parser.add_subparsers(title=b'available sub-commands', dest=b'subcommand', help=b'sub-command help')
        list_parser = subparsers.add_parser(b'list', help=b'list projects', description=b'list enabled projects')
        list_parser
        where_parser = subparsers.add_parser(b'where', help=b'find project directory', description=b'output the location of the project')
        where_parser.add_argument(dest=b'name', metavar=b'PROJECT', help=b'name of a project')
        restart_parser = subparsers.add_parser(b'restart', help=b'restart a project server', description=b'restart a server')
        restart_parser.add_argument(dest=b'name', metavar=b'PROJECT', help=b'name of a project')
        install_parser = subparsers.add_parser(b'install', help=b'install moya service', description=b'install moya service')
        install_parser.add_argument(b'--home', dest=b'home', metavar=b'PATH', default=DEFAULT_HOME_DIR, help=b'where to install service conf')
        install_parser.add_argument(b'--force', dest=b'force', action=b'store_true', help=b'overwrite files that exist')
        install_parser
        return parser

    def error(self, msg, code=-1):
        sys.stderr.write(msg + b'\n')
        sys.exit(code)

    def run(self):
        parser = self.get_argparse()
        self.args = args = parser.parse_args(sys.argv[1:])
        self.console = Console()
        if args.subcommand not in ('install', ):
            self.home_dir = args.home or os.environ.get(b'MOYA_SERVICE_HOME', None) or DEFAULT_HOME_DIR
            settings_path = os.path.join(self.home_dir, b'moya.conf')
            try:
                with io.open(settings_path, b'rt') as (f):
                    self.settings = SettingsContainer.read_from_file(f)
            except IOError:
                self.error((b'unable to read {}').format(settings_path))
                return -1

        method_name = b'run_' + args.subcommand.replace(b'-', b'_')
        try:
            return getattr(self, method_name)() or 0
        except CommandError as e:
            self.error(text_type(e))
        except Exception as e:
            if args.debug:
                raise
            self.error(text_type(e))

        return

    def _get_projects(self):
        project_paths = self.settings.get_list(b'projects', b'read')
        paths = []
        cwd = os.getcwd()
        try:
            os.chdir(self.home_dir)
            for path in project_paths:
                glob_paths = glob.glob(path)
                paths.extend([ os.path.abspath(p) for p in glob_paths ])

        finally:
            os.chdir(cwd)

        return paths

    def project_exists(self, name):
        for path in self._get_projects():
            settings = self.read_project(path)
            if settings.get(b'service', b'name', None) == name:
                return True

        return False

    def read_project(self, path):
        settings = SettingsContainer.read_os(path)
        return settings

    def run_list(self):
        table = []
        for path in self._get_projects():
            settings = self.read_project(path)
            location = settings.get(b'service', b'location', b'?')
            name = settings.get(b'service', b'name', b'?')
            domains = (b'\n').join(settings.get_list(b'service', b'domains', b''))
            table.append([name, domains, path, location])

        table.sort(key=lambda row: row[0].lower())
        self.console.table(table, header_row=[b'name', b'domain(s)', b'conf', b'location'])

    def run_where(self):
        name = self.args.name
        location = None
        for path in self._get_projects():
            settings = self.read_project(path)
            if settings.get(b'service', b'name', None) == name:
                location = settings.get(b'service', b'location', None)

        if location is None:
            self.error((b"no project '{}'").format(name))
            return -1
        else:
            sys.stdout.write(location)
            return 0

    def run_restart(self):
        name = self.args.name
        if not self.project_exists(name):
            self.error((b"no project '{}'").format(name))
        temp_dir = os.path.join(self.settings.get(b'service', b'temp_dir', tempfile.gettempdir()), b'moyasrv')
        try:
            os.makedirs(temp_dir)
        except OSError:
            pass

        change_path = os.path.join(temp_dir, (b'{}.changes').format(name))
        try:
            with open(change_path, b'a'):
                os.utime(change_path, None)
        except IOError as e:
            sys.stderr.write((b'{}\n').format(text_type(e)))
            return -1

        return

    def run_install(self):
        home_dir = self.args.home or DEFAULT_HOME_DIR

        def create_dir(_path):
            path = os.path.join(home_dir, _path)
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
                    sys.stdout.write((b"created '{}'\n").format(path))
            except OSError as e:
                if e.errno != 17:
                    raise

        for dirpath in [b'', b'sites-enabled', b'sites-available']:
            try:
                create_dir(dirpath)
            except OSError as e:
                if e.errno == 13:
                    sys.stderr.write(b'permission denied (do you need sudo)?\n')
                    return -1
                raise

        def write_file(_path, contents):
            path = os.path.join(home_dir, _path)
            if not self.args.force and os.path.exists(path):
                sys.stdout.write((b"not overwriting '{}' (use --force to overwrite)\n").format(path))
                return
            with open(path, b'wt') as (f):
                f.write(contents)
            sys.stdout.write((b"wrote '{}'\n").format(path))

        for path, contents in [(b'moya.conf', DEFAULT_CONF),
         (
          b'logging.ini', DEFAULT_LOGGING),
         (
          b'bashtools', BASH_TOOLS)]:
            try:
                write_file(path, contents)
            except IOError as e:
                if e.errno == 13:
                    sys.stdout.write((b"permission denied writing '{}' (do you need sudo)?\n").format(path))
                    return -1
                raise

        TOOLS_PATH = b'~/.bashrc'
        bashtools_path = os.path.join(home_dir, b'bashtools')
        try:
            cmd = (b'\n# Added by moya-srv install\nsource {}\n').format(bashtools_path)
            bashrc_path = os.path.expanduser(TOOLS_PATH)
            if os.path.exists(bashrc_path):
                with open(bashrc_path, b'rb') as (f):
                    bashrc = f.read()
            else:
                bashrc = b''
            if cmd not in bashrc:
                with open(bashrc_path, b'ab') as (f):
                    f.write(cmd)
        except Exception as e:
            sys.stdout.write((b'unable to add moya service bash tools ({})\n').format(e))
        else:
            sys.stdout.write((b'Added Moya service bash tools to {}\n').format(TOOLS_PATH))
            sys.stdout.write((b"Tools will be available when you next log in (or run 'source {})\n").format(bashtools_path))

        sys.stdout.write((b'Moya service was installed in {}\n').format(home_dir))


def main():
    moya_srv = MoyaSrv()
    sys.exit(moya_srv.run() or 0)