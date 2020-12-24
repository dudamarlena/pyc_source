# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/console.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2575 bytes
"""Treadmill console entry point."""
import logging, logging.config, os, tempfile, traceback, click, requests, yaml, treadmill
from treadmill import cli

@click.group(cls=cli.make_multi_command('treadmill.cli'))
@click.option('--dns-domain', required=False, envvar='TREADMILL_DNS_DOMAIN', callback=cli.handle_context_opt, is_eager=True, expose_value=False)
@click.option('--ldap', required=False, envvar='TREADMILL_LDAP', type=cli.LIST, callback=cli.handle_context_opt, is_eager=True, expose_value=False)
@click.option('--ldap-search-base', required=False, envvar='TREADMILL_LDAP_SEARCH_BASE', callback=cli.handle_context_opt, is_eager=True, expose_value=False)
@click.option('--outfmt', type=click.Choice(['json', 'yaml']))
@click.option('--debug/--no-debug', help='Sets logging level to debug', is_flag=True, default=False)
@click.option('--with-proxy', required=False, is_flag=True, help='Enable proxy environment variables.', default=False)
@click.pass_context
def run(ctx, with_proxy, outfmt, debug):
    """Treadmill CLI."""
    ctx.obj = {}
    ctx.obj['logging.debug'] = False
    requests.Session().trust_env = with_proxy
    if outfmt:
        cli.OUTPUT_FORMAT = outfmt
    cli_log_conf_file = os.path.join(treadmill.TREADMILL, 'etc', 'logging', 'cli.yml')
    try:
        with open(cli_log_conf_file, 'r') as (fh):
            log_config = yaml.load(fh)
            logging.config.dictConfig(log_config)
    except IOError:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as (f):
            traceback.print_exc(file=f)
            click.echo('Unable to load log conf: %s [ %s ]' % (
             cli_log_conf_file, f.name), err=True)
        return

    if debug:
        ctx.obj['logging.debug'] = True
        logging.getLogger('treadmill').setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)