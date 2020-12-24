# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aiows.py
# Compiled at: 2018-10-09 14:57:54
# Size of source mod 2**32: 3243 bytes
import uuid, logging, argparse
from aiohttp import web
logging.basicConfig(level=(logging.INFO),
  format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
log = logging.getLogger('aiows.main')

def set_session(app):
    """
    Sets unique session ID
    :param app:
    :return:
    """
    app['ssid'] = 's{}'.format(str(uuid.uuid4())[:8])
    log.info('Started new session: {}'.format(app['ssid']))


def set_push_password(app, pwd):
    """
    Sets push notifications action password
    :param app:
    :return:
    """
    app['pwd'] = pwd
    log.info('Publisher password: "{}"'.format(pwd or 'not set'))


def load_settings(app, args):
    """
    Define application settings
    :param app:
    :param args:
    :return:
    """
    app['args'] = args


def load_urls(app):
    """
    Load applications routes
    :param app:
    :return:
    """
    prefix = app['args'].url_prefix or None
    if prefix is None:
        prefix = '/'
    if not prefix.startswith('/'):
        prefix = '/{}'.format(prefix)
    if not prefix.endswith('/'):
        prefix = '{}/'.format(prefix)
    from aiows.aioapp.urls import patterns
    for method, pattern in patterns:
        pattern[0] = prefix + pattern[0]
        (getattr(app.router, 'add_{method}'.format(method=method)))(*pattern)


def load_tasks(app):
    """
    Register applications background tasks
    :param app:
    :return:
    """
    from aiows.aioapp.background import tasks

    async def bg_start(root):
        for identify, callback in tasks:
            if isinstance(callback, str):
                callback = getattr(tasks, callback)
            root[identify] = root.loop.create_task(callback(root))

    async def bg_stop(root):
        for identify, callback in tasks:
            root[identify].cancel()
            await root[identify]

    app.on_startup.append(bg_start)
    app.on_cleanup.append(bg_stop)


def main():
    parser = argparse.ArgumentParser(description='AIOHttp WebSocket server')
    parser.add_argument('--pwd', type=str, default=None, help='Password to be able to publish messages.')
    parser.add_argument('--usock', type=str, default=None, help='UNIX Socket file for aiows server')
    parser.add_argument('--host', type=str, default=None, help='Server host')
    parser.add_argument('--port', type=int, default=None, help='Server port')
    parser.add_argument('--reuse-addr', type=int, default=1, help='Reuse host')
    parser.add_argument('--reuse-port', type=int, default=1, help='Reuse port')
    parser.add_argument('--url-prefix', type=str, default='', help='API Endpoints prefix')
    args = parser.parse_args()
    app = web.Application()
    load_settings(app, args)
    set_session(app)
    load_urls(app)
    load_tasks(app)
    set_push_password(app, args.pwd)
    web.run_app(app=app,
      path=(args.usock),
      host=(args.host),
      port=(args.port),
      reuse_address=(args.reuse_addr),
      reuse_port=(args.reuse_port))