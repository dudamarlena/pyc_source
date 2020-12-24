# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/auth.py
# Compiled at: 2020-03-19 11:59:34
# Size of source mod 2**32: 1729 bytes
"""Auth commands."""
import os
from getpass import getpass
from appdirs import user_data_dir
import pkg_resources
from . import http

def login(log, session, args):
    """Authenticate and retrieve a long lived token."""
    user_path = _init_conf_location()
    user_data = os.path.join(user_path, '.auth')
    username = input('Username: ')
    password = getpass()
    data = {'username':username, 
     'password':password, 
     'noexpire':True}
    url = '{}/oauth/token/'.format(args.url)
    log.debug('POST: {}'.format(url))
    response = http.post_json(session, url, data)
    with open(user_data, 'w') as (auth):
        auth.write(response['token'])
    log('User token saved to {}.'.format(user_data))


def get_token(args=None):
    """
    Get the users auth token.

    If specified in the args then will use that over local config
    """
    token = args.token if 'token' in args else None
    if token is None:
        user_data = os.path.join(_get_user_dir(), '.auth')
        if os.path.exists(user_data):
            with open(user_data) as (auth):
                token = auth.read()
    return token


def _get_user_dir():
    """Get the users data directory location."""
    app_name = pkg_resources.require('zegami-cli')[0].project_name
    return user_data_dir(app_name, 'zegami')


def _init_conf_location():
    """Initialise the config file location."""
    user_data = _get_user_dir()
    if not os.path.exists(user_data):
        os.makedirs(user_data)
    return user_data