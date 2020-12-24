# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neo/backends.py
# Compiled at: 2013-05-03 05:25:56
from foundry.backends import MultiBackend

class NeoBackendBase(object):

    def authenticate(self, username=None, password=None):
        user = super(NeoBackendBase, self).authenticate(username=username, password=password)
        if user is not None:
            user.raw_password = password
        return user


class NeoMultiBackend(NeoBackendBase, MultiBackend):
    pass