# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cvttf\char_range.py
# Compiled at: 2019-06-03 03:50:12
# Size of source mod 2**32: 1011 bytes
import os
from fontTools.ttLib import TTFont
from typing import Union, Iterable, Set

def find_supported_range(font_path: [
 str]) -> Set[str]:
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"font path: {font_path} does not exist.")
    ranges = set()
    with TTFont(font_path, 0, ignoreDecompileErrors=True) as (ttf):
        for x in ttf['cmap'].tables:
            for code in x.cmap.values():
                point = int(code.replace('uni', '\\u').replace('cid', '').lower())
                ch = chr(point)
                ranges.add(ch)

    return ranges


if __name__ == '__main__':
    ranges = find_supported_range('.\\fonts\\NotoSansCJKtc-Regular.otf')
    print('x' in ranges)