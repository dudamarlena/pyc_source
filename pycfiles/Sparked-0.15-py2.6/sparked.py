# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/sparked.py
# Compiled at: 2010-12-21 15:42:19
from twisted.application.service import ServiceMaker
Spark = ServiceMaker('Sparked', 'sparked.tap', 'Sparked application launcher', 'sparked')