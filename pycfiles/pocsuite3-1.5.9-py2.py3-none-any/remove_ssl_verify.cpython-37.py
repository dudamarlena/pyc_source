# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/request/patch/remove_ssl_verify.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 109 bytes
import ssl

def remove_ssl_verify():
    ssl._create_default_https_context = ssl._create_unverified_context