# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dhclientlist\server\settings.py
# Compiled at: 2013-09-11 01:23:44
from socket import gethostname
import time
CERT_C = 'BR'
CERT_ST = 'Rio de Janeiro'
CERT_L = 'Rio de Janeiro'
CERT_O = 'INOA'
CERT_OU = 'INOA'
CERT_SERIAL = int(time.time())
CERT_CN = gethostname()
CERT_NOT_BEFORE = 0
CERT_NOT_AFTER = 315360000
PKEY_BITS = 1024