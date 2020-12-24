# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/parguments/utils.py
# Compiled at: 2013-05-18 10:24:51


def count_indentation(lines):
    if not isinstance(lines, (list, tuple)):
        lines = lines.splitlines()
    indentations = []
    for line in lines:
        if not line.strip(' '):
            continue
        indentations.append(len(line) - len(line.lstrip(' ')))

    return min(indentations)


def remove_indentation(lines):
    if not isinstance(lines, (list, tuple)):
        lines = lines.splitlines()
    i = count_indentation(lines)
    return ('\n').join([ line[i:] if len(line) > i else '' for line in lines ])