# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webchuan\decorator.py
# Compiled at: 2008-10-19 04:07:41
import logging
from twisted.internet import reactor
import element, interface
log = logging.getLogger(__name__)

class Decorator(element.Element, interface.ElementHandler):
    """Element that decorate another element
    
    """

    def __init__(self, name, target, *args, **kwargs):
        """
        
        @param name: name of decorator
        @param target: target to decorate
        """
        element.Element.__init__(self, name, *args, **kwargs)
        self.target = target
        self.connections = []
        self.bind()

    def __del__(self):
        self.unbind()

    def bind(self):
        """Bind events
        
        """
        self.connections.append(self.target.outputEvent.connect(self.handleOutput))
        self.connections.append(self.target.requireEvent.connect(self.handleRequest))
        self.connections.append(self.target.failEvent.connect(self.handleFailure))

    def unbind(self):
        """Unbind all events
        
        """
        [ connection.disconnect() for connection in self.connections ]


class Retry(Decorator):
    """Element for retrying another element
    
    """

    def __init__(self, name, target, times=5, *args, **kwargs):
        """
        
        @param name: name of retry
        @param target: target to retry
        @param times: how many times to retry
        """
        Decorator.__init__(self, name, target, *args, **kwargs)
        self.times = times
        self.errorList = []
        self.data = None
        return

    def doTry(self, data, **kwargs):
        """Try to input
        
        """
        self.target.input(data, **kwargs)

    def handleOutput(self, element, data, port, **kwargs):
        log.info('Try "%s" successfully with %s failures', self.target, len(self.errorList))
        self.output(data, port, **kwargs)
        self.errorList = []
        self.data = None
        return

    def handleRequest(self, element):
        if self.data is not None:
            (data, kwargs) = self.data
            self.doTry(data, **kwargs)
        else:
            self.require()
        return

    def handleFailure(self, element, excInfo, data, **kwargs):
        self.errorList.append(excInfo)
        if len(self.errorList) > self.times:
            log.warning('Trying "%s" exceed failed %s times', self.target, self.times)
            self.fail(excInfo, data, **kwargs)
            self.errorList = []
            self.data = None
        else:
            log.warning('Trying "%s" failed %s times', self.target, len(self.errorList))
            self.data = (
             data, kwargs)
        return

    def handleData(self, data, **kwargs):
        self.doTry(data, **kwargs)


if __name__ == '__main__':
    import base
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    getPage = base.GetPage('getPage')
    retry = Retry('retry', getPage)
    retry.input('http://www.google2.com')
    reactor.run()