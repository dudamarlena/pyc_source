# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\common_ui.py
# Compiled at: 2019-08-04 05:05:22
# Size of source mod 2**32: 229 bytes


def first_line(string_with_newlines):
    return string_with_newlines.split('\n', 1)[0]


if not first_line('abcd\ne') == 'abcd':
    raise AssertionError
else:
    assert first_line('ab') == 'ab'
    assert first_line('') == ''