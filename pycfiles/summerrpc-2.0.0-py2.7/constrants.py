# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/constrants.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'ERRNO_CONNRESET']
__authors__ = ['Tim Chow']
import errno
ERRNO_CONNRESET = (
 errno.ECONNRESET,
 errno.ECONNABORTED,
 errno.EPIPE,
 errno.ETIMEDOUT)