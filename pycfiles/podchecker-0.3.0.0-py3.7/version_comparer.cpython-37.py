# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/podchecker/utils/version_comparer.py
# Compiled at: 2019-07-21 09:30:19
# Size of source mod 2**32: 3688 bytes
from enum import Enum, unique

@unique
class VersionCompareResult(Enum):
    equal = '-'
    u = '↑'
    uu = '↑↑'
    uuu = '↑↑↑'
    l = '↓'
    ll = '↓↓'
    lll = '↓↓↓'

    def isEqual(self):
        return self == VersionCompareResult.equal

    def isUpper(self):
        return self == VersionCompareResult.u or self == VersionCompareResult.uu or self == VersionCompareResult.uuu

    def isLower(self):
        return self == VersionCompareResult.l or self == VersionCompareResult.ll or self == VersionCompareResult.lll


class VersionCompareMap(object):
    default_equal = VersionCompareResult.equal
    emap = {1: VersionCompareResult.equal}
    default_upper = VersionCompareResult.u
    umap = {0:VersionCompareResult.uuu, 
     1:VersionCompareResult.uu, 
     2:VersionCompareResult.u}
    default_lower = VersionCompareResult.l
    lmap = {0:VersionCompareResult.lll, 
     1:VersionCompareResult.ll, 
     2:VersionCompareResult.l}


class VersionComparer(object):

    def __init__(self, enabledPrint=False):
        self.enabledPrint = enabledPrint

    def compare(self, v1: str, v2: str) -> VersionCompareResult:
        splitList1 = v1.split('.')
        splitList2 = v2.split('.')
        maxCount = max(len(splitList1), len(splitList2))
        {splitList1.append('0') for _ in range(maxCount - len(splitList1))}
        {splitList2.append('0') for _ in range(maxCount - len(splitList2))}

        def _sub_compare(a, b, level) -> VersionCompareResult:
            if a == b:
                return VersionCompareMap.emap.get(level, VersionCompareMap.default_equal)
            if a < b:
                return VersionCompareMap.lmap.get(level, VersionCompareMap.default_lower)
            return VersionCompareMap.umap.get(level, VersionCompareMap.default_upper)

        compare_result = VersionCompareResult.equal
        for i in range(maxCount):
            try:
                compare_result = _sub_compare(int(splitList1[i]), int(splitList2[i]), i)
                if compare_result != VersionCompareResult.equal:
                    break
            except ValueError as _:
                try:
                    compare_result = _sub_compare(splitList1[i], splitList2[i], i)
                    if compare_result != VersionCompareResult.equal:
                        break
                finally:
                    _ = None
                    del _

        if self.enabledPrint:
            print(f"compare {v1} to {v2} : {compare_result.value}")
        return compare_result


def unittest():
    print('---')
    VersionComparer(True).compare('1.2', '1.2.0')
    print(VersionComparer().compare('1.0.0', '1.0').value)
    print('---↑')
    VersionComparer(True).compare('2.2.1', '1.2.2')
    VersionComparer(True).compare('1.2.1', '1.1.1')
    VersionComparer(True).compare('1.2.1', '1.2.0')
    print('---↓')
    VersionComparer(True).compare('1.2.1', '1.2.2')
    VersionComparer(True).compare('1.2.1', '1.3.1.1')
    VersionComparer(True).compare('1.2.1', '2.2.2')
    print('---misc')
    VersionComparer(True).compare('1.32.1', '1.3e.1')
    VersionComparer(True).compare('1.26.1', '1.218.1')
    VersionComparer(True).compare('1.39.1', '1.312e.1')