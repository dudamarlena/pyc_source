# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_vendor/requests/packages.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 695 bytes
import sys
for package in ('urllib3', 'idna', 'chardet'):
    vendored_package = 'pip._vendor.' + package
    locals()[package] = __import__(vendored_package)
    for mod in list(sys.modules):
        if mod == vendored_package or mod.startswith(vendored_package + '.'):
            unprefixed_mod = mod[len('pip._vendor.'):]
            sys.modules['pip._vendor.requests.packages.' + unprefixed_mod] = sys.modules[mod]