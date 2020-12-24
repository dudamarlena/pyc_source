# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/utils.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1312 bytes
import logging, yaml
logger = logging.getLogger(__name__)

def not_in_dict_or_none(dict, key):
    """
    Check if a key exists in a map and if it's not None
    :param dict: map to look for key
    :param key: key to find
    :return: true if key is in dict and not None
    """
    if key not in dict or dict[key] is None:
        return True
    return False


def format_client_message(session=None, address=None, port=None):
    if session:
        return '(client id=%s)' % session.client_id
    if address is not None:
        if port is not None:
            return '(client @=%s:%d)' % (address, port)
    return '(unknown client)'


def gen_client_id():
    """
    Generates random client ID
    :return:
    """
    import random
    gen_id = 'hbmqtt/'
    for i in range(7, 23):
        gen_id += chr(random.randint(0, 74) + 48)
    else:
        return gen_id


def read_yaml_config(config_file):
    config = None
    try:
        with open(config_file, 'r') as (stream):
            config = yaml.full_load(stream) if hasattr(yaml, 'full_load') else yaml.load(stream)
    except yaml.YAMLError as exc:
        try:
            logger.error('Invalid config_file %s: %s' % (config_file, exc))
        finally:
            exc = None
            del exc

    else:
        return config