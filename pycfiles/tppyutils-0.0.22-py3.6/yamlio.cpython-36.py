# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpPyUtils/yamlio.py
# Compiled at: 2020-01-16 14:56:47
# Size of source mod 2**32: 867 bytes
"""
Utility methods related to write/read YAML files
"""
from __future__ import print_function, division, absolute_import
import os, yaml, tpPyUtils

def write_to_file(data, filename):
    """
    Writes data to JSON file
    """
    if '.yml' not in filename:
        filename += '.yml'
    with open(filename, 'w') as (yaml_file):
        yaml.safe_dump(data, yaml_file)
    return filename


def read_file(filename):
    """
    Get data from JSON file
    """
    if os.stat(filename).st_size == 0:
        return
    try:
        with open(filename, 'r') as (yaml_file):
            return yaml.safe_load(yaml_file)
    except Exception as e:
        tpPyUtils.logger.warning('Could not read {0}'.format(filename))
        tpPyUtils.logger.warning(str(e))