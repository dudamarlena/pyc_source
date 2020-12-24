# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/configuration.py
# Compiled at: 2019-03-28 16:44:56
# Size of source mod 2**32: 447 bytes
import yaml

def configuration_from_yaml(filename):
    """Loads a YAML configuration file.

    :param filename: The filename of the file to load.
    :returns: dict -- A dictionary representing the YAML configuration file
        loaded. If the file can't be loaded, then the empty dict is returned.
    """
    try:
        with open(filename) as (infile):
            return yaml.safe_load(infile.read())
    except IOError:
        return {}