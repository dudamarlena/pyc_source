# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/sendfile/factory.py
# Compiled at: 2013-09-10 02:43:40
from twisted.internet.protocol import ClientFactory
from cptsoul.sendfile.protocol import SendProtocol

class SendFactory(ClientFactory):

    def __init__(self, path, progressCallback, endCallback, errorCallback):
        self._path = path
        self._progressCallback = progressCallback
        self._endCallback = endCallback
        self._errorCallback = errorCallback

    def buildProtocol(self, addr):
        return SendProtocol(self._path, self._progressCallback, self._endCallback, self._errorCallback)