# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/method.py
# Compiled at: 2015-11-15 14:49:39
from healthvaultlib.helpers.requestmanager import RequestManager

class Method:

    def __init__(self, request, response):
        self.request = request
        self.response = response

    def execute(self, connection):
        requestmgr = RequestManager(self, connection)
        requestmgr.makerequest()