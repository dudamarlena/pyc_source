# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/compat/dateandtime.py
# Compiled at: 2019-10-17 01:00:19
import time
from datetime import datetime
from sys import version_info
__all__ = [
 'strptime']
if version_info[:2] <= (2, 4):

    def strptime(text, dateFormat):
        return datetime(*time.strptime(text, dateFormat)[0:6])


else:

    def strptime(text, dateFormat):
        return datetime.strptime(text, dateFormat)