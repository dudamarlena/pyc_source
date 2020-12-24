# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/moyapi.py
# Compiled at: 2017-08-24 09:37:52
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
import os, io, sys, argparse, getpass, requests, tempfile
from .. import archive
from .. import settings
from .. import jsonrpc
from .. import package
from .. import versioning
from ..wsgi import WSGIApplication
from ..console import Console, Cell
from ..compat import text_type, raw_input
from ..command import downloader
from ..tools import get_moya_dir, is_moya_dir, nearest_word, decode_utf8_bytes
from .. import build
from . import installer
from . import dependencies
import fs.copy
from fs.path import relativefrom, join
from fs.opener import open_fs
from fs.tempfs import TempFS
from fs.zipfs import ZipFS
from fs.osfs import OSFS
DEFAULT_CONF = b'~/.moyapirc'
DEFAULT_HOST = b'https://packages.moyaproject.com/jsonrpc/'

class MOYAPI_ERRORS():
    ok = 0
    no_user = 1
    password_failed = 2
    auth_failed = 3
    no_access = 4
    no_organization = 5
    no_package = 6
    no_release = 7
    lib_invalid = 8
    organization_create_error = 9
    version_invalid = 10


class CommandError(Exception):
    pass


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


class MoyaPI(object):
    """Moya Package Index
==================

Find, install and manage Moya libraries
"""

    def __init__(self):
        self._rpc = None
        self._settings = None
        self.console = Console()
        self.moya_libs = self._get_moya_libs()
        return

    @property
    def moyapirc_path(self):
        return os.path.expanduser(DEFAULT_CONF)

    def set_settings_defaults(self, settings):
        pass

    def _get_moya_libs(self):
        archive.MOYA_LIBS_PATH
        moya_libs = {name:version for name, version, _, _ in archive.Archive.scan_libs([archive.MOYA_LIBS_PATH], None)}
        return moya_libs

    @property
    def settings(self):
        if self._settings is None:
            try:
                with io.open(os.path.expanduser(DEFAULT_CONF), b'rt') as (f):
                    self._settings = settings.SettingsContainer.read_from_file(f)
            except IOError:
                self._settings = settings.SettingsContainer()
                self.set_settings_defaults(self._settings)

        return self._settings

    @property
    def user(self):
        username = self.settings.get(b'user', b'active', None)
        if not username:
            raise CommandError(b'no active user (run moya-pm auth or moya-pm user)')
        return username

    @property
    def auth_token(self):
        user = self.user
        token = self.settings.get((b'auth:{}').format(user), b'token', None)
        if not token:
            raise CommandError(b'no auth token found (run moya-pm auth or moya-pm user)')
        return token

    def write_settings(self):
        with io.open(os.path.expanduser(DEFAULT_CONF), b'wt') as (f):
            self.settings.export(f, b'Written by moya-pm')

    @property
    def rpc(self):
        """Get the JSONRPC interface"""
        server_url = self.settings.get(b'server', b'url', DEFAULT_HOST)
        self.settings.set(b'server', b'url', server_url)
        if self._rpc is None:
            self._rpc = jsonrpc.JSONRPC(server_url, ssl_verify=False)
        return self._rpc

    def call(self, method, **params):
        """Call an rpc method, exit if server is unreachable"""
        try:
            response = self.rpc.call(method, **params)
        except IOError as e:
            self.console.error((b'Unable to reach server ({})').format(e))
            sys.exit(-1)
        else:
            if isinstance(response, dict) and b'message' in response:
                for line in response[b'message'].splitlines():
                    if line.strip():
                        self.console(b'[server] ', fg=b'green')(line).nl()

            return response

    def get_argparse(self):
        parser = MoyaArgumentParser(prog=b'moya-pm', description=self.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=b'Need Help? http://moyaproject.com')
        parser.add_argument(b'-d', b'--debug', dest=b'debug', action=b'store_true', help=b'enable debug information (show tracebacks)')
        subparsers = parser.add_subparsers(title=b'available sub-commands', dest=b'subcommand', help=b'sub-command help')
        auth_parser = subparsers.add_parser(b'auth', help=b'authorize with the server', description=b'Request authorization from the server (run once)')
        auth_parser.add_argument(b'-u', b'--username', dest=b'username', default=None)
        auth_parser.add_argument(b'-p', b'--password', dest=b'password', default=None)
        user_parser = subparsers.add_parser(b'user', help=b'switch active user', description=b'Switch between active user if you have multiple accounts')
        user_parser.add_argument(dest=b'user', default=None, nargs=b'?')
        register_parser = subparsers.add_parser(b'register', help=b'register a package', description=b'Register a new package with the server')
        register_parser.add_argument(dest=b'location', help=b'library location')
        build_parser = subparsers.add_parser(b'build', help=b'build a package', description=b'Build a library')
        build_parser.add_argument(dest=b'location', metavar=b'PATH', help=b'Library location')
        build_parser.add_argument(b'-f', b'--force', dest=b'force', action=b'store_true', help=b'Overwrite the package if it exists')
        build_parser.add_argument(b'-u', b'--upload', dest=b'upload', action=b'store_true', help=b'Also upload package')
        build_parser.add_argument(b'--overwrite', dest=b'overwrite', action=b'store_true', default=False, help=b'Force over-writing of releases')
        upload_parser = subparsers.add_parser(b'upload', help=b'upload a package', description=b'Upload a package')
        upload_parser.add_argument(dest=b'location', help=b'Library location')
        upload_parser.add_argument(b'--version', dest=b'version', default=None, required=False, help=b'version to upload')
        upload_parser.add_argument(b'--overwrite', dest=b'overwrite', action=b'store_true', default=False, help=b'force over-writing of releases')
        upload_parser.add_argument(b'-d', b'--docs', dest=b'docs', default=False, action=b'store_true', help=b'upload docs')
        list_parser = subparsers.add_parser(b'list', help=b'list package releases', description=b'List all releases for a package')
        list_parser.add_argument(dest=b'package', metavar=b'PACKAGE', help=b'Package to list (may also include version spec e.g. moya-pm list "moya.packet>=1.1.0)"')
        install_parser = subparsers.add_parser(b'install', help=b'install a package', description=b'Download and install a library')
        install_parser.add_argument(dest=b'packages', metavar=b'PACKAGES', nargs=b'*', help=b'Package to installed (may include version spec e.g. moya.package>=1.0)')
        install_parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        install_parser.add_argument(b'-i', b'--ini', dest=b'settings', default=b'settings.ini', metavar=b'SETTINGSPATH', help=b'path to project settings file')
        install_parser.add_argument(b'-s', b'--server', dest=b'server', default=b'main', metavar=b'SERVERREF', help=b'server element to use')
        install_parser.add_argument(b'-d', b'--download', dest=b'download', default=None, metavar=b'DIRECTORY', help=b"don't install package, just download package to DIRECTORY")
        install_parser.add_argument(b'-b', b'--lib-dir', dest=b'output', default=b'external/', metavar=b'DIRECTORY', help=b'directory to install the library (relative to project root)')
        install_parser.add_argument(b'-f', b'--force', dest=b'force', default=False, action=b'store_true', help=b'force overwrite of installed package')
        install_parser.add_argument(b'--upgrade', dest=b'upgrade', default=False, action=b'store_true', help=b'upgrade existing version')
        install_parser.add_argument(b'--mount', dest=b'mount', default=None, help=b'optional path to mount application')
        install_parser.add_argument(b'--app', dest=b'app', default=None, help=b'name of app to install')
        install_parser.add_argument(b'--no-add', dest=b'no_add', default=False, action=b'store_true', help=b"don't add to server.xml")
        install_parser.add_argument(b'--no-deps', dest=b'no_deps', default=False, action=b'store_true', help=b"don't install dependencies")
        return parser

    def run(self):
        parser = self.get_argparse()
        self.args = args = parser.parse_args(sys.argv[1:])
        if self.args.subcommand is None:
            parser.print_usage()
            return 1
        else:
            method_name = b'run_' + args.subcommand.replace(b'_', b'-')
            try:
                return getattr(self, method_name)() or 0
            except CommandError as e:
                self.console.error(text_type(e))
                return -1
            except jsonrpc.JSONRPCError as e:
                self.server_response(e.message, bold=True, fg=b'red')
                return e.code
            except Exception as e:
                self.console.error(text_type(e))
                if args.debug:
                    raise
                return -1

            return

    def server_response(self, text, **style):
        for line in text.splitlines():
            self.console(b'[server] ', **style)(line.lstrip()).nl()

    def run_auth(self):
        args = self.args
        username = args.username
        if username is None:
            username = getpass.getuser()
            if username:
                msg = (b'username ({}): ').format(username)
            else:
                msg = b'username: '
            username = raw_input(msg) or username
            if not username:
                self.console.error(b'a username is required (see http://packages.moyaproject.com)')
                return
        password = args.password
        if password is None:
            password = getpass.getpass((b"{}'s password: ").format(username))
        auth_result = self.call(b'auth.get-token', username=username, password=password)
        auth_token = auth_result[b'token']
        self.settings.set((b'auth:{}').format(username), b'token', auth_token)
        active_user = self.settings.get(b'user', b'active', None)
        if active_user is None:
            self.settings.set(b'user', b'active', username)
        self.write_settings()
        self.console.success((b"wrote auth token to '{}'").format(self.moyapirc_path))
        return

    def run_user(self):
        args = self.args
        username = args.user
        if username is None:
            active_user = self.settings.get(b'user', b'active', None)
            if active_user is None:
                self.console.text(b'no active user')
            else:
                self.console.text((b"active username is '{}'").format(active_user))
        else:
            self.settings.set(b'user', b'active', username)
            self.write_settings()
            self.console.text((b"switched active user to '{}'").format(username))
        return

    def run_register(self):
        args = self.args
        auth_token = self.auth_token
        path = os.path.abspath(os.path.join(args.location, b'lib.ini'))
        try:
            with io.open(path, b'rt') as (f):
                lib_settings = settings.SettingsContainer.read_from_file(f)
        except IOError:
            self.console.error((b"unable to read library settings from '{}'").format(path))
            return -1

        def get(section, key, default=Ellipsis):
            try:
                return lib_settings.get(section, key, default=default)
            except:
                raise CommandError((b'key [{}]/{} was not found in lib.ini').format(section, key))

        lib = dict(lib_settings[b'lib'])
        self.call(b'package.register', auth=auth_token, lib=lib)

    def run_build(self):
        args = self.args
        path = os.path.abspath(os.path.join(args.location, b'lib.ini'))
        try:
            with io.open(path, b'rt') as (f):
                lib_settings = settings.SettingsContainer.read_from_file(f)
        except IOError:
            self.console.error((b"unable to read library settings from '{}'").format(path))
            return -1

        lib_name = lib_settings.get(b'lib', b'name')
        lib_version = lib_settings.get(b'lib', b'version')
        package_name = (b'{}-{}').format(lib_name, lib_version)
        package_filename = (b'{}.zip').format(package_name)
        exclude_wildcards = lib_settings.get_list(b'package', b'exclude')
        exclude_wildcards.append(b'__moyapackage__/*')
        lib_fs = open_fs(args.location)
        package_destination_fs = lib_fs.makedir(b'__moyapackage__', recreate=True)
        if not args.force and package_destination_fs.exists(package_filename):
            raise CommandError((b"package '{}' exists, use --force to overwrite").format(package_filename))
        package.make_package(lib_fs, package_destination_fs, package_filename, exclude_wildcards, auth_token=self.auth_token)
        output_path = package_destination_fs.getsyspath(package_filename)
        self.console.text((b"built '{}'").format(package_filename))
        if args.upload:
            upload_info = self.call(b'package.get-upload-info')
            upload_url = upload_info[b'url']
            self.upload(upload_url, lib_name, lib_version, package_destination_fs, package_filename, overwrite=args.overwrite)

    def upload(self, url, package_name, version, build_fs, filename, overwrite=False):
        self.console((b"uploading '{}'...").format(filename)).nl()
        if not overwrite:
            try:
                self.call(b'package.get-download-info', package=package_name, version=version)
            except jsonrpc.JSONRPCError as e:
                if e.code != 7:
                    raise
            else:
                raise CommandError(b'Upload failed because this release exists. It generally better to create a new release than overwrite an existing one.\nUse the --overwrite switch if you really want to do this.')

        with build_fs.open(filename, b'rb') as (package_file):
            files = [
             (
              b'file', (filename, package_file, b'application/octet-stream'))]
            data = {b'auth': self.auth_token, b'package': package_name, 
               b'version': version}
            username = self.settings.get(b'upload', b'username', None)
            password = self.settings.get(b'upload', b'password', None)
            if username and password:
                auth = (
                 username, password)
            else:
                auth = None
            response = requests.post(url, verify=False, auth=auth, files=files, data=data, hooks={})
        if response.status_code != 200:
            raise CommandError((b'upload failed -- server returned {} response').format(response.status_code))
        message = decode_utf8_bytes(response.headers.get(b'moya-upload-package-message', b''))
        result = decode_utf8_bytes(response.headers.get(b'moya-upload-package-result', b''))
        if result == b'success':
            self.server_response(message, fg=b'green')
        else:
            raise CommandError(message)
        return

    def run_upload(self):
        args = self.args
        path = os.path.abspath(os.path.join(args.location, b'lib.ini'))
        try:
            with io.open(path, b'rt') as (f):
                lib_settings = settings.SettingsContainer.read_from_file(f)
        except IOError:
            self.console.error((b"unable to read library settings from '{}'").format(path))
            return -1

        lib_name = lib_settings.get(b'lib', b'name')
        lib_version = args.version or lib_settings.get(b'lib', b'version')
        if args.docs:
            return self.upload_docs(lib_name, lib_version)
        package_name = (b'{}-{}').format(lib_name, lib_version)
        package_filename = (b'{}.zip').format(package_name)
        upload_info = self.call(b'package.get-upload-info')
        upload_url = upload_info[b'url']
        lib_fs = open_fs(args.location)
        package_destination_fs = lib_fs.makedir(b'__moyapackage__', recreate=True)
        if not package_destination_fs.exists(package_filename):
            raise CommandError((b"package '{}' does not exist, run 'moya-pm build'").format(package_filename))
        self.upload(upload_url, lib_name, lib_version, package_destination_fs, package_filename, overwrite=args.overwrite)

    def upload_docs(self, lib_name, lib_version):
        args = self.args
        archive, lib = build.build_lib(args.location, ignore_errors=True)
        lib_name = lib.long_name
        from ..docgen.extracter import Extracter
        extract_fs = TempFS((b'moyadoc-{}').format(lib_name))
        extracter = Extracter(archive, extract_fs)
        extracter.extract_lib(lib_name)
        _fh, temp_filename = tempfile.mkstemp(b'moyadocs')
        with ZipFS(temp_filename, b'w') as (docs_zip_fs):
            fs.copy.copy_dir(extract_fs, b'/', docs_zip_fs, b'/')
        package_filename = (b'{}-{}.docs.zip').format(lib_name, lib_version)
        upload_info = self.call(b'package.get-upload-info')
        docs_url = upload_info[b'docs_url']
        self.console((b"uploading '{}'...").format(package_filename)).nl()
        with io.open(temp_filename, b'rb') as (package_file):
            files = [
             (
              b'file', (package_filename, package_file, b'application/octet-stream'))]
            data = {b'auth': self.auth_token, b'package': lib_name, 
               b'version': lib_version}
            response = requests.post(docs_url, verify=False, files=files, data=data, hooks={})
        if response.status_code != 200:
            raise CommandError((b'upload failed -- server returned {} response').format(response.status_code))
        message = decode_utf8_bytes(response.headers.get(b'moya-upload-package-message', b''))
        result = decode_utf8_bytes(response.headers.get(b'moya-upload-package-result', b''))
        if result == b'success':
            self.server_response(message, fg=b'green')
        else:
            raise CommandError((b'upload error ({})').format(message))
        if result == b'success':
            pass
        else:
            self.console.error(b'upload failed')

    def run_list(self):
        args = self.args
        package = args.package
        version_spec = versioning.VersionSpec(package)
        releases = self.call(b'package.list-releases', package=version_spec.name)[b'releases']
        releases.sort(key=lambda r: versioning.Version(r[b'version']))
        table = []
        for release in releases:
            if version_spec.comparisons and release[b'version'] not in version_spec:
                continue
            table.append([Cell(release[b'version'], bold=True, fg=b'magenta'), release[b'notes']])

        self.console.table(table, header_row=[b'version', b'release notes'])

    @property
    def location(self):
        _location = getattr(self, b'_location', None)
        if _location is not None:
            return _location
        else:
            location = self.args.location
            if location is None:
                location = b'./'
            if location and b'://' in location:
                return location
            try:
                location = get_moya_dir(location) + b'/'
            except ValueError:
                raise CommandError(b'Moya project directory not found, run this command from a project directory or specify --location')

            if not is_moya_dir(location):
                raise CommandError(b"Location is not a moya project (no 'moya' file found)")
            self._location = location
            return location

    def select_packages(self, packages):
        """Select packages from a list of version specs."""
        selected = []
        for _package in packages:
            version_spec = versioning.VersionSpec(_package)
            try:
                select = self.call(b'package.select', package=_package)
            except jsonrpc.RemoteMethodError as error:
                if error.code == MOYAPI_ERRORS.no_package:
                    select = None
                else:
                    raise

            selected.append((_package, select))

        for _package, package_select in selected:
            if package_select is None:
                version_spec = versioning.VersionSpec(_package)
                raise CommandError((b"requested package '{}' was not found").format(version_spec.name))
            if package_select[b'version'] is None:
                raise CommandError((b"no installation candidate for '{}'").format(_package))

        return selected

    def check_existing(self, package_installs):
        """Check if packages are already installed."""
        if not (self.args.force or self.args.download):
            try:
                application = WSGIApplication(self.location, self.args.settings, disable_autoreload=True, test_build=True)
                archive = application.archive
                if archive is None:
                    raise CommandError(b'unable to load project, use the --force switch to force installation')
            except Exception as e:
                if not self.args.force:
                    self.console.exception(e)
                    raise CommandError(b'unable to load project, use the --force switch to force installation')

            for package_name, install_version in package_installs:
                libs = [ (lib.long_name, lib.version, lib.install_location) for lib in archive.libs.values() if lib.long_name == package_name ]
                for name, version, location in libs:
                    if name == package_name:
                        if version > install_version:
                            raise CommandError((b'a newer version ({}) of package {} is already installed, use --force to force installation').format(version, name))
                        elif install_version == version:
                            raise CommandError((b'version {} of {} is already installed, use --force to force installation').format(version, name))
                        elif not self.args.upgrade:
                            raise CommandError((b'an older version ({}) of {} is installed, use --upgrade to force upgrade').format(version, name))

            return application
        return

    def install_packages(self, output_fs, selected_packages, application=None):
        """Install packages"""
        download_fs = TempFS()
        install_packages = []
        for index, (_, select_package) in enumerate(selected_packages):
            app_name = self.args.app or select_package[b'name'].split(b'.', 1)[(-1)].replace(b'.', b'')
            _install = self.download_package(download_fs, select_package, app=app_name if index == 0 else None, mount=self.args.mount if index == 0 else None)
            install_packages.append(_install)

        installed = []
        if application:
            cfg = application.archive.cfg
        else:
            cfg = build.read_config(self.location, self.args.settings)
        changed_server = False
        for _package in install_packages:
            _changed_server, _installed_packages = self.install_package(download_fs, output_fs, _package, cfg=cfg)
            installed.extend(_installed_packages)
            changed_server = changed_server or _changed_server

        table = []
        for _package, mount in installed:
            table.append([Cell((b'{name}').format(**_package), fg=b'magenta', bold=True),
             Cell((b'{version}').format(**_package)),
             Cell(_package[b'location'], fg=b'blue', bold=True),
             Cell(mount or b'', fg=b'cyan', bold=True)])

        if table:
            self.console.table(table, [b'package', b'version', b'location', b'mount'])
        if application is not None:
            archive = application.archive
            logic_location = archive.cfg.get(b'project', b'location')
            server_xml = archive.cfg.get(b'project', b'startup')
            server_xml = archive.project_fs.getsyspath(join(logic_location, server_xml))
            if changed_server:
                self.console.text((b"moya-pm modified '{}' -- please check changes").format(server_xml), fg=b'green', bold=b'yes')
        return

    def install_package(self, download_fs, output_fs, packages, cfg=None):
        args = self.args
        changed_server_xml = False
        installed = []
        for package_name, (app_name, mount, package_select) in packages.items():
            if package_select[b'system']:
                install_location = None
                package_select[b'location'] = b'<builtin>'
            else:
                package_name = package_select[b'name']
                install_version = versioning.Version(package_select[b'version'])
                filename = (b'{}-{}.{}').format(package_name, install_version, package_select[b'md5'])
                download_url = package_select[b'download']
                install_location = relativefrom(self.location, join(self.location, args.output, package_select[b'name']))
                package_select[b'location'] = install_location
            with download_fs.open(filename, b'rb') as (package_file):
                with ZipFS(package_file) as (package_fs):
                    with output_fs.makedir(package_select[b'name'], recreate=True) as (lib_fs):
                        lib_fs.removetree(b'/')
                        fs.copy.copy_dir(package_fs, b'/', lib_fs, b'/')
                        installed.append((package_select, mount))
            if not args.no_add:
                server_xml = cfg.get(b'project', b'startup')
                changed_server_xml = installer.install(project_path=self.location, server_xml_location=cfg.get(b'project', b'location'), server_xml=server_xml, server_name=args.server, lib_path=install_location, lib_name=package_name, app_name=app_name, mount=mount)

        return (
         changed_server_xml, installed)

    def download_package(self, download_fs, select_package, app=None, mount=None):
        args = self.args
        username = self.settings.get(b'upload', b'username', None)
        password = self.settings.get(b'upload', b'password', None)
        if username and password:
            auth = (
             username, password)
        else:
            auth = None
        _install = (b'{}=={}').format(select_package[b'name'], select_package[b'version'])
        packages = dependencies.gather_dependencies(self.rpc, app, mount, _install, self.console, no_deps=args.no_deps, ignore_libs=self.moya_libs)
        if not args.no_add:
            for package_name, (app_name, mount, package_select) in packages.items():
                if package_select[b'version'] is None:
                    raise CommandError((b"no install candidate for dependency '{}', run 'moya-pm list {}' to see available packages").format(package_name, package_name))

        for package_name, (app_name, mount, package_select) in packages.items():
            if package_select[b'system']:
                continue
            package_name = package_select[b'name']
            install_version = versioning.Version(package_select[b'version'])
            filename = (b'{}-{}.{}').format(package_name, install_version, package_select[b'md5'])
            download_url = package_select[b'download']
            package_filename = download_url.rsplit(b'/', 1)[(-1)]
            with download_fs.open(filename, b'wb') as (package_file):
                checksum = downloader.download(download_url, package_file, console=self.console, auth=auth, verify_ssl=False, msg=(b'requesting {name}=={version}').format(**package_select))
                if checksum != package_select[b'md5']:
                    raise CommandError((b"md5 checksum of download doesn't match server! download={}, server={}").format(checksum, package_select[b'md5']))
            if args.download:
                with open_fs(args.download) as (dest_fs):
                    fs.copy.copy_file(download_fs, filename, dest_fs, package_filename)

        return packages

    def run_install(self):
        args = self.args
        selected_packages = self.select_packages(args.packages)
        package_installs = [ (p[b'name'], versioning.Version(p[b'version'])) for _spec, p in selected_packages
                           ]
        application = self.check_existing(package_installs)
        output_path = args.download if args.download is not None else join(self.location, args.output)
        output_fs = OSFS(output_path, create=True)
        self.install_packages(output_fs, selected_packages, application=application)
        for name, package in selected_packages:
            if package[b'notes']:
                self.console.table([[package[b'notes']]], [(b'{name} {version} release notes').format(**package)])

        return


def main():
    return MoyaPI().run()