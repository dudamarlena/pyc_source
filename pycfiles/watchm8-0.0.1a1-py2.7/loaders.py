# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/loaders.py
# Compiled at: 2017-09-11 04:55:45


def file_loader(config_file):
    """
    Load config from YAML file

    Args:
        config_file: String path to config file

    Returns:
        Result of yaml.load

    Raises:
        KeyError: If 'jobs' key not defined in config
    """
    from yaml import load
    with open(config_file, 'r') as (fh):
        config = load(fh.read())
    if 'jobs' not in config:
        raise KeyError('No jobs defined. "jobs" key missing.')
    return config