# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/__init__.py
# Compiled at: 2020-02-05 10:16:56
# Size of source mod 2**32: 264 bytes
__doc__ = '\nModule package aedir_pproc\n'
from .__about__ import __version__, __author__, __license__
import os
os.environ['LDAPRC'] = '/opt/ae-dir/etc/ldap.conf'
import ldap0