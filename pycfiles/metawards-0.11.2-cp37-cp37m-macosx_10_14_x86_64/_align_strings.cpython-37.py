# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/utils/_align_strings.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 853 bytes
from typing import List as _List
__all__ = [
 'align_strings']

def align_strings(strings: _List[str], sep: str=':') -> _List[str]:
    """Align the passed list of strings such that they are aligned
       against every appearance of 'sep'
    """
    results = []
    size = []
    for string in strings:
        words = string.split(sep)
        for i, word in enumerate(words):
            if i >= len(size):
                size.append(len(word))

    for string in strings:
        words = string.split(sep)
        result = ''
        for i, word in enumerate(words):
            diff = size[i] - len(word)
            result += diff * ' ' + word
            if i < len(words) - 1:
                result += sep

        results.append(result)

    return results