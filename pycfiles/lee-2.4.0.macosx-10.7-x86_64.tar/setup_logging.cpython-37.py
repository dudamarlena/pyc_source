# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zk/anaconda3/lib/python3.7/site-packages/lee/logx/setup_logging.py
# Compiled at: 2020-01-25 05:46:09
# Size of source mod 2**32: 1100 bytes
import os, yaml, logging.config, logging, coloredlogs

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    | **@author:** Prathyush SP
    | Logging Setup
    """
    mydir = os.path.dirname(os.path.abspath(__file__))
    path = default_path
    path = os.path.join(mydir, path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    elif os.path.exists(path):
        with open(path, 'rt') as (f):
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                try:
                    print(e)
                    print('Error in Logging Configuration. Using default configs')
                    logging.basicConfig(level=default_level)
                    coloredlogs.install(level=default_level)
                finally:
                    e = None
                    del e

    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')