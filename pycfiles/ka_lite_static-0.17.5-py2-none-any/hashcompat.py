# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/hashcompat.py
# Compiled at: 2018-07-11 18:15:30
"""
The md5 and sha modules are deprecated since Python 2.5, replaced by the
hashlib module containing both hash algorithms. Here, we provide a common
interface to the md5 and sha constructors, depending on system version.
"""
import warnings
warnings.warn('django.utils.hashcompat is deprecated; use hashlib instead', DeprecationWarning)
import hashlib
md5_constructor = hashlib.md5
md5_hmac = md5_constructor
sha_constructor = hashlib.sha1
sha_hmac = sha_constructor