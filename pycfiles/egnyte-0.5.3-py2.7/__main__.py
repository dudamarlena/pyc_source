# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/__main__.py
# Compiled at: 2017-05-23 09:48:11
from __future__ import print_function, unicode_literals
import getpass, argparse, json, sys, datetime, codecs
from contextlib import closing
from egnyte import client, configuration, exc, base
parser_kwargs = dict(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))

def create_main_parser():
    main = argparse.ArgumentParser(prog=b'python -m egnyte', **parser_kwargs)
    main.add_argument(b'-c', b'--config-path', help=b'Path to config file')
    main.add_argument(b'-v', b'--verbose', action=b'count', dest=b'verbosity', help=b'Be more verbose. Can be repeated for debugging', default=0)
    main.add_argument(b'--impersonate', metavar=b'USERNAME', help=b'Impersonate another user (username or email)', default=None)
    subparsers = main.add_subparsers()
    parser_config = subparsers.add_parser(b'config', help=b'commands related to configuration', **parser_kwargs)
    subparsers_config = parser_config.add_subparsers()
    parser_config_show = subparsers_config.add_parser(b'show', help=b'show configuration', **parser_kwargs)
    parser_config_show.set_defaults(command=b'config_show')
    parser_config_create = subparsers_config.add_parser(b'create', help=b'create a new configuration file', **parser_kwargs)
    parser_config_create.set_defaults(command=b'config_create')
    parser_config_update = subparsers_config.add_parser(b'update', help=b'update a configuration file', **parser_kwargs)
    parser_config_update.set_defaults(command=b'config_update')
    parser_config_token = subparsers_config.add_parser(b'token', help=b'generate a new access token and store it in config file', **parser_kwargs)
    parser_config_token.set_defaults(command=b'config_token')
    parser_token = subparsers.add_parser(b'token', help=b'generate a new access token and print it', **parser_kwargs)
    parser_token.set_defaults(command=b'token')
    parser_test = subparsers.add_parser(b'test', help=b'test if config is correct (connects to service)', **parser_kwargs)
    parser_test.set_defaults(command=b'test')
    for parser, required in [(parser_config_create, True), (parser_config_update, False), (parser_token, False)]:
        parser.add_argument(b'-d', b'--domain', required=required, help=b'domain name')
        parser.add_argument(b'-l', b'--login', required=False, help=b'login')
        parser.add_argument(b'-p', b'--password', required=False, help=b'password')
        parser.add_argument(b'-k', b'--key', dest=b'api_key', required=required, help=b'API key')

    for parser in (parser_config_create, parser_config_update):
        parser.add_argument(b'-t', b'--token', dest=b'access_token', required=False, help=b'API access token')
        parser.add_argument(b'-T', b'--timeout', required=False, help=b'Request timeout')

    parser_audit = subparsers.add_parser(b'audit', help=b'generate audit reports', **parser_kwargs)
    subparsers_audit = parser_audit.add_subparsers()
    parser_audit_files = subparsers_audit.add_parser(b'files', help=b'create Files report', **parser_kwargs)
    parser_audit_files.set_defaults(command=b'audit_files')
    parser_audit_logins = subparsers_audit.add_parser(b'logins', help=b'create Logins report', **parser_kwargs)
    parser_audit_logins.set_defaults(command=b'audit_logins')
    parser_audit_permissions = subparsers_audit.add_parser(b'permissions', help=b'create Permissions report', **parser_kwargs)
    parser_audit_permissions.set_defaults(command=b'audit_permissions')
    parser_audit_get = subparsers_audit.add_parser(b'get', help=b'get a previously generated report', **parser_kwargs)
    parser_audit_get.set_defaults(command=b'audit_get')
    for parser in (parser_audit_files, parser_audit_logins, parser_audit_permissions, parser_audit_get):
        parser.add_argument(b'--save', required=False, default=None, help=b'File to save to the report to (default is standard output)')

    for parser in (parser_audit_files, parser_audit_logins, parser_audit_permissions):
        parser.add_argument(b'--format', required=False, default=b'csv', help=b'Report type (json or csv. Default is csv)')
        parser.add_argument(b'--start', required=False, default=b'yesterday', help=b'Start date (YYYY-MM-DD)')
        parser.add_argument(b'--end', required=False, default=b'today', help=b'End date (YYYY-MM-DD)')

    parser_audit_files.add_argument(b'--folder', required=False, action=b'append', default=None, help=b"Absolute folder path for the destination folder. 'folder' or 'file' is required. Can be used multiple times")
    parser_audit_files.add_argument(b'--file', required=False, default=None, help=b"Absolute folder path for the destination file, wildcards allowed. 'folder' or 'file' is required")
    parser_audit_files.add_argument(b'--users', required=False, default=None, help=b'Users to report on (comma separated list, default is all)')
    parser_audit_files.add_argument(b'--transaction_type', required=False, default=None, help=b'\n    Transaction type: upload, download, preview, delete, copy, move, restore_trash, delete_trash, create_link, delete_link, download_link\n    (comma separated list, default is all')
    parser_audit_logins.add_argument(b'--events', required=True, help=b'Event types: logins, logouts, account_lockouts, password_resets, failed_attempts (comma separated list)')
    parser_audit_logins.add_argument(b'--access-points', required=False, default=None, help=b'Access points to cover: Web, FTP, Mobile (comma separated list, default is all)')
    parser_audit_logins.add_argument(b'--users', required=False, default=None, help=b'Users to report on (comma separated list, default is all)')
    parser_audit_permissions.add_argument(b'--assigners', required=True, help=b'Permission assigners (comma separated list)')
    parser_audit_permissions.add_argument(b'--folder', required=True, action=b'append', default=None, help=b'Absolute folder path for the destination folder. Can be used multiple times')
    parser_audit_permissions.add_argument(b'--users', required=False, default=None, help=b'Users to report on (comma separated list)')
    parser_audit_permissions.add_argument(b'--groups', required=False, default=None, help=b'Groups to report on (comma separated list)')
    parser_audit_get.add_argument(b'--id', type=int, required=True, help=b'Id of the report')
    parser_upload = subparsers.add_parser(b'upload', help=b'send files to Egnyte', **parser_kwargs)
    parser_upload.set_defaults(command=b'upload')
    parser_upload.add_argument(b'paths', nargs=b'+', help=b'Paths (files to directories) to upload')
    parser_upload.add_argument(b'target', help=b'Path in Cloud File System to upload to')
    parser_upload.add_argument(b'-x', b'--exclude', action=b'append', default=None, help=b'Exclude items that match this glob pattern')
    parser_download = subparsers.add_parser(b'download', help=b'download files from Egnyte', **parser_kwargs)
    parser_download.set_defaults(command=b'download')
    parser_download.add_argument(b'paths', nargs=b'+', help=b'Paths (files to directories) to download')
    parser_download.add_argument(b'--target', help=b'Local directory to put downloaded files and directories in', default=b'.')
    parser_download.add_argument(b'--overwrite', action=b'store_const', const=True, default=False, help=b'Delete local files and directories that conflict with cloud content')
    parser_settings = subparsers.add_parser(b'settings', help=b'show domain settings', **parser_kwargs)
    parser_settings.set_defaults(command=b'settings')
    parser_search = subparsers.add_parser(b'search', help=b'search for files', **parser_kwargs)
    parser_search.set_defaults(command=b'search')
    parser_search.add_argument(b'query', help=b'Search query')
    parser_search.add_argument(b'--mtime_from', help=b'Minimim modification date', default=None)
    parser_search.add_argument(b'--mtime_to', help=b'Maximum modification date', default=None)
    parser_search.add_argument(b'--folder', help=b'Limit search to a specified folder', default=None)
    parser_events = subparsers.add_parser(b'events', help=b'show events from the domain', **parser_kwargs)
    parser_events.set_defaults(command=b'events')
    parser_events.add_argument(b'--start', type=int, help=b'Starting event id. Default or 0 - last seen event. Negative numbers are counter backwards from last event', default=None)
    parser_events.add_argument(b'--stop', type=int, help=b'Stop event id. Default - poll indefinitely. 0 means last event. Negative numbers are counter backwards from last event', default=None)
    parser_events.add_argument(b'--type', action=b'append', help=b'Limit to events of specific type', default=None)
    parser_events.add_argument(b'--folder', help=b"Limit to events in specific folder and it's subfolders", default=None)
    parser_events.add_argument(b'--suppress', help=b'Skip events caused by this app or user. Valid values: app, user.', default=None)
    return main


def to_json(obj):
    return {k:v for k, v in obj.__dict__.items() if not k.startswith(b'_') if not k.startswith(b'_')}


class Commands(object):
    _config = None
    config_keys = ('login', 'password', 'domain', 'api_key', 'access_token', 'timeout')
    STATUS_CMD_NOT_FOUND = 1
    STATUS_API_ERROR = 2
    INFO = 1
    DEBUG = 2

    def load_config(self):
        if self._config is None:
            self._config = configuration.load(self.args.config_path)
        return self._config

    def save_config(self):
        return configuration.save(self.config, self.args.config_path)

    config = property(load_config)

    def __init__(self, args):
        self.args = args

    @property
    def info(self):
        """If verbosity is INFO or better"""
        return self.args.verbosity >= self.INFO

    @property
    def debug(self):
        """If verbosity is INFO or better"""
        return self.args.verbosity >= self.DEBUG

    def run(self):
        if not hasattr(self.args, b'command'):
            print(b'Use -h or --help for help')
            return
        else:
            method = getattr(self, b'cmd_%s' % self.args.command, None)
            if self.debug:
                print(b'running %s' % method.__name__)
            if method is None:
                print(b"Command '%s' not implemented yet" % self.args.command.replace(b'_', b' '))
                return self.STATUS_CMD_NOT_FOUND
            try:
                return method()
            except exc.EgnyteError as e:
                if self.debug:
                    raise
                print(repr(e))
                return self.STATUS_API_ERROR

            return

    def get_client(self):
        result = client.EgnyteClient(self.config)
        if self.args.impersonate is not None:
            result.impersonate(self.args.impersonate)
        return result

    def get_access_token(self):
        config = self.require_password()
        return base.get_access_token(config)

    def merge_config(self):
        """Merge loaded config with command line params"""
        for key in self.config_keys:
            if getattr(self.args, key, None) is not None:
                self.config[key] = getattr(self.args, key)

        return

    def require_password(self):
        """If config does not contain a password, ask user for it, but don't store it"""
        if self.config[b'password']:
            return self.config
        else:
            config = self.config.copy()
            config[b'password'] = getpass.getpass(b'Enter the password: ')
            return config

    def print_json(self, obj):
        print(json.dumps(obj, indent=2, sort_keys=True, default=to_json))

    def cmd_config_show(self):
        self.print_json(self.config)

    def cmd_config_create(self):
        self._config = {}
        self.merge_config()
        self.save_config()

    def cmd_config_update(self):
        self.merge_config()
        self.save_config()

    def cmd_config_token(self):
        self.config[b'access_token'] = self.get_access_token()
        self.save_config()

    def cmd_token(self):
        self.merge_config()
        print(self.get_access_token())

    def cmd_test(self):
        api = self.get_client()
        info = api.user_info()
        print(b'Connection successful for user %s' % (info[b'username'],))

    def cmd_search(self):
        api = self.get_client()
        results = api.search.files(self.args.query, modified_before=self.args.mtime_to, modified_after=self.args.mtime_from, folder=self.args.folder)
        self.print_json(results)

    def common_audit_args(self):
        format = self.args.format
        date_start = self.date(self.args.start)
        date_end = self.date(self.args.end)
        return (format, date_start, date_end)

    def date(self, value):
        """Poor mans human readable dates"""
        if value == b'today':
            return datetime.date.today()
        else:
            if value == b'yesterday':
                return datetime.date.today() - datetime.timedelta(days=1)
            return datetime.date.datetime.strptime(value, b'%Y-%m-%d').date()

    def wait_and_save_report(self, report):
        if self.args.save:
            output = open(self.args.save, b'wb')
            print(b'Opened %s for writing, requesting report')
            with closing(output):
                report.wait()
                report.download().write_to(output)
        else:
            report.wait()
            download = report.download()
            with closing(download):
                lines = codecs.iterdecode(iter(download), b'UTF-8')
                for line in lines:
                    print(line)

    def comma_split(self, param):
        value = getattr(self.args, param, None)
        if value:
            return value.split(b',')
        else:
            return

    def cmd_audit_get(self):
        api = self.get_client()
        audits = api.audits
        report = audits.get(id=self.args.id)
        return self.wait_and_save_report(report)

    def cmd_audit_files(self):
        api = self.get_client()
        audits = api.audits
        folders = getattr(self.args, b'folder', None)
        file = self.args.file
        users = self.comma_split(b'users')
        transaction_type = self.comma_split(b'transaction_type')
        report = audits.files(folders=folders, file=file, users=users, transaction_type=transaction_type, *self.common_audit_args())
        return self.wait_and_save_report(report)

    def cmd_audit_permissions(self):
        api = self.get_client()
        audits = api.audits
        assigners = self.comma_split(b'assigner')
        folders = self.args.folder
        users = self.comma_split(b'users')
        groups = self.comma_split(b'groups')
        report = audits.permissions(assigners=assigners, folders=folders, users=users, groups=groups, *self.common_audit_args())
        return self.wait_and_save_report(report)

    def cmd_audit_logins(self):
        api = self.get_client()
        audits = api.audits
        users = self.comma_split(b'users')
        events = self.comma_split(b'events')
        access_points = self.comma_split(b'access_points')
        report = audits.logins(events=events, access_points=access_points, users=users, *self.common_audit_args())
        return self.wait_and_save_report(report)

    def transfer_callbacks(self):
        if self.info:
            if sys.stdout.isatty():
                result = TerminalCallbacks()
                if self.debug:
                    result.force_newline = True
                return result
            return VerboseCallbacks()

    def cmd_upload(self):
        api = self.get_client()
        api.bulk_upload(self.args.paths, self.args.target, self.args.exclude, self.transfer_callbacks())

    def cmd_download(self):
        api = self.get_client()
        api.bulk_download(self.args.paths, self.args.target, self.args.overwrite, self.transfer_callbacks())

    def cmd_settings(self):
        self.print_json(self.get_client().settings)

    def cmd_events(self):
        start = self.args.start
        stop = self.args.stop
        events = self.get_client().events
        if start is None:
            start = events.latest_event_id
        else:
            if start <= 0:
                start = events.latest_event_id + start
            if stop is not None and stop <= 0:
                stop = events.latest_event_id + stop
            events = events.filter(start_id=start, suppress=self.args.suppress, folder=self.args.folder, types=self.args.type or None)
            try:
                for event in events:
                    self.print_json(event)
                    print()
                    if stop is not None and event.id >= stop:
                        break

            except KeyboardInterrupt:
                pass

        return


class VerboseCallbacks(client.ProgressCallbacks):
    """Progress callbacks used when sys.stdout is a file or a pipe"""

    def write(self, text, force_newline=False):
        print(text)

    def getting_info(self, cloud_path):
        self.write(b'Getting info about %s' % cloud_path)

    def got_info(self, cloud_obj):
        self.write(b'Got info about %s' % cloud_obj.path)

    def download_start(self, local_path, cloud_file, size):
        self.write(b'Downloading %s' % local_path)
        self.current = local_path

    def upload_start(self, local_path, cloud_file, size):
        self.write(b'Uploading %s' % local_path)
        self.current = local_path

    def creating_directory(self, cloud_folder):
        self.write(b'Creating directory %s' % cloud_folder.path)

    def skipped(self, cloud_obj, reason):
        self.write(b'Skipped %s: %s' % (cloud_obj.path, reason), force_newline=True)

    def finished(self):
        self.write(b'Finished', force_newline=True)


class TerminalCallbacks(VerboseCallbacks):
    """Progress callbacks used when sys.stdout is a terminal"""
    force_newline = False

    def __init__(self):
        self.last_len = 0

    def write(self, text, force_newline=None):
        if force_newline is None:
            force_newline = self.force_newline
        output = [
         b'\r']
        sys.stdout.write(b'\r')
        if len(text) < self.last_len:
            sys.stdout.write(b' ' * self.last_len)
            sys.stdout.write(b'\r')
        output.append(text)
        if force_newline:
            output.append(b'\n')
        sys.stdout.write((b'').join(output))
        sys.stdout.flush()
        self.last_len = len(text)
        return

    def download_progress(self, cloud_file, size, downloaded):
        self.write(b'Downloading %s, %d%% complete' % (self.current, downloaded * 100 / size))

    def upload_progress(self, cloud_file, size, uploaded):
        self.write(b'Uploading %s, %d%%' % (self.current, uploaded * 100 / size))

    def download_finish(self, cloud_file):
        self.write(b'Downloaded %s' % self.current)

    def upload_finish(self, cloud_file):
        self.write(b'Uploaded %s' % self.current)


def main():
    parsed = create_main_parser().parse_args()
    sys.exit(Commands(parsed).run())


def full_help():
    parser = create_main_parser()
    return parser.format_help()


if __name__ == b'__main__':
    main()