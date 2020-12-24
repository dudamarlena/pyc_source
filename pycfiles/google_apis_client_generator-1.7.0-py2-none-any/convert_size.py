# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/convert_size.py
# Compiled at: 2019-01-24 16:56:47
"""Convert human readable sizes to numbers.

Convert a string like 10G/K/M/B to a number.
"""

def ConvertSize(size):
    if not size:
        return
    else:
        units = [
         (
          'GB', 1073741824),
         (
          'MB', 1048576),
         (
          'KB', 1024),
         ('B', 1)]
        size = size.upper()
        for suffix, multiplier in units:
            if size.endswith(suffix):
                num_units = size[:-len(suffix)]
                try:
                    return int(num_units) * multiplier
                except (ValueError, KeyError):
                    break

        return