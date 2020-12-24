# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/calcutils/__init__.py
# Compiled at: 2019-11-02 01:58:26
# Size of source mod 2**32: 114 bytes
from calcutils.calcutils import evalall
all_values = ''
for exp in evalall():
    all_values += '%s;\n' % exp