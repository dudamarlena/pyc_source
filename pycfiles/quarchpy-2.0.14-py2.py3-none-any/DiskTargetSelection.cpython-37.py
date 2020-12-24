# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\DiskTargetSelection.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 946 bytes
"""
This contains useful functions to help with disk target selection

Ensure installation of wmi and pywin32

########### VERSION HISTORY ###########

13/08/2018 - Andy Norrie    - First version, based on initial work from Pedro Leao
"""
import quarchpy.disk_test.iometerDiskFinder as iometerDiskFinder

def getDiskTargetSelection(purpose='iometer'):
    driveInfo = {}
    if purpose.lower() == 'iometer':
        iometerObject = iometerDiskFinder()
        disk = iometerObject.returnDisk()
        driveInfo = disk
    return driveInfo