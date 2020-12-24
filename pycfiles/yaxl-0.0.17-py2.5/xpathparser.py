# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\yaxl\xpathparser.py
# Compiled at: 2006-10-29 18:57:37


def parse_expression(s):
    for char in s:
        if char == '(':
            yield LPAREN