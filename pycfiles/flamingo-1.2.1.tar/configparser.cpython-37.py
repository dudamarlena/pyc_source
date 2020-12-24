# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/utils/configparser.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 334 bytes
from configparser import ConfigParser

def parse_config_string(config_string):
    parser = ConfigParser()
    try:
        parser.read_string('[config]\n{}'.format(config_string))
        return {option:parser.get('config', option) for option in parser.options('config')}
    except Exception:
        return {}