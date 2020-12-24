# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5924.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import univ
id_kp = univ.ObjectIdentifier('1.3.6.1.5.5.7.3')
id_kp_sipDomain = id_kp + (20, )