# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir_pproc/__init__.py
# Compiled at: 2020-02-05 10:16:56
# Size of source mod 2**32: 264 bytes
"""
Module package aedir_pproc
"""
from .__about__ import __version__, __author__, __license__
import os
os.environ['LDAPRC'] = '/opt/ae-dir/etc/ldap.conf'
import ldap0