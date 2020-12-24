# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/felix/Documentos/tmp/python-emailahoy/emailahoy/exceptions.py
# Compiled at: 2019-06-15 14:23:42
# Size of source mod 2**32: 247 bytes
import os

class UnableToVerifyException(Exception):
    __doc__ = 'It was impossible to verify the existence of this email'


class HostSystemNotSupportedException(Exception):
    f"The host system ('{os.name}') is not supported for this package"