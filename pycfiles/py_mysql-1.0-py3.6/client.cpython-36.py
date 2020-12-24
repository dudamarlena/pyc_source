# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\django\client.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 1882 bytes
import django, subprocess
if django.VERSION >= (1, 8):
    from django.db.backends.base.client import BaseDatabaseClient
else:
    from django.db.backends import BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'mysql'

    @classmethod
    def settings_to_cmd_args(cls, settings_dict):
        args = [cls.executable_name]
        db = settings_dict['OPTIONS'].get('database', settings_dict['NAME'])
        user = settings_dict['OPTIONS'].get('user', settings_dict['USER'])
        passwd = settings_dict['OPTIONS'].get('password', settings_dict['PASSWORD'])
        host = settings_dict['OPTIONS'].get('host', settings_dict['HOST'])
        port = settings_dict['OPTIONS'].get('port', settings_dict['PORT'])
        defaults_file = settings_dict['OPTIONS'].get('read_default_file')
        if defaults_file:
            args.append('--defaults-file={0}'.format(defaults_file))
        args.append('--init-command=SET @@session.SQL_MODE=TRADITIONAL')
        if user:
            args.append('--user={0}'.format(user))
        if passwd:
            args.append('--password={0}'.format(passwd))
        if host:
            if '/' in host:
                args.append('--socket={0}'.format(host))
            else:
                args.append('--host={0}'.format(host))
        if port:
            args.append('--port={0}'.format(port))
        if db:
            args.append('--database={0}'.format(db))
        return args

    def runshell(self):
        args = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
        subprocess.call(args)