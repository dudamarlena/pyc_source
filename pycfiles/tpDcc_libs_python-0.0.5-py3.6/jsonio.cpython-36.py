# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/jsonio.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 1141 bytes
"""
Utility methods related to write/read json files
"""
from __future__ import print_function, division, absolute_import
import os, json
from tpDcc.libs import python

def write_to_file(data, filename, **kwargs):
    """
    Writes data to JSON file
    """
    if '.json' not in filename:
        filename += '.json'
    indent = kwargs.pop('indent', 2)
    try:
        with open(filename, 'w') as (json_file):
            (json.dump)(data, json_file, indent=indent, **kwargs)
    except IOError:
        python.logger.error('Data not saved to file {}'.format(filename))
        return
    else:
        python.logger.info('File correctly saved to: {}'.format(filename))
        return filename


def read_file(filename):
    """
    Get data from JSON file
    """
    if os.stat(filename).st_size == 0:
        return
    else:
        try:
            with open(filename, 'r') as (json_file):
                data = json.load(json_file)
        except Exception as err:
            python.logger.warning('Could not read {0}'.format(filename))
            raise err

        return data