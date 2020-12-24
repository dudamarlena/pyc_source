# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmonitor/constant.py
# Compiled at: 2019-10-12 06:44:13
# Size of source mod 2**32: 1635 bytes
import os
from configparser import ConfigParser
from enum import Enum, unique

@unique
class BuildType(Enum):
    BETA = 'wmonitor_beta.cfg'
    DEV = 'wmonitor_dev.cfg'
    PROD = 'wmonitor_prod.cfg'
    DEFAULT = 'wmonitor.cfg'


class Config:
    config_dir = None
    build_type = None
    config_parser = None
    domain = None
    app_code = None
    log_dir = None
    logging_level = None

    @staticmethod
    def init():
        Config.build_type = os.environ.get('BUILD_TYPE', 'DEFAULT')
        Config.config_dir = os.environ.get('CONFIG_DIR', './')
        Config.log_dir = os.environ.get('LOG_DIR', './')
        Config.logging_level = int(os.environ.get('LOGGING_LEVEL', 20))
        print('build_type:%s config_dir:%s log_dir:%s' % (Config.build_type, Config.config_dir, Config.log_dir))
        if Config.build_type in BuildType.__members__:
            filename = BuildType.__getattr__(Config.build_type)
            path = os.path.join(Config.config_dir, filename.value)
            print('加载配置文件。path:%s' % path)
            Config.config_parser = ConfigParser()
            Config.config_parser.read(path)
        else:
            raise ValueError('构建类型错误 build_type:%s' % Config.build_type)
        Config._Config__set_domain()
        Config._Config__set_app_code()

    @staticmethod
    def __set_domain():
        Config.domain = Config.config_parser.get('web', 'domain')
        print('domain:%s' % Config.domain)

    @staticmethod
    def __set_app_code():
        Config.app_code = Config.config_parser.get('app', 'app_code')
        print('app_code:%s' % Config.app_code)


Config.init()