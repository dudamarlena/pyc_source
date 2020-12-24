# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paczesiowa/projects/tvu/tests/test_compat.py
# Compiled at: 2017-02-09 14:45:58
import sys
if sys.version_info < (3, ):
    text = unicode
else:
    text = str