# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/from_si_unit.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re

def from_si_unit(arg, base_uom='MB'):
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024
    val = re.sub('[^0-9.]', '', arg)
    uom = re.sub('[0-9.]', '', arg).upper()
    base = 0
    if uom.startswith('G'):
        base = int(float(val)) * GB
    else:
        if uom.startswith('M'):
            base = int(float(val)) * MB
        else:
            if uom.startswith('K'):
                base = int(float(val)) * KB
            else:
                base = int(float(val))
            if base_uom.startswith('M'):
                return base / MB
            if base_uom.startswith('G'):
                return base / GB
        if base_uom.startswith('K'):
            return base / KB
    return base


class FilterModule(object):
    """Returns converts a string with a number and SI UOM to a number with a base of 1024, e.g. 1G == 1024"""

    def filters(self):
        return {'from_si_unit': from_si_unit}


if __name__ == '__main__':
    print from_si_unit('1.6G')
    assert from_si_unit('1.6G') == 1638
    assert from_si_unit('1G') == 1024
    assert from_si_unit('1MiB') == 1
    assert from_si_unit('1M') == 1
    assert from_si_unit('1') == 1