# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytextgrid/get_named_value.py
# Compiled at: 2018-12-13 05:11:22
# Size of source mod 2**32: 396 bytes
import re

def getintval(line, field_name):
    m = re.match('\\s*%s\\s*\\=\\s*(\\d+)\\s*' % field_name, line)
    return int(m.group(1))


def getfloatval(line, field_name):
    m = re.match('\\s*%s\\s*\\=\\s*((\\w|\\.)+)\\s*' % field_name, line)
    f = float(m.group(1))
    return f


def getstringval(line, field_name):
    m = re.match('\\s*%s\\s*\\=\\s*\\"(.*)\\"\\s*' % field_name, line)
    return m.group(1)