# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\MobileHR\MobileHR.Mario.Engine\MobileHR.Mario.Engine\modules\logging\logging.py
# Compiled at: 2018-12-11 08:53:27
# Size of source mod 2**32: 894 bytes
import os, yaml, logging.config, logging, coloredlogs

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG', log_dir=''):
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as (f):
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)

    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')