# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rtownley/Projects/stonehenge/stonehenge/file_validators.py
# Compiled at: 2018-08-31 13:32:27
# Size of source mod 2**32: 1149 bytes
import importlib, os

def validate_config(config_file_location):
    """Confirms that the config file exists and is properly filled in

    If the file exists and is valid, returns a dictionary containing desired
    project parameters. If not, an error is thrown.
    """
    if os.path.isfile(config_file_location):
        spec = importlib.util.spec_from_file_location('stonehenge.project_config_from_file', config_file_location)
        stonehenge_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stonehenge_config)
        CONFIG = stonehenge_config.PROJECT_CONFIGURATION
    else:
        raise Exception('Config file not found at {0}'.format(config_file_location))
    if not CONFIG['PROJECT_NAME']:
        raise AssertionError
    else:
        assert CONFIG['GITHUB_REPOSITORY']
        assert 'git@' in CONFIG['GITHUB_REPOSITORY']
    db = CONFIG['ENVIRONMENTS']['LOCAL']['DATABASE']
    for key in db.keys():
        if not db[key]:
            raise Exception('Required database field {0} not specified'.format(key))

    return CONFIG