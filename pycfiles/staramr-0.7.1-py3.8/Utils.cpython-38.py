# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/Utils.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 536 bytes
from typing import Dict

def get_string_with_spacing(data: Dict[(str, str)]) -> str:
    """
    Gets a string representation of a list of key/value pairs (as OrderedDictionary) with proper spacing between key/values.
    :param data: A Dictionary containing key/value pairs.
    :return: A string representation of the Dictionary.
    """
    max_width = max([len(k) for k in data])
    return '\n'.join(('{} = {}'.format(k.ljust(max_width), v) for k, v in data.items())) + '\n'