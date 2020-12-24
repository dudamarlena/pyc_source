# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/simo/Projects/pygmount/pygmount/utils/utils.py
# Compiled at: 2014-04-03 08:12:27
from __future__ import unicode_literals, absolute_import
import os, platform
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

def get_sudo_username():
    """
    Check 'SUDO_USER' var if in environment and return a tuple with True and value of 'SUDO_USER' if
    the var in environment or a tuple with False and 'USER' value.

    Return tuple.
    """
    if b'SUDO_USER' in os.environ:
        return (True, os.environ[b'SUDO_USER'])
    return (False, os.environ[b'USER'])


def get_home_dir():
    """
    Return path of user's home directory.

    Return string.
    """
    system = platform.system().lower()
    if system == b'linux':
        return b'/home/'
    if system == b'darwin':
        return b'/Users/'
    if system == b'windows':
        return b'C:/Documents...'
    raise Exception(b'Impossibile individuare il tipo di sistema')


def read_config(file=None):
    """
    Read a config file into .ini format and return dict of shares.

    Keyword arguments:
    file -- the path of config file (default None)

    Return dict.
    """
    if not os.path.exists(file):
        raise IOError(b'Impossibile trovare il file %s' % file)
    shares = []
    config = ConfigParser()
    config.read(file)
    for share_items in [ config.items(share_title) for share_title in config.sections()
                       ]:
        dict_share = {}
        for key, value in share_items:
            if key == b'hostname' and b'@' in value:
                hostname, credentials = (item[::-1] for item in value[::-1].split(b'@', 1))
                dict_share.update({key: hostname})
                credentials = tuple(cred.lstrip(b'"').rstrip(b'"') for cred in credentials.split(b':', 1))
                dict_share.update({b'username': credentials[0]})
                if len(credentials) > 1:
                    dict_share.update({b'password': credentials[1]})
                continue
            dict_share.update({key: value})

        shares.append(dict_share)

    return shares