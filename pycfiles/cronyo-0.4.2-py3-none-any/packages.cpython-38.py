# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/requests/packages.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 542 bytes
import sys
for package in ('urllib3', 'idna', 'chardet'):
    locals()[package] = __import__(package)
    for mod in list(sys.modules):
        if mod == package or mod.startswith(package + '.'):
            sys.modules['requests.packages.' + mod] = sys.modules[mod]