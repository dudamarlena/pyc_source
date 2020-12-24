# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/szczepan/.virtualenvs/pyh/lib/python2.7/site-packages/pyhistory/file_config.py
# Compiled at: 2017-09-29 03:29:06
from pathlib import Path
from six.moves.configparser import ConfigParser, NoSectionError, NoOptionError
from .utilities import find_file_across_parents
FILE_TO_CHECK = 'setup.cfg'
CONFIG_SECTION = 'pyhistory'

def get_defaults_from_config_file_if_exists(file_to_check=FILE_TO_CHECK):
    try:
        config_file = find_file_across_parents(Path.cwd(), file_to_check)
    except RuntimeError:
        return {}

    return _get_config_from_file(config_file)


def _get_config_from_file(config_file):
    parser = ConfigParser()
    parser.read(str(config_file))
    return _ConfigGetter(parser, CONFIG_SECTION)


class _ConfigGetter(object):

    def __init__(self, parser, section):
        self.parser = parser
        self.section = section

    def get(self, key, default=None):
        try:
            return self.parser.get(self.section, key)
        except (NoSectionError, NoOptionError):
            return default