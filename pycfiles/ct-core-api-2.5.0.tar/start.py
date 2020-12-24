# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/start.py
# Compiled at: 2019-08-05 00:35:42
__doc__ = '\n### Usage: ctstart [--web_backend=BACKEND] [--port=PORT] [--datastore=DS_PATH]\n\n### Options:\n    -h, --help            show this help message and exit\n    -w WEB_BACKEND, --web_backend=WEB_BACKEND\n                          web backend. options: dez, gae. (default: dez)\n    -p PORT, --port=PORT  select your port (default=8080)\n    -a ADMIN_PORT, --admin_port=ADMIN_PORT\n                          select your port (default=8002)\n    -d DATASTORE, --datastore=DATASTORE\n                          select your datastore file (default=sqlite:///data.db)\n    -o, --overwrite_password\n                          overwrite admin password (default=False)\n'
from optparse import OptionParser
from cantools import config
from cantools.util import error

def go():
    parser = OptionParser('ctstart [--web_backend=BACKEND] [--port=PORT] [--datastore=DS_PATH]')
    parser.add_option('-w', '--web_backend', dest='web_backend', default=config.web.server, help='web backend. options: dez, gae. (default: %s)' % (config.web.server,))
    parser.add_option('-p', '--port', dest='port', default=config.web.port, help='select your port (default=%s)' % (config.web.port,))
    parser.add_option('-a', '--admin_port', dest='admin_port', default=config.admin.port, help='select your port (default=%s)' % (config.admin.port,))
    parser.add_option('-d', '--datastore', dest='datastore', default=config.db.main, help='select your datastore file (default=%s)' % (config.db.main,))
    parser.add_option('-o', '--overwrite_password', action='store_true', dest='overwrite_password', default=False, help='overwrite admin password (default=False)')
    options, args = parser.parse_args()
    config.web.update('port', int(options.port))
    config.admin.update('port', int(options.admin_port))
    if options.overwrite_password:
        config.update('newpass', True)
    if options.web_backend == 'gae':
        import subprocess
        cmd = 'dev_appserver.py . --host=%s --port=%s --admin_port=%s --datastore_path=%s' % (config.web.host,
         options.port, options.admin_port, options.datastore)
        print cmd
        subprocess.call(cmd, shell=True)
    elif options.web_backend == 'dez':
        from cantools.web import run_dez_webserver
        run_dez_webserver()
    else:
        error('invalid web_backend: %s' % (options.web_backend,))


if __name__ == '__main__':
    go()