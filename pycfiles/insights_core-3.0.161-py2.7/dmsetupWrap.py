# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/dmsetupWrap.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import print_function
from __future__ import absolute_import
from . import util
import string

def getMajorMinor(deviceName, dmsetupLs):
    """
    Given output of dmsetup ls this will return
    themajor:minor (block name) of the device deviceName
    """
    startingIndex = string.rindex(dmsetupLs, deviceName) + len(deviceName)
    endingIndex = string.index(dmsetupLs[startingIndex:], '\n') + startingIndex
    newStr = dmsetupLs[startingIndex + 2:endingIndex - 1]
    return newStr


def getDmsetupLs():
    cmd = [
     'dmsetup', 'ls']
    r = util.subp(cmd)
    if r.return_code != 0:
        print(r.stderr)
        return -1
    return r.stdout