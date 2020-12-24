# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\convertHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 1631 bytes


def convertStorageUnit(num, srcUnit, desUnit):
    """Convert unit
    - num: value
    - srcUnit: gb/mb/kb/byte
    - desUnit: gb/mb/kb/byte
    """
    try:
        units = [
         'gb', 'mb', 'kb', 'byte']
        if srcUnit not in units or desUnit not in units:
            return
        if srcUnit == desUnit:
            return num
        num = float(num)
        if num == 0:
            return 0
        srcIndex = units.index(srcUnit)
        desIndex = units.index(desUnit)
        tmp = desIndex - srcIndex
        while tmp != 0:
            if srcIndex < desIndex:
                num = num * 1024
            else:
                num = num / 1024
            if tmp > 0:
                tmp = tmp - 1
            else:
                tmp = tmp + 1

        return num
    except:
        return


def convertStorageUnitToString(num, srcUnit):
    """Convert unit to string
    - num: value
    - srcUnit: gb/mb/kb/byte
    """
    try:
        units = [
         'gb', 'mb', 'kb', 'byte']
        if srcUnit not in units:
            return '0 KB'
        num = float(num)
        srcIndex = units.index(srcUnit)
        if srcIndex == 0:
            return str(round(num, 2)) + ' ' + units[0].upper()
        tmp = num
        while srcIndex != 0:
            num = num / 1024
            if num < 1:
                return str(round(tmp, 2)) + ' ' + units[srcIndex].upper()
            tmp = num
            srcIndex = srcIndex - 1

        return str(round(tmp, 2)) + ' ' + units[srcIndex].upper()
    except:
        return '0 KB'