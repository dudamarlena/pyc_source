# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/python_essentials.py
# Compiled at: 2014-12-28 23:18:17
import os, ConfigParser, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
config_file_name_default = 'python-essentials.cfg'
config_file_pathes_default = [os.path.join(os.environ['HOME'], '.%s' % config_file_name_default), os.path.join('/etc', config_file_name_default)]

def create_config_parser(config_file_name=config_file_name_default, config_file_pathes=config_file_pathes_default):
    chosen_config_file_path = None
    for config_file_path in config_file_pathes:
        if os.path.exists(config_file_path):
            logger.info("using '%s' as configuration file" % config_file_path)
            chosen_config_file_path = config_file_path
            break

    config = ConfigParser.ConfigParser()
    if chosen_config_file_path is None:
        logger.info('no configuration file found, using default values')
    else:
        config.read(chosen_config_file_path)
    return config