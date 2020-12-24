# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Bureau\educat_irsensor\irsensors\irsensors\__init__.py
# Compiled at: 2019-09-23 22:16:18
# Size of source mod 2**32: 717 bytes
"""This package allows to read data from an IR sensor set connected by micro USB / USB.

This package expect the IR sensor set to send string encode line data as follow:
"ID,Error_Code,Distance,.........,
". What is between the third and the fourth comma does not matter.

This package uses the serial package. You can install it with "pip install serial" command.

In this version, the sensor ID can not be more than 9 (if it is more than 9, it will cause a bug).

"""
__version__ = '0.0.8'
from irsensors.irsensorset import IRSensorSet
if __name__ == '__main__':
    try:
        try:
            pass
        except KeyboardInterrupt:
            pass

    finally:
        pass