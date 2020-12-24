# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/instruction_name_and_argument_splitter.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 237 bytes


def splitter(line: str) -> str:
    s = line.lstrip()
    if not s:
        raise ValueError('Line contains no instruction name')
    idx = 1
    l = len(s)
    while idx < l and not s[idx].isspace():
        idx += 1

    return s[:idx]