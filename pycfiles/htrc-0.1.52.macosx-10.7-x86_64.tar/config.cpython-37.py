# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/config.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 4744 bytes
"""
`htrc.volumes`

Contains the configuration parser object.
"""
from future import standard_library
standard_library.install_aliases()
from builtins import input
from configparser import RawConfigParser as ConfigParser, NoSectionError
from codecs import open
from getpass import getpass
import logging, os.path, shutil, time
from htrc.lib.cli import bool_prompt
DEFAULT_PATH = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(DEFAULT_PATH, '.htrc')
if not os.path.exists(DEFAULT_PATH):
    DEFAULT_FILE = os.path.dirname(__file__)
    DEFAULT_FILE = os.path.join(DEFAULT_FILE, '.htrc.default')
    logging.info('Copying default config file to home directory.')
    shutil.copyfile(DEFAULT_FILE, DEFAULT_PATH)

def _get_value(section, key, path=None):
    if path is None:
        path = DEFAULT_PATH
    config = ConfigParser(allow_no_value=True)
    with open(path, encoding='utf8') as (configfile):
        config.readfp(configfile)
    try:
        return config.get(section, key)
    except NoSectionError:
        raise EnvironmentError('Config not set for {} {} in {}'.format(section, key, path))


def get_dataapi_port(path=None):
    port = int(_get_value('data', 'port', path))
    return port


def get_dataapi_host(path=None):
    host = _get_value('data', 'host', path)
    return host


def get_dataapi_epr(path=None):
    return _get_value('data', 'url', path)


def get_dataapi_cert(path=None):
    return _get_value('data', 'cert', path)


def get_dataapi_key(path=None):
    return _get_value('data', 'key', path)


def get_idp_host_port(path=None):
    host = _get_value('idp', 'host', path)
    port = _get_value('idp', 'port', path)
    return (
     host, port)


def get_idp_path(path=None):
    return _get_value('idp', 'url')


def get_idp_url(path=None):
    host, port = get_idp_host_port(path)
    path = get_idp_path(path)
    if port == 443:
        return 'https://{}{}'.format(host, path)
    return 'https://{}:{}{}'.format(host, port, path)


def get_jwt_token(path=None):
    try:
        token = _get_value('jwt', 'token', path)
        expiration = int(_get_value('jwt', 'expiration', path))
        if time.time() > expiration:
            raise RuntimeError('JWT token expired.')
    except:
        import htrc.auth
        token, expiration = htrc.auth.get_jwt_token()
        htrc.config.save_jwt_token(token, expiration, path)

    return token


def save_jwt_token(token, expiration=None, path=None):
    """
    Saves JWT token in the config file.
    """
    if path is None:
        path = DEFAULT_PATH
    else:
        if expiration is None:
            expiration = time.time()
        config = ConfigParser(allow_no_value=True)
        if os.path.exists(path):
            config.read(path)
        config.has_section('jwt') or config.add_section('jwt')
    config.set('jwt', 'token', token)
    config.set('jwt', 'expiration', expiration)
    with open(path, 'w') as (credential_file):
        config.write(credential_file)
    return token


def remove_jwt_token(path=None):
    """
    Removes JWT token from the config file.
    """
    if path is None:
        path = DEFAULT_PATH
    else:
        config = ConfigParser(allow_no_value=True)
        if os.path.exists(path):
            config.read(path)
        config.has_section('jwt') or config.add_section('jwt')
    config.set('jwt', 'token', ' ')
    config.set('jwt', 'expiration', ' ')
    with open(path, 'w') as (credential_file):
        config.write(credential_file)


def get_credentials(path=None):
    """
    Retrieves the username and password from a config file for the Data API.
    Raises an EnvironmentError if not specified.
    See also: credential_prompt
    """
    client_id = _get_value('idp', 'client_id', path)
    client_secret = _get_value('idp', 'client_secret', path)
    if not client_id:
        if not client_secret:
            logging.error('Config path: {}'.format(path))
            raise EnvironmentError('No client_id and client_secret stored in config file.')
    return (
     client_id, client_secret)


def populate_parser(parser):
    return parser


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser = populate_parser(parser)
    parser.parse_args()