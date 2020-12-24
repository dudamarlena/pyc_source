# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests/requests/packages.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 542 bytes
import sys
for package in ('urllib3', 'idna', 'chardet'):
    locals()[package] = __import__(package)
    for mod in list(sys.modules):
        if mod == package or mod.startswith(package + '.'):
            sys.modules['requests.packages.' + mod] = sys.modules[mod]