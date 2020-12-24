# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/start.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import sys, click
from sentry.runner.decorators import configuration
SERVICES = {'http': 'sentry.services.http.SentryHTTPServer', 
   'smtp': 'sentry.services.smtp.SentrySMTPServer'}

@click.command()
@click.option('--bind', '-b', default=None, help='Bind address.', metavar='ADDRESS')
@click.option('--workers', '-w', default=0, help='The number of worker processes for handling requests.')
@click.option('--upgrade', default=False, is_flag=True, help='Upgrade before starting.')
@click.option('--noinput', default=False, is_flag=True, help='Do not prompt the user for input of any kind.')
@click.argument('service', default='http', type=click.Choice(sorted(SERVICES.keys())))
@configuration
@click.pass_context
def start(ctx, service, bind, workers, upgrade, noinput):
    """DEPRECATED see `sentry run` instead."""
    from sentry.runner.initializer import show_big_error
    show_big_error([
     '`sentry start%s` is deprecated.' % (' ' + service if 'http' in sys.argv else ''),
     'Use `sentry run %s` instead.' % {'http': 'web'}.get(service, service)])
    if bind:
        if ':' in bind:
            host, port = bind.split(':', 1)
            port = int(port)
        else:
            host = bind
            port = None
    else:
        host, port = (None, None)
    if upgrade:
        click.echo('Performing upgrade before service startup...')
        from sentry.runner import call_command
        call_command('sentry.runner.commands.upgrade.upgrade', verbosity=0, noinput=noinput)
    click.echo('Running service: %r' % service)
    sys.argv = sys.argv[:1]
    from sentry.utils.imports import import_string
    import_string(SERVICES[service])(host=host, port=port, workers=workers).run()
    return