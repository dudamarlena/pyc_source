# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/util/trim.py
# Compiled at: 2012-08-01 03:51:57
"""Sorts out the docstring indentation as per :pep:`257`.

This function has been copied verbatim from the PEP above,
And is copyright (C) 1990-2012, Python Software Foundation
"""
import sys

def trim(docstring):
    """Reformats a docstring, replacing tabs with spaces and repaginating"""
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [
     lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)