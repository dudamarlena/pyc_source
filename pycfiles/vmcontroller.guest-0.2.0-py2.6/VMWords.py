# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/guest/services/VMWords.py
# Compiled at: 2011-03-04 15:52:41
try:
    from vmcontroller.common import support, exceptions
    from vmcontroller.common import BaseWord
    from vmcontroller.common import destinations
    import CommandExecuter, sys, inspect, fnmatch
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

def getWords():
    currentModule = sys.modules[__name__]
    return dict(inspect.getmembers(currentModule, inspect.isclass))


class PING(BaseWord):

    def listenAndAct(self, msg):
        headers = msg['headers']
        if fnmatch.fnmatch(self.subject.descriptor.id, headers['to']):
            self.subject.pong(msg)


class PONG(BaseWord):

    def howToSay(self, pingMsg):
        headers = {}
        headers['destination'] = destinations.CMD_RES_DESTINATION
        headers['ping-id'] = pingMsg['headers']['ping-id']
        headers['timestamp'] = pingMsg['headers']['timestamp']
        headers['from'] = self.subject.id
        self.frame.headers = headers
        return self.frame.pack()


class CMD_RUN(BaseWord):

    def listenAndAct(self, msg):
        headers = msg['headers']
        if fnmatch.fnmatch(self.subject.descriptor.id, headers['to']):
            paramsList = ('cmd', 'args', 'env', 'path', 'fileForStdin')
            params = {}
            for p in paramsList:
                params[p] = headers.get(p)

            cmdId = headers.get('cmd-id')
            cmdExecuter = CommandExecuter.CommandExecuter(cmdId, params)
            cmdExecuter.executeCommand().addCallback(cmdExecuter.getExecutionResults).addErrback(cmdExecuter.errorHandler).addCallback(self.subject.dealWithExecutionResults)


class CMD_RESULT(BaseWord):

    def howToSay(self, results):
        self.frame.headers['destination'] = destinations.CMD_RES_DESTINATION
        self.frame.headers['cmd-id'] = results['cmd-id']
        results = support.serialize(results)
        self.frame.body = (' ').join((self.frame.body, results))
        return self.frame.pack()


class HELLO(BaseWord):

    def howToSay(self):
        self.frame.headers = {'destination': destinations.CONN_DESTINATION, 'descriptor': self.subject.descriptor.serialize()}
        return self.frame.pack()


class BYE(BaseWord):

    def howToSay(self):
        self.frame.headers = {'destination': destinations.CONN_DESTINATION, 'descriptor': self.subject.descriptor.serialize()}
        return self.frame.pack()


class AINT(BaseWord):

    def listenAndAct(self, requester, msg):
        logger.warn("Unknown message type received. Data = '%s'" % str(msg))