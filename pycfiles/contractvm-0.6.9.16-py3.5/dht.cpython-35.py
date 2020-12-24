# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/dht.py
# Compiled at: 2015-11-30 17:37:59
# Size of source mod 2**32: 2759 bytes
import time, logging, random, kad, threading
from threading import Thread, Lock, Timer
from . import config
logger = logging.getLogger(config.APP_NAME)

class DHT:

    def __init__(self, port, seedlist=[], dhtfile='', info={}):
        self.dhtfile = dhtfile
        self.seeds = []
        self.info = info
        self.port = port
        self.temp = {'index': 0}
        self.storage = kad.storage.Shelve(self.dhtfile)
        self.writelock = Lock()
        for peer in seedlist:
            peer = peer.split(':')
            if len(peer) == 2:
                self.seeds.append((peer[0], int(peer[1])))
                logger.debug('Binding peer (%s:%d)', peer[0], int(peer[1]))

    def prepare(self, data):
        self.writelock.acquire()
        self.temp['index'] += 1
        tempid = str(self.temp['index'])
        self.temp[tempid] = data
        logger.debug('Prepare temp data %s (%d in the buffer)', str(tempid), len(self.temp))
        self.writelock.release()
        return tempid

    def publish(self, tempid, key):
        self.writelock.acquire()
        tempid = str(tempid)
        if tempid not in self.temp:
            self.writelock.release()
            return
        logger.debug('Publish temp data %s -> %s', str(tempid), key)
        data = self.temp[tempid]
        r = self.set(key, data)
        del self.temp[str(tempid)]
        self.writelock.release()
        return r

    def startServiceThread(self):
        self.thread = Thread(target=self.serviceThread, args=())
        self.thread.start()

    def run(self):
        logger.info('Bootstraping DHT from %d nodes, listening on port %d', len(self.seeds), self.port)
        self.bootstrap()

    def set(self, key, value):
        self.dht[key] = value
        logger.debug('Storing %s', key)
        return True

    def identity(self):
        return self.dht.identity()

    def get(self, key, handler, handlerdata):
        logger.info('Waiting for %s', key)
        self.dht.get(key, lambda d: handler(handlerdata, d))

    def bootstrap(self):
        self.dht = kad.DHT('', int(self.port), storage=self.storage, info=str(self.info))
        self.dht.bootstrap(self.seeds)
        self.startServiceThread()

    def peers(self):
        return self.dht.peers()

    def serviceThread(self):
        i = 0
        while True:
            if i % 4 == 0:
                logger.debug('Discovering nodes, %d total', len(self.peers()))
            try:
                self.dht.bootstrap()
            except:
                pass

            time.sleep(60)
            i += 1