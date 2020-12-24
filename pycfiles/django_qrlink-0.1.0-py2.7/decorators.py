# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qrlink/decorators.py
# Compiled at: 2011-02-15 04:41:43
from qrlink.middleware import QrlinkMiddleware
from django.utils.decorators import decorator_from_middleware
qrlink = decorator_from_middleware(QrlinkMiddleware)