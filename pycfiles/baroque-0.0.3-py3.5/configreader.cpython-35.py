# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/utils/configreader.py
# Compiled at: 2017-03-02 16:01:08
# Size of source mod 2**32: 1695 bytes
"""Utility functions for handling with Baroque config datastructure"""
import os, yaml
from baroque.defaults.config import DEFAULT_CONFIG
from baroque.exceptions import configuration

def read_config_or_default(path_to_file):
    """Loads configuration data from the supplied file or returns the default
    Baroque configuration.

    Args:
        path_to_file (str, optional): Path to the configuration file.

    Returns:
        dict: The configuration dictionary

    Raises:
        (:obj:`baroque.exceptions.configuration.ConfigurationNotFoundError`:
        when the supplied filepath is not a regular file
        (:obj:`baroque.exceptions.configuration.ConfigurationParseError`:
        when the supplied file cannot be parsed

    """
    if path_to_file is None:
        return DEFAULT_CONFIG
    return readconfig(path_to_file)


def readconfig(path_to_file):
    """Loads configuration data from the supplied file.

    Args:
        path_to_file (str, optional): Path to the configuration file.

    Returns:
        dict: The configuration dictionary

    Raises:
        (:obj:`baroque.exceptions.configuration.ConfigurationNotFoundError`:
        when the supplied filepath is not a regular file
        (:obj:`baroque.exceptions.configuration.ConfigurationParseError`:
        when the supplied file cannot be parsed

    """
    if not os.path.isfile(path_to_file):
        raise configuration.ConfigurationNotFoundError('Configuration file not found: {}'.format(path_to_file))
    with open(path_to_file, 'r') as (cf):
        try:
            return yaml.load(cf)
        except yaml.YAMLError:
            raise configuration.ConfigurationParseError()