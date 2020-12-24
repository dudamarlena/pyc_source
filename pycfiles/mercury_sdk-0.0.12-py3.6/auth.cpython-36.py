# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/auth/auth.py
# Compiled at: 2019-03-28 16:45:27
# Size of source mod 2**32: 2289 bytes
import logging, importlib, os, yaml
from datetime import datetime, timezone
import dateutil.parser
LOG = logging.getLogger(__name__)
__auth_handler = None

def write_token(token_data, path):
    with open(path, 'w') as (token_file):
        yaml.safe_dump(token_data, stream=token_file)


def read_token(path):
    with open(path) as (fp):
        return yaml.safe_load(fp)


def get_auth_handler(handler_name):
    global __auth_handler
    if not __auth_handler:
        __auth_handler = importlib.import_module(('.mcli.auth.{}'.format(handler_name)),
          package='mercury_sdk')
    return __auth_handler


def update_parser(handler_name, parser):
    _h = get_auth_handler(handler_name)
    if hasattr(_h, 'add_arguments'):
        _h.add_arguments(parser)


def get_token(configuration, token_path):
    if os.path.exists(token_path):
        LOG.debug('Token exists, checking...')
        token_data = read_token(token_path)
        if datetime.now(timezone.utc) < dateutil.parser.parse(token_data['expires_at']):
            return token_data
        LOG.info('Token expired at: {}'.format(token_data['expires_at']))
        os.remove(token_path)
    LOG.info('Auth handler: {}'.format(configuration['auth_handler']))
    auth_handler = get_auth_handler(configuration['auth_handler'])
    token_data = auth_handler.authenticate(configuration)
    if not configuration.get('no_store'):
        LOG.debug('Writing token file: {}'.format(token_path))
        write_token(token_data, token_path)
    return token_data


def invalidate_token(configuration, token_path):
    if os.path.exists(token_path):
        token_data = read_token(token_path)
        auth_handler = get_auth_handler(configuration['auth_handler'])
        auth_handler.invalidate(configuration, token_data)
        os.remove(token_path)