# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/utils/compat.py
# Compiled at: 2016-02-19 17:15:24
import sys
if sys.version_info < (3, ):

    def u(x):
        return unicode(x)


else:

    def u(x):
        return str(x)