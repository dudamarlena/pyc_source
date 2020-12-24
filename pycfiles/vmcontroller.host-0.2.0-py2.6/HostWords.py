# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/host/services/HostWords.py
# Compiled at: 2011-03-04 15:52:41
try:
    import inspect, logging, sys, uuid
    from vmcontroller.common import support, exceptions, BaseWord, destinations, EntityDescriptor
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

logger = logging.getLogger(__name__)

def getWords():
    currentModule = sys.modules[__name__]
    return dict(inspect.getmembers(currentModule, inspect.isclass))


class PING(BaseWord):

    def howToSay(self, dst):
        self.frame.headers['to'] = dst
        self.frame.headers['destination'] = destinations.CMD_REQ_DESTINATION
        self.frame.headers['ping-id'] = uuid.uuid1()
        return self.frame.pack()


class PONG(BaseWord):

    def listenAndAct(self, msg):
        self.subject.processPong(msg)


class CMD_RUN(BaseWord):

    def howToSay(self, to, cmdId, cmd, args=(), env={}, path=None, fileForStdin=''):
        headers = {}
        headers['destination'] = destinations.CMD_REQ_DESTINATION
        headers['to'] = to
        headers['cmd-id'] = cmdId
        headers['cmd'] = cmd
        headers['args'] = args
        headers['env'] = env
        headers['path'] = path
        headers['fileForStdin'] = fileForStdin
        self.frame.headers = headers
        return self.frame.pack()


class CMD_RESULT(BaseWord):

    def listenAndAct(self, resultsMsg):
        self.subject.processCmdResult(resultsMsg)


class HELLO(BaseWord):

    def listenAndAct(self, msg):
        headers = msg['headers']
        vmDescriptor = EntityDescriptor.deserialize(headers['descriptor'])
        self.subject.addVM(vmDescriptor)


class BYE(BaseWord):

    def listenAndAct(self, msg):
        headers = msg['headers']
        who = headers['id']
        self.subject.removeVM(who)


class AINT(BaseWord):

    def listenAndAct(self, requester, msg):
        logger.warn("Unknown message type received. Data = '%s'" % str(msg))