# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/psphere/config.py
# Compiled at: 2013-04-04 22:22:41
import os, yaml, logging
logger = logging.getLogger(__name__)
config_path = os.path.expanduser('~/.psphere/config.yaml')
try:
    config_file = open(config_path, 'r')
    PSPHERE_CONFIG = yaml.load(config_file)
    config_file.close()
except IOError:
    logger.warning("Configuration file %s could not be opened, perhaps you haven't created one?" % config_path)
    PSPHERE_CONFIG = {'general': {}, 'logging': {}}

def _config_value(section, name, default=None):
    file_value = None
    if name in PSPHERE_CONFIG[section]:
        file_value = PSPHERE_CONFIG[section][name]
    if file_value:
        return file_value
    else:
        return default
        return