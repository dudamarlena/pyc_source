# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/runner/commands/devserver.py
# Compiled at: 2019-09-04 11:06:16
from __future__ import absolute_import, print_function
import click, six
from six.moves.urllib.parse import urlparse
from sentry.runner.decorators import configuration, log_options

@click.command()
@click.option('--reload/--no-reload', default=True, help='Autoreloading of python files.')
@click.option('--watchers/--no-watchers', default=True, help='Watch static files and recompile on changes.')
@click.option('--workers/--no-workers', default=False, help='Run asynchronous workers.')
@click.option('--prefix/--no-prefix', default=True, help='Show the service name prefix and timestamp')
@click.option('--styleguide/--no-styleguide', default=False, help='Start local styleguide web server on port 9001')
@click.option('--environment', default='development', help='The environment name.')
@click.option('--experimental-spa/--no-experimental-spa', default=False, help='This enables running sentry with pure separation of the frontend and backend')
@click.argument('bind', default='127.0.0.1:8000', metavar='ADDRESS', envvar='SENTRY_DEVSERVER_BIND')
@log_options()
@configuration
def devserver(reload, watchers, workers, experimental_spa, styleguide, prefix, environment, bind):
    """Starts a lightweight web server for development."""
    if ':' in bind:
        host, port = bind.split(':', 1)
        port = int(port)
    else:
        host = bind
        port = None
    import os
    os.environ['SENTRY_ENVIRONMENT'] = environment
    from django.conf import settings
    from sentry import options
    from sentry.services.http import SentryHTTPServer
    url_prefix = options.get('system.url-prefix', '')
    parsed_url = urlparse(url_prefix)
    needs_https = parsed_url.scheme == 'https' and (parsed_url.port or 443) > 1024
    has_https = False
    if needs_https:
        from subprocess import check_output
        try:
            check_output(['which', 'https'])
            has_https = True
        except Exception:
            has_https = False
            from sentry.runner.initializer import show_big_error
            show_big_error([
             'missing `https` on your `$PATH`, but https is needed',
             '`$ brew install mattrobenolt/stuff/https`'])

    uwsgi_overrides = {'http-keepalive': True, 
       'worker-reload-mercy': 2, 
       'honour-stdin': True, 
       'limit-post': 1073741824, 
       'http-chunked-input': True, 
       'thunder-lock': False, 
       'timeout': 600, 
       'harakiri': 600}
    if reload:
        uwsgi_overrides['py-autoreload'] = 1
    daemons = []
    if experimental_spa:
        os.environ['SENTRY_EXPERIMENTAL_SPA'] = '1'
        if not watchers:
            click.secho('Using experimental SPA mode without watchers enabled has no effect', err=True, fg='yellow')
    if watchers:
        daemons += settings.SENTRY_WATCHERS
        proxy_port = port
        port = port + 1
        uwsgi_overrides['protocol'] = 'http'
        os.environ['SENTRY_WEBPACK_PROXY_PORT'] = '%s' % proxy_port
        os.environ['SENTRY_BACKEND_PORT'] = '%s' % port
        webpack_config = next(w for w in daemons if w[0] == 'webpack')[1]
        webpack_config[0] = os.path.join(*(os.path.split(webpack_config[0])[0:-1] + ('webpack-dev-server', )))
        daemons = [ w for w in daemons if w[0] != 'webpack' ] + [('webpack', webpack_config)]
    else:
        uwsgi_overrides.update({'http': '%s:%s' % (host, port), 
           'protocol': 'uwsgi', 
           'uwsgi-socket': None})
    if workers:
        if settings.CELERY_ALWAYS_EAGER:
            raise click.ClickException('Disable CELERY_ALWAYS_EAGER in your settings file to spawn workers.')
        daemons += [
         (
          'worker', ['sentry', 'run', 'worker', '-c', '1', '--autoreload']),
         (
          'cron', ['sentry', 'run', 'cron', '--autoreload'])]
        from sentry import eventstream
        if eventstream.requires_post_process_forwarder():
            daemons += [
             (
              'relay',
              [
               'sentry',
               'run',
               'post-process-forwarder',
               '--loglevel=debug',
               '--commit-batch-size=1'])]
    if needs_https and has_https:
        https_port = six.text_type(parsed_url.port)
        https_host = parsed_url.hostname
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, 0))
        port = s.getsockname()[1]
        s.close()
        bind = '%s:%d' % (host, port)
        daemons += [
         (
          'https', ['https', '-host', https_host, '-listen', host + ':' + https_port, bind])]
    if daemons:
        uwsgi_overrides['log-format'] = '"%(method) %(uri) %(proto)" %(status) %(size)'
    else:
        uwsgi_overrides['log-format'] = '[%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size)'
    server = SentryHTTPServer(host=host, port=port, workers=1, extra_options=uwsgi_overrides)
    if not daemons:
        return server.run()
    else:
        import sys
        from subprocess import list2cmdline
        from honcho.manager import Manager
        from honcho.printer import Printer
        os.environ['PYTHONUNBUFFERED'] = 'true'
        server.prepare_environment()
        daemons += [('server', ['sentry', 'run', 'web'])]
        if styleguide:
            daemons += [('storybook', ['./bin/yarn', 'storybook'])]
        cwd = os.path.realpath(os.path.join(settings.PROJECT_ROOT, os.pardir, os.pardir))
        manager = Manager(Printer(prefix=prefix))
        for name, cmd in daemons:
            manager.add_process(name, list2cmdline(cmd), quiet=False, cwd=cwd)

        manager.loop()
        sys.exit(manager.returncode)
        return