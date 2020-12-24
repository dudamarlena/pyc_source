# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/ssh/policy.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import paramiko
from reviewboard.ssh.errors import UnknownHostKeyError

class RaiseUnknownHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    """A Paramiko policy that raises UnknownHostKeyError for missing keys."""

    def missing_host_key(self, client, hostname, key):
        raise UnknownHostKeyError(hostname, key)