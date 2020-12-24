# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/backend/node.py
# Compiled at: 2015-12-16 03:40:29
# Size of source mod 2**32: 2497 bytes
import requests, json, logging, time, shelve, socket, codecs, binascii
from pycoin.block import Block
from threading import Thread
from threading import Lock
from pycoin.serialize import b2h_rev, h2b
from bitpeer import clients, networks, node, serializers
from ..chain.message import Message
from .backend import *
from .. import config
from io import BytesIO
logger = logging.getLogger(config.APP_NAME)

class Node(Backend):

    def blockFilter(block):
        v = []
        for tx in block.txs:
            tt = tx.as_hex()
            try:
                if Message.isMessage(tt):
                    v.append(tx)
            except:
                pass

        block.txs = v
        return block

    def __init__(self, chain, dbfile, genesisblock=None):
        if not networks.isSupported(chain):
            raise ChainNotSupportedException()
        self.genesis = genesisblock
        self.tx_cache = {}
        self.thread = None
        self.lastID = 0
        self.node = node.Node(chain, dbfile, self.genesis[0], self.genesis[1], maxpeers=25, logger=logger)
        self.node.blockFilter = Node.blockFilter

    def getChainCode(self):
        return self.chain

    def connect(self):
        logger.info('Waiting for bootstrap from seed servers')
        try:
            self.node.bootstrap()
        except:
            logger.critical('No reachable seed server found')
            return False

        try:
            self.node.connect()
        except:
            logger.critical('No peer available')
            return False

        logger.info('Bootstraped from %d peers (%d nodes discovered)', len(self.node.clients), len(self.node.peers))
        self.thread = Thread(target=self.node.loop, args=())
        self.thread.start()
        return True

    def getLastBlockHeight(self):
        return self.node.getLastBlockHeight()

    def getBlockHash(self, index):
        self.lastID = index
        return self.node.getBlockHash(index)

    def getBlockByHash(self, bhash):
        if bhash == None:
            return
        block = self.node.getBlockByHash(bhash)
        v = []
        d = {}
        for tx in block.txs:
            v.append(tx.id())
            d[tx.id()] = tx.as_hex()

        self.tx_cache = d
        block = {'height': self.lastID, 'time': block.timestamp, 'hash': bhash, 'tx': v}
        return block

    def broadcastTransaction(self, transaction):
        return self.node.broadcastTransaction(transaction)

    def getTransaction(self, txid):
        return self.tx_cache[txid]