# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymessagefocus2/client.py
# Compiled at: 2016-08-14 13:02:32
from xmlrpclib import ServerProxy
from transport import Transport

class Client(ServerProxy):

    def __init__(self, organisation, username, password, verbose=False):
        ServerProxy.__init__(self, 'https://%s.%s:%s@app.adestra.com/api/xmlrpc' % (organisation, username, password), transport=Transport(use_datetime=True), encoding='UTF-8', allow_none=True, verbose=verbose)