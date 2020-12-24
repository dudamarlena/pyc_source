# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/workstation/__init__.py
# Compiled at: 2019-09-25 05:49:08
# Size of source mod 2**32: 648 bytes
import csv, sys
from workstation.robot.robot import Robot
from workstation.robot2.robot2 import Robot2
from ._version import get_versions
version = sys.version_info[0:2]
if version < (3, 5):
    raise RuntimeError('workstation requires Python 3.5 or above, this is {0}.{1}'.format(version[0], version[1]))
robot = Robot()
robot2 = Robot2()

def reset():
    global robot
    robot = Robot()
    return robot


def reset2():
    global robot2
    robot2 = Robot2()
    return robot2


__all__ = [
 csv, robot, robot2, reset, reset2]
__version__ = get_versions()['version']
del get_versions