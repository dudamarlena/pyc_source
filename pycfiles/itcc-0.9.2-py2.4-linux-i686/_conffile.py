# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/_conffile.py
# Compiled at: 2008-04-20 13:19:45


def conffile(ifile):
    for line in ifile:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        yield line