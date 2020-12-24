# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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