# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/dustmail/dustmailbackClient.py
# Compiled at: 2010-06-01 14:15:46
from dust.util.jsonrpc.proxy import ServiceProxy

class DustmailbackClient(ServiceProxy):

    def __init__(self, router):
        ServiceProxy.__init__(self, router, serviceName='dustmailback')