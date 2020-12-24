# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mservice.py
# Compiled at: 2017-08-15 11:28:10
import sys, time, atexit, signal, logging
from mrlpy.exceptions import HandshakeTimeout
from mrlpy import mcommand
from mrlpy import mutils

class MService(object):
    name = ''
    handshakeSuccessful = False
    handshakeTimeout = 1
    handshakeSleepPeriod = 0.25
    createProxyOnFailedHandshake = True
    __log = logging.getLogger(__name__)
    proxyClass = 'PythonProxy'

    def __init__(self, name=''):
        """
                Registers service with mcommand event registers and MRL service registry
                """
        if name == '':
            try:
                self.name = sys.argv[1]
            except IndexError:
                self.name = mutils.genID()

        else:
            self.name = name
        self.connectWithProxy(True)
        atexit.register(self.release)
        signal.pause()

    def setProxyClass(self, proxy):
        self.proxyClass = proxy

    def connectWithProxy(self, tryagain=False):
        """
                Utility method used for getting initialization info from proxy and running handshake
                """
        mcommand.sendCommand('runtime', 'createAndStart', [self.name, self.proxyClass])
        mrlRet = mcommand.callServiceWithJson(self.name, 'handshake', [])
        self.__log.debug('mrlRet = ' + str(mrlRet))
        mcommand.addEventListener(self.name, self.onEvent)
        start = time.time()
        lastTime = 0
        while not self.handshakeSuccessful and time.time() - start < self.handshakeTimeout:
            time.sleep(self.handshakeSleepPeriod)
            lastTime = time.time()
            if lastTime - start >= self.handshakeTimeout:
                if self.createProxyOnFailedHandshake and tryagain:
                    self.__log.info('Proxy not active. Creating proxy...')
                    mcommand.sendCommand('runtime', 'createAndStart', [self.name, 'PythonProxy'])
                    self.connectWithProxy()
                else:
                    raise HandshakeTimeout('Error attempting to sync with MRL proxy service; Proxy name = ' + str(self.name))

    def onEvent(self, e):
        """
                Handles message invocation and parsing
                of params; WARNING: DO NOT OVERRIDE
                THIS METHOD UNLESS YOU KNOW WHAT YOU
                ARE DOING!!!!!!!
                """
        ret = None
        try:
            params = (',').join(map(str, e.data))
            self.__log.debug('Invoking: ' + e.method + '(' + params + ')')
            ret = eval('self.' + e.method + '(' + params + ')')
        except Exception:
            self.__log.debug('Invoking: ' + e.method + '()')
            ret = eval('self.' + e.method + '()')

        self.returnData(ret)
        return

    def returnData(self, dat):
        mcommand.sendCommand(self.name, 'returnData', [dat])

    def handshake(self):
        """
                Second half of handshake.

                Called by proxy during the handshake procedure.
                """
        self.__log.debug('Handshake successful.')
        self.handshakeSuccessful = True

    def release(self):
        """
                Utility method for releasing the proxy service;
                Also deletes this service
                """
        mcommand.sendCommand('runtime', 'release', [self.name])
        del self