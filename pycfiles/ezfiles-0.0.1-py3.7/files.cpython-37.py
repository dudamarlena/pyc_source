# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ezfiles/files.py
# Compiled at: 2019-12-02 04:04:27
# Size of source mod 2**32: 898 bytes
import os, json
from typing import List

def readlines(filename: str, strip_newline: bool=True) -> List:
    with open(os.path.abspath(filename), 'r') as (f):
        lines = f.readlines()
    if not strip_newline:
        return lines
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip())

    return new_lines


def writelines(lines: List, filename, append_newline: bool=True) -> None:
    newlines = []
    for line in lines:
        if append_newline:
            line.endswith('\n') or newlines.append(f"{line}\n")
        else:
            newlines.append(line)

    with open(filename, 'w') as (f):
        f.writelines(newlines)


def readstr(filename: str) -> str:
    with open(filename, 'r') as (f):
        content = f.read()
    return content


def readjson(filename: str) -> dict:
    content = readstr(filename)
    return json.loads(content)