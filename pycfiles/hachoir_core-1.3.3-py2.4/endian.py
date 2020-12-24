# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/endian.py
# Compiled at: 2009-09-07 17:44:28
"""
Constant values about endian.
"""
from hachoir_core.i18n import _
BIG_ENDIAN = 'ABCD'
LITTLE_ENDIAN = 'DCBA'
NETWORK_ENDIAN = BIG_ENDIAN
endian_name = {BIG_ENDIAN: _('Big endian'), LITTLE_ENDIAN: _('Little endian')}