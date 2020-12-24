# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/capture0_data/utils.py
# Compiled at: 2016-09-25 19:56:11
# Size of source mod 2**32: 147 bytes
from urllib.request import urlopen

def csv_lines(url):
    with urlopen(url) as (f):
        for line in f:
            yield line.decode('utf-8')