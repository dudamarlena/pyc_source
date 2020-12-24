# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/webstarts/__init__.py
# Compiled at: 2017-07-13 17:49:19
# Size of source mod 2**32: 1957 bytes
"""Applicable to webstarts"""
import json, os
from decorator import decorator
__author__ = 'john'

def get_conf(env):
    """Right now just checks if it is debug mode"""
    conf = json.loads(env.get('WSCONF', '{}'))
    debug = True if env.get('WSDEV') == '1' else False
    conf.update(debug=debug)
    return conf


def configure(env=os.environ):
    from . import wlog, backend
    conf = get_conf(env)
    wlog.setup(conf)
    backend.setup_celery(conf)
    return conf


def entry():
    """Run eventlet

  - structlog
    Check out colorama
    Like queries always do log = log.new(y=23)
    logging.getLogger('foo').addHandler(logging.NullHandler()) should be used by libraries
  - GoogleCloud logging - when the shit gets fixed
    I could add the handler to logging.getLogger('socialclime') since it will be the parent of all app loggers.
    Now that i finally understand logging.

  """
    from gevent import monkey
    monkey.patch_all(subprocess=True)
    conf = configure()
    from .gunicorn import WebstartsApp
    app = WebstartsApp('%(prog)s [OPTIONS] [APP_MODULE]', conf['debug'])
    return app.run()


@decorator
def trace(f, *args, **kwargs):
    import colorama, inspect
    reset = colorama.Style.RESET_ALL
    brblack = colorama.Fore.BLACK + colorama.Style.BRIGHT
    red = colorama.Fore.LIGHTRED_EX + colorama.Style.BRIGHT
    from . import log_id
    name = [i for i in inspect.getmembers(f, lambda mem: isinstance(mem, str)) if i[0] == '__qualname__'][0][1]
    before = log_id.find()
    ret = f(*args, **kwargs)
    after = log_id.find()
    return ret