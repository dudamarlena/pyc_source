# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8209.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
id_kp = univ.ObjectIdentifier('1.3.6.1.5.5.7.3')
id_kp_bgpsec_router = id_kp + (30, )