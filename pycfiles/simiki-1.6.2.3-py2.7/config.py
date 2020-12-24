# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/config.py
# Compiled at: 2019-04-21 06:05:20
from __future__ import absolute_import, unicode_literals
import os, os.path, sys, io, logging, datetime
from pprint import pprint
import yaml, tzlocal

class ConfigFileNotFound(Exception):
    pass


def _set_default_config():
    config = {b'url': b'', 
       b'title': b'', 
       b'keywords': b'', 
       b'description': b'', 
       b'author': b'', 
       b'root': b'/', 
       b'source': b'content', 
       b'destination': b'output', 
       b'attach': b'attach', 
       b'themes_dir': b'themes', 
       b'theme': b'simple2', 
       b'default_ext': b'md', 
       b'pygments': True, 
       b'debug': False, 
       b'time': datetime.datetime.now(tzlocal.get_localzone())}
    return config


def _post_process(config):
    for k, v in config.items():
        if v is None:
            config[k] = b''

    if config[b'url'].endswith(b'/'):
        config[b'url'] = config[b'url'][:-1]
    return config


def get_default_config():
    return _post_process(_set_default_config())


def parse_config(config_file):
    if not os.path.exists(config_file):
        raise ConfigFileNotFound((b'{0} not exists').format(config_file))
    default_config = _set_default_config()
    with io.open(config_file, b'rt', encoding=b'utf-8') as (fd):
        config = yaml.load(fd, Loader=yaml.FullLoader)
    default_config.update(config)
    config = _post_process(default_config)
    return config


if __name__ == b'__main__':
    if len(sys.argv) == 1:
        base_dir = os.path.dirname(__file__)
        _config_file = os.path.join(base_dir, b'conf_templates', b'_config.yml.in')
    elif len(sys.argv) == 2:
        base_dir = os.getcwd()
        _config_file = os.path.join(base_dir, sys.argv[1])
    else:
        logging.error(b"Use the template config file by default, you can specify the config file to parse. \nUsage: `python -m simiki.config [_config.yml]'")
        sys.exit(1)
    pprint(parse_config(_config_file))