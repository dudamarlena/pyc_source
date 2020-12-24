# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/zensols/hostcon/config.py
# Compiled at: 2018-09-20 01:26:50
# Size of source mod 2**32: 417 bytes
import configparser
from zensols.actioncli import Config

class AppConfig(Config):

    def __init__(self, config_file=None, default_section='default', default_vars=None):
        Config.__init__(self, config_file, default_section, default_vars)

    def _create_config_parser(self):
        inter = configparser.ExtendedInterpolation()
        return configparser.ConfigParser(interpolation=inter)