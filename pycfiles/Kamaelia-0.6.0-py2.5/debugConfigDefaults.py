# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/debugConfigDefaults.py
# Compiled at: 2008-10-19 12:19:52
"""===============================
Default debugging configuration
===============================

This file defines default configuration used by Axon.debug.debug when it cannot
find a configuration file to load.

The defaultConfig() method returns the default configuration.
"""
_tags = 'debugTestClass.even\ndebugTestClass.triple\ndebugTestClass.run\ndebugTestClass.__init__\ndebugTestClass.randomChange\nmicroprocess.microprocess\nmicroprocess.__str__\nmicroprocess.__init__\nmicroprocess.setthread\nmicroprocess._isStopped\nmicroprocess._isRunnable\nmicroprocess.stop\nmicroprocess.pause\nmicroprocess._unpause\nmicroprocess.activate\nmicroprocess.main\nmicroprocess._unpause\nscheduler.scheduler\nscheduler.__init__\nscheduler._addThread\nscheduler.main\nscheduler.main.threads\nscheduler.objecttrack\nscheduler.runThreads\nmicrothread.microthread\nmicrothread.__init__\nmicrothread.activate\npostman.postman\npostman.main\npostman.__init__\npostman.__str__\npostman.register\npostman.registerlinkage\npostman.deregister\npostman.deregisterlinkage\npostman.showqueuelengths\npostman.findrecipient\npostman.domessagedelivery.linkages\npostman.domessagedelivery\npostman.specificTransits\npostman.messagedelivery.fail\ncomponent.component\ncomponent.Component\ncomponent.__init__\ncomponent.__str__\ncomponent.dataReady\ncomponent.link\ncomponent.recv\ncomponent.send\ncomponent.doSomething\ncomponent.mainBody\ncomponent.main\ncomponent.addChildren\ncomponent.removeChild\ncomponent.childComponents\ncomponent.initialiseComponent\ncomponent.closeDownComponent\ncomponent._collect\ncomponent._deliver\ncomponent.__addChild\nlinkage.linkage\nidGen.idGen\nidGen.numId\nidGen.strId\nidGen.tupleId\nReadFileAdapter.main\nAudioCookieProtocol.initialiseComponent\nFortuneCookieProtocol.main\nSimpleServer.checkOOBInfo\nSimpleServer.handleClosedCSA\nSimpleServer.handleNewCSA\nSimpleServerTestProtocol.__init__\nSimpleServerTestProtocol.mainBody\nSimpleServerTestProtocol.closeDownComponent\nHTTPServer.initialiseComponent\nMimeRequestComponent.mainBody\nPrimaryListenSocket.makeTCPServerPort\nConnectedSocketAdapter.handleDataReady\nConnectedSocketAdapter.handleDataSend\nConnectedSocketAdapter.mainBody\n'

def defaultConfig():
    """   Returns a default debugging configuration - a dictionary mapping section
   names to (level, location) tuples
   """
    debugConfig = {}
    for tag in _tags.split('\n'):
        debugConfig[tag] = (0, 'default')

    return debugConfig


if __name__ == '__main__':
    import pprint
    config = defaultConfig()
    pprint.pprint(config)