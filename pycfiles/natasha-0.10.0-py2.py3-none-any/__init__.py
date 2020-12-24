# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alexkuk/natasha/natasha/natasha/data/__init__.py
# Compiled at: 2017-09-21 09:53:14
from __future__ import unicode_literals
from io import open
import os

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def maybe_strip_comment(line):
    if b'#' in line:
        line = line[:line.index(b'#')]
        line = line.rstrip()
    return line


def load_lines(filename):
    path = get_path(filename)
    with open(path, encoding=b'utf-8') as (file):
        for line in file:
            line = line.rstrip(b'\n')
            line = maybe_strip_comment(line)
            yield line