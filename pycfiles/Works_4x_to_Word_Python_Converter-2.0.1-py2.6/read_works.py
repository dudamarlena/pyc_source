# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\works4xtowordpythonconverter\read_works.py
# Compiled at: 2012-12-07 21:49:13


def read_ms_works_file(file):
    text = []
    started = False
    with open(file, 'rb') as (f):
        lines = f.readlines()
        for (i, line) in enumerate(lines):
            if line.endswith('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\n'):
                started = True
                continue
            if started:
                if line.strip().startswith('\x00') or line.strip().endswith('\x00'):
                    break
                text.append(line)

    return text[2:]