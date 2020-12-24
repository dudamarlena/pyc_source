# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/commands/lxrefresh.py
# Compiled at: 2011-04-20 13:40:15
import sys, os.path, optparse, logging
from linkexchange.config import file_config, ConfigError

def main():
    op = optparse.OptionParser(usage='%prog -c linkexchange.cfg [other options] [name=value...]', description='Refresh links database using configuration from linkexchange.cfg. Interpolation variables can be specified in arguments using name=value format.')
    op.add_option('-c', '--config', dest='config', default=None, help='specify path to LinkExchange configuration file', metavar='FILE')
    op.add_option('-r', '--request-url', dest='request_url', default=None, help='request URL or domain', metavar='URL')
    op.add_option('-q', '--quiet', dest='quiet', action='store_true', default=False, help='suppress all normal output')
    op.add_option('--debug', dest='debug', action='store_true', default=False, help='print debug output')
    opts, args = op.parse_args()
    op.print_usage = lambda file=None: None
    if not opts.config:
        op.error('you must specify configuration file with -c or --config option!')
    interpolation = dict(basedir=os.path.abspath(os.path.dirname(opts.config)))
    for arg in args:
        try:
            k, v = arg.split('=', 1)
        except ValueError:
            op.error('%s is not seems like name=value')

        interpolation[k] = v

    log = logging.getLogger()
    log_hdl = logging.StreamHandler(sys.stderr)
    log.addHandler(log_hdl)
    if opts.debug:
        log.setLevel(logging.DEBUG)
    else:
        if opts.quiet:
            log.setLevel(logging.CRITICAL)
        else:
            log.setLevel(logging.WARNING)
        vars = {}
        try:
            file_config(vars, opts.config, defaults=interpolation)
        except ConfigError as e:
            op.error(str(e))

    request_url = opts.request_url
    if request_url is None:
        request_url = vars['options'].get('host', None)
    if not request_url:
        op.error('host undefined! you need to set the host option in the linkexchange.cfg or pass -r option at the comment line.')
    if '://' not in request_url:
        request_url = 'http://' + request_url
    vars['platform'].refresh_db(request_url)
    return 0


if __name__ == '__main__':
    sys.exit(main())