# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/service.py
# Compiled at: 2019-09-15 01:25:44
# Size of source mod 2**32: 2317 bytes
from twisted.application import service
from twisted.internet.protocol import ServerFactory
from ampoule import rpool

def makeService(options):
    """
    Create the service for the application
    """
    ms = service.MultiService()
    from ampoule.pool import ProcessPool
    from ampoule.main import ProcessStarter
    name = options['name']
    ampport = options['ampport']
    ampinterface = options['ampinterface']
    child = options['child']
    parent = options['parent']
    min = options['min']
    max = options['max']
    maxIdle = options['max_idle']
    recycle = options['recycle']
    childReactor = options['reactor']
    timeout = options['timeout']
    starter = ProcessStarter(packages=('twisted', 'ampoule'), childReactor=childReactor)
    pp = ProcessPool(child, parent, min, max, name, maxIdle, recycle, starter, timeout)
    svc = AMPouleService(pp, child, ampport, ampinterface)
    svc.setServiceParent(ms)
    return ms


class AMPouleService(service.Service):

    def __init__(self, pool, child, port, interface):
        self.pool = pool
        self.port = port
        self.child = child
        self.interface = interface
        self.server = None

    def startService(self):
        """
        Before reactor.run() is called we setup the system.
        """
        service.Service.startService(self)
        from twisted.internet import reactor
        try:
            factory = ServerFactory()
            factory.protocol = lambda : rpool.AMPProxy(wrapped=(self.pool.doWork), child=(self.child))
            self.server = reactor.listenTCP((self.port), factory,
              interface=(self.interface))
            reactor.callLater(0, self.pool.start)
        except:
            import traceback
            print(traceback.format_exc())

    def stopService(self):
        service.Service.stopService(self)
        if self.server is not None:
            self.server.stopListening()
        return self.pool.stop()